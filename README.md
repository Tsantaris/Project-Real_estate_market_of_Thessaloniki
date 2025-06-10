# Project-Real_estate_market_of_Thessaloniki

This is an ongoing project whose goal is discovering the best "value for money" houses to buy in the city of Thessaloniki in Greece. It incorporates all the stages of a data science project from data collection and data cleaning/transformation to EDA and model selection.

In the first stage we will scrape data from the biggest real estate website in Greece: spitogatos.gr. The file scrape.py contains all the necessary functions for that. In the scraping notebook we describe the scraping process in detail. The aquired data will contain a table of houses for sale with their characteristics such as price, floor level, tota area, location, number of bathrooms and rooms and year of construction.

In the second stage we will develop an ETL pipeline where we clean/transform/augment the aquired data. 

In the third and final stage we will split the data into training and evaluation sets. We  then fit several machine learning models to the data and evaluate their performance. Our goal is to choose the algorithm that predicts house prices in the best possible way.
