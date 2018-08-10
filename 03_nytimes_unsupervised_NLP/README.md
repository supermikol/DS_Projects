## Unsupervised Learning topic modeling of historical New York Times articles

Datasize: 268,000 manually scraped articles

### Objective
The goal of this project was to track how topic coverage has varied over 10 years with the New York Times. I used two alternative unsupervised NLP techniques to cluster all articles (Latent Semantic Analysis, and Latent Dirichlet Allocation with K-Means), and then applied the learned clustering models on an annual basis, to track how the weight of each topic has varied over the years.

### Data Scraping

File: `nyt_scraper.py`
The original plan was to simply utilize the [NYTimes API](https://developer.nytimes.com/) to obtain lead sentences from 268,000 articles, but later determined that 250 character length snippets would not be sufficient. As a result, I built a scraper `nyt_scraper.py` to retrieve full articles from the urls provided through the API. There were around 3700 articles per month on average, for a total of 268,000 articles that I scraped across 3 EC2 servers.

### Data Modeling with LSI:

File: `NYTLSA.ipynb`
1. Load and parse the merged csv file (containing all 268k articles) and then a random subset of 20k articles per each year, for 140,000 articles.
2. Applied TFIDF vectorizing. This was chosen because I think the methodology is ideal for drawing distinctions between articles. 
3. Applied LSI modeling and generated an elbow plot with 150 topics, so I could visualize how many topics would be ideal moving forward. Although 10 features seemed to cover most of the variance, I didn’t think it would hurt to go with 50, since I could capture additional noise/variance. Since my next step involved clustering, I didn’t see the need to narrow the topics down at this point.
4. (sidetrack) At this point, I created a MatrixSimilarity, and was able to pull similar articles so that I could build a recommendation system around it, but this was useless for my case. The code is still available in the notebook, but commented out.
5. K-Means: With the LSI transformed set of data, I created a silhouette plot up to 30 clusters. Without a clear inflection point in the plot, I decided to settle with 18.

### Retro Fitting the Data
The step after this was to fit individual year’s data back into this general model, so I could get an accurate breakdown of the number of articles that are categorized in each of the 20 clusters. This taking an individual year’s articles and:
- Converting with the pre-fitted TFIDF vectorizor (on the entire year’s data), 
- Transforming with the pre-trained LSI model (50 terms) and then
- Predicting the clusters with the pre-trained KMeans cluster(20 clusters)
This effectively gave me a total counts of articles per category, per year.
The method in the notebook corresponding to this is `get_clusters_for_year`

#### Cluster Definition
The problem with this approach is that each cluster was defined by the set of reduced features that itself was messy to interpret, due to the nature of LSA feature reduction. Negative values and repeat terms meant I could not look at the topics themselves to figure out what belonged in the cluster. (This is what led to my LDA experiment, as described in the next section) However, I was able to manually sift through random samples of each cluster to see how articles were related. I would say 3/4 were very clearly defined (basketball, performance art, finance, politics, etc..) but there were a few clusters that were a bit messy, and felt like an amalgamation of leftover articles that didn’t belong to any existing cluster but was limited by the number of clusters available. If I were to build upon this project, I would definitely look into the clusters number and go with a higher cluster number.


### Data Modeling with LDA
File: `NYTLDA.ipynb`
Having dealt with the ambiguity of the LSA model, I wanted to see if LDA would help with better defined topics. The overall process was generally the same, with a few exceptions:
- I used CountVectorizer instead of TFIDF because it’s better suited for LDA
- I chose 20 topics instead of 50, because with LDA, the more well defined topics meant I could interpret each feature individually, now that they were sets of distinct words that more or less described an actual news topic
- The benefits of the LDA approach is that there was no need to further cluster, because each topic/feature was now more explicitly defined
However, for a few feature sets, the word weights alone didn’t necessarily give a clear indication of the topic.

For instance, the following word cloud clustered marriage announcements:
![alt text](https://github.com/supermikol/DS_Projects/raw/master/03_nytimes_unsupervised_NLP/imgs/topic9_marriages.png "Marriage Announcements")

However, for the most part, most clusters produced very obvious topics:

Middle East War:

![alt text](https://github.com/supermikol/DS_Projects/raw/master/03_nytimes_unsupervised_NLP/imgs/topic1.png "Middle East")

Climate & Energy:

![alt text](https://github.com/supermikol/DS_Projects/raw/master/03_nytimes_unsupervised_NLP/imgs/topic3_climateEnergy.png "Climate and Energy")

Finance:

![alt text](https://github.com/supermikol/DS_Projects/raw/master/03_nytimes_unsupervised_NLP/imgs/topic5_finance.png "Finance")

Baseball:

![alt text](https://github.com/supermikol/DS_Projects/raw/master/03_nytimes_unsupervised_NLP/imgs/topic7_baseball.png "Baseball")

Finally, I took the percentage weights of how each topic varied across the years:

![alt text](https://github.com/supermikol/DS_Projects/raw/master/03_nytimes_unsupervised_NLP/imgs/topic_graph.png "Topic Weights")

Note how the sports coverage started with an incline, and peaked in 2014, followed by a steep drop, whereas global politics took a sudden spike in 2016, which correspond with the presidential election and the ensuring uptick in coverage that followed.

In general I thought this graph was rather interesting and can be used to monitor aggregate trends that the media is paying attention to.


