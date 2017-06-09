import pandas as pd
import numpy as np

from sklearn import ensemble as ens
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

stats = pd.read_csv('../data/clustered_stats.csv')

# create player-type distribution dataframe!
teams = list(stats['tm'].unique())
team_dists = pd.DataFrame(columns=range(0,13),index=teams)

for team in teams:
    team_dists.loc[team] = stats[stats['tm'] == team]['labels'].value_counts().to_dict()

team_dists.fillna(value=0,inplace=True)
team_dists.drop('TOT',axis=0,inplace=True)
team_dists.sort_index(inplace=True)

# I should've considered this before, but at this point the easiest way to create a target column is to simply do it manually.  Here's season wins for each team,alphabetically:

wins = np.array([43,53,20,41,36,51,33,40,37,67,55,42,51,26,43,41,42,31,34,31,47,29,28,24,41,32,61,51,51,49])

# First go at a model

X = team_dists
y = wins
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

forest = ens.RandomForestRegressor(n_estimators=1000)
# forest.fit(X_train,y_train)
# print "Feature Importances: {}".format(zip(range(0,13),forest.feature_importances_))
# print "R-squared Score: {}".format(forest.score(X_test,y_test))

# This yielded wildly variant R-squared scores, including a few negative!  Tough to tease out a pattern with such scant data, but let's carry on...

adaboost = ens.AdaBoostRegressor(base_estimator=DecisionTreeRegressor(),n_estimators=10000,learning_rate=.5,loss='square')
adaboost.fit(X_train,y_train)
print "Feature Importances: {}".format(zip(range(0,13),adaboost.feature_importances_))
print "R-squared Score: {}".format(adaboost.score(X_test,y_test))
