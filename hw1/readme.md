# World Happiness Report 2021 - Data Analysis
## why choose this dataset?

I chose this dataset because it is based on real survey data that reflects people's life satisfaction across countries, making it directly relevant and close to everyday life. The data contains clear country-level and regional classifications and a quantitative `Ladder score`, which lets me compare happiness rates across regions and individual countries. My main interest is exploring differences in happiness by region and identifying which countries have above-average happiness scores.


## Three Questions the Dataset Can Answer

### Question 1: Which are the top 3 regions with the most countries having high ladder scores?

**Output:**
```
Regional indicator
Western Europe                 21
Latin America and Caribbean    18
Central and Eastern Europe     14
Name: count, dtype: int64
```

**Explanation:**
The dataset supports this question because it contains both the "Regional indicator" column (which categorizes countries by geographic region) and the "HighLow" column (which classifies countries as having high or low ladder scores based on whether they exceed the overall mean). By filtering for countries where HighLow equals "high" and then using value_counts() on the Regional indicator column, we can easily identify which regions have the most countries with above-average happiness scores. This reveals that Western Europe leads with 21 high-scoring countries, followed by Latin America and Caribbean with 18, and Central and Eastern Europe with 14.

### Question 2: How many regions are there in total?

**Output:**
```
Total number of regions: 10
```

**Explanation:**
The dataset's "Regional indicator" column contains categorical data grouping countries by geographic region. By using the `nunique()` method on this column, we can count the number of distinct regional values present in the dataset. This shows that the 2021 World Happiness Report covers 10 different regions globally, providing a comprehensive geographic breakdown for analyzing happiness patterns across major world regions.

### Question 3: Which region has the most countries with data?

**Output:**
```
Region with most countries: Sub-Saharan Africa
Number of countries: 36
```

**Explanation:**
Using the `value_counts()` method on the "Regional indicator" column returns the frequency of countries in each region, sorted in descending order. This analysis reveals that Sub-Saharan Africa has the highest representation with 36 countries in the dataset. This makes sense as Africa has 54 countries total, and many are concentrated in the sub-Saharan region. Having comprehensive coverage of this region is valuable for understanding happiness patterns in developing economies and diverse cultural contexts.

---

## What the Data Cannot Answer

### A Question We Wish We Could Answer

**Question:** How have happiness scores changed over time for each country?

**What data is missing:**
The current dataset only contains data from 2021. To answer temporal questions, we would need:
- Historical data from multiple years (e.g., 2015-2021)
- Time-series structure with year as a variable
- Consistent country coverage across years

**Assumptions that would be misleading:**
If we tried to answer this question with only 2021 data, we might be tempted to assume that countries with high scores have always been happy, or that regional rankings have remained stable. However, economic crises, political changes, natural disasters, or pandemics could significantly shift happiness scores year to year. Without historical data, any inference about trends or stability would be pure speculation and potentially misleading. 