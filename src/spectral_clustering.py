import pandas as pd
import numpy as np
import timeit

import matplotlib.pyplot as plt

from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score

def get_data(df,stats_list):
    '''
    Takes in final stats dataframe and stats list in format of the list seen in the main block below, outputs normalized data (X) - also outputs team column (tm) for future reattachment
    '''
    df.set_index('player_year',inplace=True)
    tm = df.pop('Tm_x')

    df = df[stats_list]

    # one column (3Par) has a few nans - it makes sense to simply convert these to 0's
    df.fillna(value=0,inplace=True)

    X = normalize(df)
    return X,tm

def print_silhouette_scores(X,cluster_list,gamma_list):
    print ('n | g')
    for n in cluster_list:
        for g in gamma_list:
            spectral = SpectralClustering(n_clusters=n,gamma=g,n_init=1000,n_jobs=2)
            spectral.fit(X)
            print ('{} | {}    |   {}'.format(n,g,silhouette_score(X,spectral.labels_)))
def plot_silhouette_scores(X,cluster_list):
    '''
    Takes fit model and range of number of clusters and plots silhouette score of each number of clusters, saves plots in img folder
    '''
    x,y = [],[]
    for n in cluster_list:
        spectral = SpectralClustering(n_clusters=n,n_init=1000,n_jobs=2)
        spectral.fit(X)
        x.append[n],y.append[silhouette_score(X,spectral.labels_)]
    plt.plot(x,y)
    plt.xlabel('N Clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Spectral Clustering with Discretization for Label Assignment')
    plt.savefig('../img/spectral_silhouettes.png')
    plt.close()




if __name__ == '__main__':
    # Initialization Options
    stats_list = ['3PAr','FTr','AST%','STL%','BLK%','USG%','3P%','2P','2PA','3P','3PA','FT','FTA','ORB','ORB%','DRB','DRB%','AST','STL','BLK','dist','spd','tchs','pass','sast','ftast','dfgm','dfga']

    df = pd.read_csv('../data/final_stats.csv')
    cluster_list = range(5,21)
    gamma_list = np.linspace(0.01,1,5)

    X,tm = get_data(df,stats_list)
    print_silhouette_scores(X,stats_list,gamma_list)
