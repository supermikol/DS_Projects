# Data Science Projects
*More details can be found in the README of the repository folders.*

The three projects in this repository are:

### [Amazon Product Ranking Regression Analysis](https://github.com/supermikol/DS_Projects/tree/master/01_amazon_regression)
Using standard OLS, I set out to find correlation between various publicly available features of 12,000 scraped Amazon listings, and the product's ranking in it's respective category.

Datasize: 12,000 manually scraped Amazon listings

Tools Used:
- Selenium
- L1, L2, ElasticNet Regularization


### [Instacart Classification Problem](https://github.com/supermikol/DS_Projects/tree/master/02_instacart_classification)
Classification problem to determine whether a user will reorder a product given order history.

Datasize: 3.4 million unique orders from 200,000 users (data from Kaggle)

Tools:
- Feature Engineering from 6 join tables
- Oversampling to account for class imbalance, Standard Scaling
- F1 score measurement
- Logistic Regression
- Random Forest Classifier with hyperparameter tuning
- XG Boost with hyperparameter tuning

### [NYTimes Unsupervised NLP Clustering Analysis](https://github.com/supermikol/DS_Projects/tree/master/03_nytimes_unsupervised_NLP)
Topic coverage of the NYTimes over the 10 years period between 2007 - 2017. Used two alternative unsupervised NLP techniques to cluster all articles (Latent Semantic Analysis, and Latent Dirichlet Allocation with K-Means), and then applied the learned clustering models on annual sets of data, to track how the weight of each topic has varied over the years.

Datasize: 268,000 manually scraped articles

- TFIDF, Count Vectorizer
- Latent Semantic Analysis, Latent Dirichlet Allocation
- K-Means for clustering
- Matrix Similarity Recommendation system
