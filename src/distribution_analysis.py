import pandas as pd
import numpy as np
import string
import operator

from sklearn import ensemble as ens
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV

# create player-type distribution dataframe!
def create_distribution(stats,team_wins):
    # create team_year column, in stats, create team_dists df with team seasons as index
    stats['team_year'] = stats['Tm'].map(str) + '/' + stats['Season_x'].map(str)
    teams = list(stats['team_year'].unique())
    team_dists = pd.DataFrame(columns=range(0,13),index=teams)

    # perform similar operation on team_wins
    team_wins['team_year'] = team_wins['Tm'].apply(lambda x: str(x).translate(None,string.punctuation)).map(str) + '/' + team_wins['Season'].map(str)
    team_wins.set_index('team_year',inplace=True)

    for team_year in teams:
        tm_stats = stats[stats['team_year'] == team_year]
        grouped = tm_stats.groupby('label').sum()
        cluster_minutes_dict = {}
        for i in grouped.index:
            cluster_minutes_dict[i] = grouped.loc[i]['MP_x']

        team_dists.loc[team_year] = cluster_minutes_dict

    team_dists.fillna(value=0,inplace=True)
    team_dists.sort_index(inplace=True)
    team_dists = team_dists[team_dists.index.str.contains("TOT") == False]

    #
    # merge distributions and wins
    team_dists = pd.merge(team_dists,team_wins,left_index=True,right_index=True)

    # drop extraneous columns
    team_dists.drop(['Season'],axis=1,inplace=True)
    team_dists.drop(['Tm'],axis=1,inplace=True)

    return team_dists

# This yielded wildly variant R-squared scores, including a few negative!  Tough to tease out a pattern with such scant data, but let's carry on...


if __name__ == '__main__':
    df = pd.read_csv('../data/clustered_stats.csv')
    team_wins = pd.read_csv('../data/team_wins.csv')

    team_dists = create_distribution(df,team_wins)
    # First go at a model

    targets = [u'W/L%',u'MOV',u'SOS',u'SRS',u'Pace',u'ORtg',u'DRtg', u'eFG%',u'TOV%',u'ORB%',u'FT/FGA',u'eFG%.1',u'TOV%.1',u'ORB%.1', u'FT/FGA.1']

    y = team_dists.pop('W/L%')
    X = team_dists.iloc[:,:13]
    for _ in range(20):
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    #
    #
    #     forest = ens.RandomForestRegressor(n_estimators=1000)
    #     forest.fit(X_train,y_train)
    #
        extra = ens.ExtraTreesRegressor(n_estimators=500,max_features='auto',bootstrap=False,criterion='mae',max_depth=5)
        extra.fit(X_train,y_train)
    #
    #     gb = ens.GradientBoostingRegressor(n_estimators=1000)
    #     gb.fit(X_train,y_train)
    #
    #     feat = zip(range(0,13),forest.feature_importances_)
    #     feat.sort(key=lambda x:x[1])
    #     print 'Random Forest:'
    #     print 'Test: {}   |   {}'.format(_,forest.score(X_test,y_test))
    #     print 'Train: {}   |   {}'.format(_,forest.score(X_train,y_train))
    #     print '---------'
        print 'Extremely Randomized Trees:'
        print 'Test: {}   |   {}'.format(_,extra.score(X_test,y_test))
        print 'Train: {}   |   {}'.format(_,extra.score(X_train,y_train))
        print '---------'
    #     print 'Gradient Tree Boosting'
    #     print 'Test: {}   |   {}'.format(_,gb.score(X_test,y_test))
    #     print 'Train: {}   |   {}'.format(_,gb.score(X_train,y_train))
    #     print '---------'


    extreme_grid = {'n_estimators':[500,1000,1500],
                    'criterion':['mse','mae'],
                    'max_features':['auto','sqrt','log2'],
                    'max_depth': [5,10,15],
                    'bootstrap': [True,False],
    }
    extreme_grid_search = GridSearchCV(ens.ExtraTreesRegressor(),
                                       extreme_grid,
                                       n_jobs=-1,
                                       verbose=True,
                                       )
    extreme_grid_search.fit(X_train,y_train)
    print 'Best Params: {}'.format(extreme_grid_search.best_params_)
    # print "Feature Importances: {}".format(feat)
    # print "R-squared Score: {}".format(forest.score(X_test,y_test))
    # print "The three most important features are {}".format([x[0] for x in feat[::-1][:3]])
