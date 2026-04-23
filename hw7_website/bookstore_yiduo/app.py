import sqlite3
import os
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'bookstore_yd.db')

SORT_MAP = {
    'title':      'book.title ASC',
    'price_asc':  'book.price ASC',
    'price_desc': 'book.price DESC',
}

SORT_LABELS = {
    'title':      'Title A–Z',
    'price_asc':  'Price: Low → High',
    'price_desc': 'Price: High → Low',
}


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.context_processor
def inject_globals():
    """Provide base-template constants to every rendered template."""
    return dict(sort_labels=SORT_LABELS)


def get_order_clause(sort_key):
    return SORT_MAP.get(sort_key, 'book.title ASC')


def get_all_categories(conn):
    return conn.execute('SELECT * FROM category ORDER BY categoryName').fetchall()


@app.route('/')
def home():
    sort_key  = request.args.get('sort', 'title')
    read_now  = request.args.get('readNow', '0') == '1'
    category_id = request.args.get('categoryId', type=int)
    order     = get_order_clause(sort_key)

    conn = get_db()
    categories = get_all_categories(conn)

    params = []
    conditions = []

    if category_id is not None:
        conditions.append('book.categoryId = ?')
        params.append(category_id)
    if read_now:
        conditions.append('book.readNow = 1')

    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''
    sql = f'''
        SELECT book.*, category.categoryName, category.categoryImage
        FROM book
        JOIN category ON book.categoryId = category.categoryId
        {where}
        ORDER BY {order}
    '''
    books = conn.execute(sql, params).fetchall()
    conn.close()

    # Group books by category, preserving sort order
    shelves = defaultdict(list)
    shelf_meta = {}
    for b in books:
        cid = b['categoryId']
        shelves[cid].append(b)
        if cid not in shelf_meta:
            shelf_meta[cid] = {
                'categoryName':  b['categoryName'],
                'categoryImage': b['categoryImage'],
            }

    # Preserve category display order (alphabetical from DB)
    ordered_shelves = []
    seen = set()
    for cat in categories:
        cid = cat['categoryId']
        if category_id is not None and cid != category_id:
            continue
        if cid in shelves:
            ordered_shelves.append({
                'categoryId':    cid,
                'categoryName':  cat['categoryName'],
                'categoryImage': cat['categoryImage'],
                'books':         shelves[cid],
            })
            seen.add(cid)

    return render_template(
        'index.html',
        shelves=ordered_shelves,
        categories=categories,
        sort_key=sort_key,
        sort_labels=SORT_LABELS,
        read_now=read_now,
        selected_category_id=category_id,
        search_term=None,
    )


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search', '').strip()
    sort_key    = request.form.get('sort', 'title')
    read_now    = request.form.get('readNow', '0') == '1'
    order       = get_order_clause(sort_key)

    conn = get_db()
    categories = get_all_categories(conn)

    conditions = ['lower(book.title) LIKE lower(?)']
    params     = [f'%{search_term}%']
    if read_now:
        conditions.append('book.readNow = 1')

    where = 'WHERE ' + ' AND '.join(conditions)
    sql = f'''
        SELECT book.*, category.categoryName, category.categoryImage
        FROM book
        JOIN category ON book.categoryId = category.categoryId
        {where}
        ORDER BY {order}
    '''
    books = conn.execute(sql, params).fetchall()
    conn.close()

    shelves = defaultdict(list)
    for b in books:
        shelves[b['categoryId']].append(b)

    ordered_shelves = []
    for cat in categories:
        cid = cat['categoryId']
        if cid in shelves:
            ordered_shelves.append({
                'categoryId':    cid,
                'categoryName':  cat['categoryName'],
                'categoryImage': cat['categoryImage'],
                'books':         shelves[cid],
            })

    return render_template(
        'index.html',
        shelves=ordered_shelves,
        categories=categories,
        sort_key=sort_key,
        sort_labels=SORT_LABELS,
        read_now=read_now,
        selected_category_id=None,
        search_term=search_term,
    )


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    conn = get_db()
    categories = get_all_categories(conn)
    book = conn.execute(
        '''SELECT book.*, category.categoryName
           FROM book
           JOIN category ON book.categoryId = category.categoryId
           WHERE book.bookId = ?''',
        (book_id,)
    ).fetchone()
    conn.close()

    if book is None:
        return render_template('error.html', error='Book not found'), 404

    return render_template('book_detail.html', book=book, categories=categories)


@app.errorhandler(Exception)
def handle_error(e):
    try:
        conn = get_db()
        categories = get_all_categories(conn)
        conn.close()
    except Exception:
        categories = []
    return render_template(
        'error.html',
        error=e,
        categories=categories,
        sort_key='title',
        read_now=False,
        selected_category_id=None,
        search_term=None,
    ), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
