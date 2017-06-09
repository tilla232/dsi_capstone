import pandas as pd
import numpy as np

from create_player_dict import get_bbref

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

km = KMeans(n_clusters=13,n_init=50,max_iter=1000,algorithm='full',random_state=23)

pca = PCA(n_components=2,svd_solver='auto')
# In [3]: run k_means.py
# Out [3]:
# 2016: 0.358362946988
# 2015: 0.29260287844

# In [12]: list(stats2016[stats2016['labels'] == 10].index)
# Out[13]: ['DeAndre Jordan', 'Dwight Howard', 'Rudy Gobert']

stats_list = ['MP_x','3PAr','FTr','ORB%','DRB%','AST%','STL%','BLK%','TOV%','USG%','WS/48','3P%','FT%','2P%']

stats2016 = get_bbref(2016)
stats2015 = get_bbref(2015)

df_dict = {2015:stats2015,2016:stats2016}

# pop team column out for purposes of scaling/analysis, and later reattachment
tm2016 = stats2016.pop('Tm_x')
tm2015 = stats2015.pop('Tm_x')

# set data using stats_list
X_2016 = stats2016[stats_list]
X_2015 = stats2015[stats_list]

X_2016.fillna(value=0,inplace=True)
X_2015.fillna(value=0,inplace=True)

# standard scale
scaler = StandardScaler()
scaled2016 = scaler.fit_transform(X_2016)
scaled2015 = scaler.transform(X_2015)


# perform dimension reduction
reduced_2016 = pca.fit_transform(scaled2016)
reduced_2015 = pca.fit_transform(scaled2015)

# fit the model to reduced, scaled 2016 data
km.fit(reduced_2016)

# reattach tm column, attach labels
stats2016['Tm'] = tm2016
stats2016['labels'] = km.labels_

stats2015['Tm'] = tm2015
stats2015['labels'] = km.predict(reduced_2015)

# calculate means for each stat for each cluster
def get_cluster_means(year):
    stats = df_dict[year]
    cluster_nums = {}
    for label in range(0,13):
        cluster = stats[stats['labels'] == label]
        cluster.drop('labels',axis=1,inplace=True)
        means_dict = cluster.describe().loc['mean'].to_dict()
        means_dict = {k:round(v,4) for k,v in means_dict.items()}
        cluster_nums[label] = means_dict
    return cluster_nums

cluster_stats_2015 = get_cluster_means(2015)
cluster_stats_2016 = get_cluster_means(2016)

print "2016: {}".format(silhouette_score(reduced_2016,km.labels_))
print "2015: {}".format(silhouette_score(reduced_2015,km.predict(reduced_2015)))

# stats.to_csv('../data/clustered_stats.csv')
