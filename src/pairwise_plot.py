import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

X = pd.read_csv('../data/clustered_feature_space.csv').set_index('player_year')

plot = sns.pairplot(X,hue='label',diag_kind='kde',kind='reg')
plt.show()
