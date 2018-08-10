## README

### Objective
This project is based on the Instacart Market Basket Analysis Challenge from Instacart. Using data from 3 million product orders across 200,000 users, the objective is to classify whether the product will be reordered.

More details here: https://www.kaggle.com/c/instacart-market-basket-analysis
Data set: “The Instacart Online Grocery Shopping Dataset 2017”, Accessed from https://www.instacart.com/datasets/grocery-shopping-2017 on July 30, 2018


### Data
From Kaggle: 
>>> The dataset for this competition is a relational set of files describing customers' orders over time. The goal of the competition is to predict which products will be in a user's next order. The dataset is anonymized and contains a sample of over 3 million grocery orders from more than 200,000 Instacart users. For each user, we provide between 4 and 100 of their orders, with the sequence of products purchased in each order. We also provide the week and hour of day the order was placed, and a relative measure of time between orders. 
https://www.kaggle.com/c/instacart-market-basket-analysis/data

### Strategy
- Feature Engineering with data from multiple join tables
- Subsetting 5% of data for training/testing, due to computation limitations
- Oversampling to account for class imbalance
- 70/30 Train/test split by user_id
- Standard Scaling features
- Logistic Regression
- F1 score measurement
- Random Forest Classifier with hyperparameter tuning
- XG Boost with hyperparameter tuning

### Obstacles
For feature engineering, there were two issues that I ran into. 

- One was running into memory errors because the files were taking up too much space when I was joining them. I managed this by downcasting the column types, mainly from int64 to anything from int8 (Boolean columns) to int32. This was something Mike(the other one) showed me so for the first half of my project, I had to deal with a lot of kernel crashes

- Second was dealing with the NaN values for Days Since Prior Orders, because products that were purchased for the first time would end up with an NaN. I could not simply discard these rows because NaN itself was indicative of first time purchase, which is relevant in predictions. I dealt with this two alternative ways. The first method was to create separate bins, which was used for Logistic Regression. This created 7 extra dummy variable columns. The second method was to convert the NaN values to -1, which I used for tree based methods. 

### Things to note
- Because the dataset was so large (8+ million after grouping), I took out a 5% subset to run train/validation on. This 5% subset was assigned a 70/30 train/validate split, based on user_id
- There was significant imbalance, which reflected in my baseline logistic regression run, so I applied an even-weight oversampling.
- I ran logistic regression on individual features to gauge f1 scores for each one. In retrospect, and per Debbie’s advice, I should’ve done Lasso regression or use XGBoost feature importance to identify important features.
- For my business approach, my intent was to use F1 as a more well-balanced metric, and utilize recall solely to calculate the dollar amount of revenue from reorder we’d be able to predict. In this case our goal was NOT to maximize recall. I was simply using the recall (0.3) to determine the percent of ALL reorders (10% of all orders are reorders) that was predictable. In this case, our model with it’s 0.3 rate will allow us to predict the equivalent of 3% of all revenue.

