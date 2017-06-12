import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from create_player_dict import get_bbref

from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF

stats_list = ['MP_x','3PAr','FTr','ORB%','DRB%','AST%','STL%','BLK%','TOV%','USG%','3P%','FT%','2P%','2P','2PA','3P','3PA','FT','FTA','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','eFG%','TS%_x','TRB%','ORtg','DRtg']

stats2016 = get_bbref(2016)
tm2016 = stats2016.pop('Tm_x')
X = stats2016[stats_list]
X.fillna(value=0,inplace=True)

scaled2016 = normalize(X)

U,sigma,VT = np.linalg.svd(scaled2016)

plt.plot((sigma ** 2)[:20])
plt.title('SVD')
plt.xlabel('# Features')
plt.ylabel('Power')
plt.savefig('../img/svd.png')
plt.close()

plt.plot(np.cumsum(sigma ** 2))
plt.savefig('../img/cumulative_power.png')
plt.close()

total_energy = np.sum(sigma ** 2)
# print "90\% of energy = {}".format(total_energy * 0.9)

# We can retain 90% power with roughly 9 singular values
V_9 = VT[:9,:]
U_9 = U[:9,:]
#---------let's look at NMF-------------#
x = []
y = []
comp_range = range(5,21)
for comp in comp_range:
    nmf = NMF(n_components=comp,max_iter=100,random_state=23,alpha=0.1)
    nmf.fit(scaled2016)
    print "Number of components: {} |  Reconstruction Error: {}".format(comp,nmf.reconstruction_err_)
    x.append(comp)
    y.append(nmf.reconstruction_err_)
plt.plot(x,y)
plt.xlabel('Number of Components')
plt.ylabel('Reconstruction Error')
plt.title('NMF Elbow Plot')
plt.savefig('../img/nmfelbow.png')
