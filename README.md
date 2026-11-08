# Exploratory Data Analysis

A practical collection of data-cleaning and exploratory data-analysis work using Python. The repository demonstrates how to move from raw datasets to reliable insights through inspection, cleaning, visualization, and interpretation.

## What this repository covers

- Loading and inspecting raw datasets
- Understanding columns, data types, and data quality
- Identifying and handling missing values and duplicate records
- Cleaning and preparing data for analysis
- Exploring distributions, relationships, and trends
- Creating visualizations with Matplotlib and Seaborn
- Summarizing findings and recording insights at the end of an analysis

## Repository contents

| Path | Description |
| --- | --- |
| [`Agriculture_cleaning  dataset.ipynb`](./Agriculture_cleaning%20%20dataset.ipynb) | Data-cleaning workflow for an agriculture dataset |
| [`student_performane_EDA.ipynb`](./student_performane_EDA.ipynb) | Exploratory analysis of student performance data |
| [`data_cleaning/`](./data_cleaning/) | Supporting data-cleaning work and resources |
| [`savanna_retail_sales_raw.csv`](./savanna_retail_sales_raw.csv) | Raw retail-sales dataset for analysis practice |

## Analysis workflow

The notebooks generally follow this process:

1. **Load the data** with Pandas.
2. **Inspect the dataset** using shape, column, data-type, and summary-statistics checks.
3. **Assess data quality** by looking for missing values, duplicates, inconsistent formats, and unusual values.
4. **Clean and transform the data** so it is consistent and ready for analysis.
5. **Perform exploratory analysis** using descriptive statistics and grouped summaries.
6. **Visualize patterns** with Matplotlib and Seaborn.
7. **Interpret the results** by documenting the main findings and insights.

## Tools and libraries

- Python 3
- Jupyter Notebook or Google Colab
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Getting started

Clone the repository and install the commonly used dependencies:

```bash
git clone https://github.com/Kasera001/Explaratory-Data-Analysis.git
cd Explaratory-Data-Analysis
pip install pandas numpy matplotlib seaborn jupyter
```

Start Jupyter Notebook:

```bash
jupyter notebook
```

Then open either notebook and run the cells from top to bottom. The notebooks can also be opened directly in Google Colab using the **Open in Colab** link where available.

## Goal

The goal of this repository is to build a repeatable, understandable data-analysis process: clean the data carefully, explore it systematically, visualize important patterns, and communicate useful insights from the results.