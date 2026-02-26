#pandas approach: 
#https://codesignal.com/learn/courses/basics-of-numpy-and-pandas-with-titanic-dataset/lessons/mastering-pandas-a-deep-dive-into-dataframes-and-data-manipulation
#https://medium.com/data-science/olympics-kaggle-dataset-exploratory-analysis-part-2-understanding-sports-4b8d73a8ec30
import pandas as pd

# your local filename:
filepath = "world-happiness-report-2021-with-highlow.csv"

df = pd.read_csv(filepath)

# whole dataset (not recommended to print all)
# print(df)

# first N rows (like slicing your list)
print(df.head(2))

# "first row"
print(df.iloc[0])

# slice rows 10..19 (like squirrels[10:20])
print(df.iloc[10:20])

# column names (like squirrels[0].keys())
print(df.columns)

# one column
print(df["Ladder score"].head(10)) # return first 10 rows 

# multiple columns (prints the first 10 rows of each column)
print(df[["Country name", "Ladder score", "Standard error of ladder score"]].head(10))

# X,Y locations of gray squirrels
gray_xy = df.loc[df["Regional indicator"] == "Western Europe", ["upperwhisker", "lowerwhisker"]]
print(gray_xy.head(10))

# how many gray squirrels?
gray_count = (df["Regional indicator"] == "Western Europe").sum()
print(gray_count)

# how many Adult vs Juvenile (overall)
print(df["Regional indicator"].value_counts(dropna=False)) # value_counts 是统计该列中每个不同值出现的次数，按照从高到低排序并且返回一个series
    #dropna = True会忽略Nan，dropna = False会把Nan也算进统计

# how many Adult vs Juvenile GRAY squirrels
#gray_age_counts = df.loc[df["Primary Fur Color"] == "Gray", "Age"].value_counts(dropna=False)
#print(gray_age_counts)

print("\n=== ANALYSIS QUESTIONS ===\n")

# Question 1: Which are the top 3 regions with the most countries having high ladder scores?
print("Question 1: Which are the top 3 regions with the most countries having high ladder scores?")
high_ladder_countries = df[df["HighLow"] == "high"]
top_3_regions = high_ladder_countries["Regional indicator"].value_counts().head(3)
print(top_3_regions)
print()

# Question 2: How many regions are there in total?
print("Question 2: How many regions are there in total?")
total_regions = df["Regional indicator"].nunique()
print(f"Total number of regions: {total_regions}")
print()

# Question 3: Which region has the most countries with data?
print("Question 3: Which region has the most countries with data?")
region_counts = df["Regional indicator"].value_counts()
print(f"Region with most countries: {region_counts.index[0]}")
print(f"Number of countries: {region_counts.iloc[0]}")
print()

