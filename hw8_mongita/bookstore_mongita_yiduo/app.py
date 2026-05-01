import os
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for
from mongita import MongitaClientDisk

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = MongitaClientDisk(os.path.join(BASE_DIR, 'mongita_data'))
db = client.bookstore
categories_col = db.category
books_col = db.book

SORT_LABELS = {
    'title':      'Title A–Z',
    'price_asc':  'Price: Low → High',
    'price_desc': 'Price: High → Low',
}


@app.context_processor
def inject_globals():
    return dict(sort_labels=SORT_LABELS)


def get_all_categories():
    return sorted(list(categories_col.find()), key=lambda c: c['categoryName'])


def sort_books(books, sort_key):
    if sort_key == 'price_asc':
        return sorted(books, key=lambda b: b['price'])
    elif sort_key == 'price_desc':
        return sorted(books, key=lambda b: b['price'], reverse=True)
    else:
        return sorted(books, key=lambda b: b['title'])


def get_next_book_id():
    books = list(books_col.find())
    if not books:
        return 1
    return max(b['bookId'] for b in books) + 1


def build_shelves(books, categories, category_id=None):
    shelves_dict = defaultdict(list)
    for b in books:
        shelves_dict[b['categoryId']].append(b)
    ordered = []
    for cat in categories:
        cid = cat['categoryId']
        if category_id is not None and cid != category_id:
            continue
        if cid in shelves_dict:
            ordered.append({
                'categoryId':    cid,
                'categoryName':  cat['categoryName'],
                'categoryImage': cat['categoryImage'],
                'books':         shelves_dict[cid],
            })
    return ordered


def base_ctx(**kwargs):
    return dict(sort_key='title', read_now=False,
                selected_category_id=None, search_term=None, **kwargs)


# ------------------------------------------
# 1. HOMEPAGE — bookshelf + category links
# ------------------------------------------
@app.route('/')
def home():
    sort_key    = request.args.get('sort', 'title')
    read_now    = request.args.get('readNow', '0') == '1'
    category_id = request.args.get('categoryId', type=int)

    categories = get_all_categories()

    query = {}
    if category_id is not None:
        query['categoryId'] = category_id
    if read_now:
        query['readNow'] = 1

    books = sort_books(list(books_col.find(query)), sort_key)
    shelves = build_shelves(books, categories, category_id)

    return render_template(
        'index.html',
        shelves=shelves,
        categories=categories,
        sort_key=sort_key,
        read_now=read_now,
        selected_category_id=category_id,
        search_term=None,
    )


# ------------------------------------------
# 2. SEARCH
# ------------------------------------------
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search', '').strip()
    sort_key    = request.form.get('sort', 'title')
    read_now    = request.form.get('readNow', '0') == '1'

    categories = get_all_categories()
    all_books  = list(books_col.find())
    books = [b for b in all_books if search_term.lower() in b['title'].lower()]
    if read_now:
        books = [b for b in books if b.get('readNow') == 1]
    books = sort_books(books, sort_key)
    shelves = build_shelves(books, categories)

    return render_template(
        'index.html',
        shelves=shelves,
        categories=categories,
        sort_key=sort_key,
        read_now=read_now,
        selected_category_id=None,
        search_term=search_term,
    )


# ------------------------------------------
# 3. READ — list all books (required)
# ------------------------------------------
@app.route('/read')
def read():
    categories = get_all_categories()
    books = sort_books(list(books_col.find()), 'title')
    return render_template('read.html', books=books,
                           categories=categories, **base_ctx())


# ------------------------------------------
# 4. BOOK DETAIL
# ------------------------------------------
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    categories = get_all_categories()
    book = books_col.find_one({'bookId': book_id})
    if not book:
        return render_template('error.html', error='Book not found',
                               categories=categories, **base_ctx()), 404
    return render_template('book_detail.html', book=book,
                           categories=categories, **base_ctx())


# ------------------------------------------
# 5. CREATE — show form (required)
# ------------------------------------------
@app.route('/create')
def create():
    categories = get_all_categories()
    return render_template('create.html', categories=categories, **base_ctx())


# ------------------------------------------
# 6. CREATE_POST — insert book (required)
# ------------------------------------------
@app.route('/create_post', methods=['POST'])
def create_post():
    categories  = get_all_categories()
    title       = request.form.get('title', '').strip()
    author      = request.form.get('author', '').strip()
    isbn        = request.form.get('isbn', '').strip()
    price       = float(request.form.get('price', 0) or 0)
    image       = request.form.get('image', '').strip()
    category_id = int(request.form.get('categoryId', 0) or 0)
    read_now    = 1 if request.form.get('readNow') == '1' else 0

    selected_cat = next((c for c in categories if c['categoryId'] == category_id), None)

    books_col.insert_one({
        'bookId':       get_next_book_id(),
        'categoryId':   category_id,
        'categoryName': selected_cat['categoryName'] if selected_cat else '',
        'title':        title,
        'author':       author,
        'isbn':         isbn,
        'price':        price,
        'image':        f'static/book/{image}' if image else '',
        'readNow':      read_now,
    })
    return redirect(url_for('read'))


# ------------------------------------------
# 7. EDIT — show pre-filled form (required)
# ------------------------------------------
@app.route('/edit/<int:book_id>')
def edit(book_id):
    categories = get_all_categories()
    book = books_col.find_one({'bookId': book_id})
    if not book:
        return render_template('error.html', error='Book not found',
                               categories=categories, **base_ctx()), 404
    return render_template('edit.html', book=book,
                           categories=categories, **base_ctx())


# ------------------------------------------
# 8. EDIT_POST — update book (required)
# ------------------------------------------
@app.route('/edit_post/<int:book_id>', methods=['POST'])
def edit_post(book_id):
    categories  = get_all_categories()
    title       = request.form.get('title', '').strip()
    author      = request.form.get('author', '').strip()
    isbn        = request.form.get('isbn', '').strip()
    price       = float(request.form.get('price', 0) or 0)
    image       = request.form.get('image', '').strip()
    category_id = int(request.form.get('categoryId', 0) or 0)
    read_now    = 1 if request.form.get('readNow') == '1' else 0

    selected_cat = next((c for c in categories if c['categoryId'] == category_id), None)

    books_col.replace_one({'bookId': book_id}, {
        'bookId':       book_id,
        'categoryId':   category_id,
        'categoryName': selected_cat['categoryName'] if selected_cat else '',
        'title':        title,
        'author':       author,
        'isbn':         isbn,
        'price':        price,
        'image':        f'static/book/{image}' if image else '',
        'readNow':      read_now,
    })
    return redirect(url_for('read'))


# ------------------------------------------
# 9. DELETE (required)
# ------------------------------------------
@app.route('/delete/<int:book_id>')
def delete(book_id):
    books_col.delete_one({'bookId': book_id})
    return redirect(url_for('read'))


# ------------------------------------------
# ERROR HANDLER
# ------------------------------------------
@app.errorhandler(Exception)
def handle_error(e):
    try:
        categories = get_all_categories()
    except Exception:
        categories = []
    return render_template('error.html', error=e,
                           categories=categories, **base_ctx()), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
