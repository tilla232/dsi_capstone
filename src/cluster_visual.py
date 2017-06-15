import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from agglomerative import get_data

from sklearn.manifold import TSNE
from sklearn import feature_selection as fs
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, Birch
from sklearn.metrics import silhouette_score

def plot_tsne_scatter(X,filename=None,three_d=False,title=None):
    '''
    Arguments:
    Feature matrix X, a dataframe or array of numerical data.

    Output:
    None, plots 2d-projection of higher-dimensional data, saves figure to img directory.
    '''
    tsne2d = TSNE(n_components=2,init='pca',random_state=23).fit_transform(X)
    tsne3d = TSNE(n_components=3,init='pca',random_state=23).fit_transform(X)


    fig = plt.figure(figsize=(6,4))
    ax1 = fig.add_subplot(111)
    ax1.scatter(tsne2d[:,0],tsne2d[:,1],cmap=plt.cm.Spectral)
    ax1.set_title(title)
    plt.axis('tight')
    if not filename:
        plt.savefig('../img/2dtsne.png')
    else:
        plt.savefig('../img/2dtsne_{}.png'.format(filename))

    if three_d:
        ax2 = fig.add_subplot(111,projection='3d')
        ax2.scatter(tsne3d[:,0],tsne3d[:,1],tsne3d[:,2],cmap=plt.cm.Spectral)
        ax2.set_title(title)
        plt.axis('tight')
        if not filename:
            plt.savefig('../img/3dtsne.png')
        else:
            plt.savefig('../img/3dtsne_{}.png'.format(filename))

if __name__=='__main__':
    stats_list = ['FG','FGA','2P','2PA','3P','3PA','FT','FTA','ORB', 'DRB', 'TRB', 'AST', 'STL','BLK','TOV','PF','PTS','FG%','2P%','3P%', 'eFG%', 'FT%', 'TS%_x', 'PER', '3PAr','FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%','ORtg', 'DRtg', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM','VORP', 'dist', 'spd', 'tchs', 'pass', 'sast', 'ftast', 'dfgm','dfga']

    df = pd.read_csv('../data/final_stats.csv')

    # X,tm = get_data(df,stats_list)

    # plot_tsne_scatter(X)
    # we see...nothing resembling discernible clusters - let's try some feature reduction
    # t_list = np.linspace(0.2,0.99,20)[::-1]
    # for t in t_list:
    #     try:
    #         variance = fs.VarianceThreshold(threshold=t)
    #         break
    #     except ValueError:
    #         continue
    # X = variance.fit_transform(X)
    # X = normalize(X)
    #
    # # plot_tsne_scatter(X,filename='var_threshold')
    # idx = variance.get_support(indices=True)
    # new_stats_list = [stats_list[idx[i]] for i,_ in enumerate(idx)]
    new_stats_list = ['2P','2PA','3P','3PA','FT','FTA','ORB','DRB','AST','STL','BLK','dist','tchs','pass','sast','ftast','dfgm','dfga']
    #,'ORB%','DRB%','AST%','STL%','BLK%','USG%'
    X,tm = get_data(df,new_stats_list)
    X = normalize(X)
    plot_tsne_scatter(X,filename='reduced2')
    #
    # # let's try it with PCA
    # for n in range(2,10):
    #     pca = PCA(n_components=n,random_state=23,svd_solver='full')
    #     pca.fit(X)
    #     components = pca.components_.T
    #     if n == 2:
    #         plt.figure(figsize=(6,4))
    #         plt.scatter(components[:,0],components[:,1])
    #         plt.title('With PCA, 2 components')
    #         plt.savefig('../img/reducedPCA2components.png')
    #     else:
    #         plot_tsne_scatter(components,filename='reducedPCA{}components'.format(n),title='With PCA, {} components'.format(n))

    # Let's try clustering on 5 positions, then running those results through a different clustering mechanism...
    # km = KMeans(n_clusters=5,max_iter=500,n_init=50,algorithm='full',precompute_distances=True,verbose=2)
    # km.fit(X)
    #
    # # df['label'] = km.labels_
    # # stats_list.append('label')
    # np.append(X,km.labels_)
    #
    # birch = Birch(n_clusters=13)
    # birch.fit(X)
    # df['new_label'] = birch.labels_
