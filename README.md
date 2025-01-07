# Project-spitogatos
This is an ongoing project inspired from an IBM data science course I took.

The project is about finding the best "value for money" house to buy in the city of Thessaloniki in Greece. 

First we will scrape data from the biggest real estate website in Greece: spitogatos.gr. This step is completed in the spitogatos scrape jupyter notebook. The aquired data will contain a table of houses for sale with their characteristics such as price, floor level, tota area, location, number of bathrooms and rooms and year of construction.

In the second step we will clean the aquired data. This is done in the cleaner jupyter notenook.

Finally we will split the data into training and evaluation sets. We  then fit several machine learning models to the data and evaluate their performance. Our goal is to chose the algorithm that predicts the price the best.
