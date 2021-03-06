  
# A Winning Formula    

## Table of Contents  
1. [Abstract](#abstract)  
2. [Data](#data)  
3. [Model](#model)
    * [Clustering](#clustering)
    * [Regression](#regression)
    

  
## Abstract

There’s long been a simmering belief that basketball’s traditional positional labels
(point guard, shooting guard, small forward, power forward, center) are insufficient in
fully describing a player’s role and activity on the court. Today, more than ever, the
issue is bubbling over, and we see players like Giannis Antetokounmpo, Nikola Jokic, et
al. bending the rules ascribed to players of their position by traditionalists - we need to
adapt our viewing/analyzing paradigms accordingly. [Muthu Alagappan famously made
an effort to reposition NBA players at Sloan 2012](http://www.sloansportsconference.com/wp-content/uploads/2012/03/Alagappan-Muthu-EOSMarch2012PPT.pdf), but his analysis falls short for me.
The main issue I find is that a number of his positions fail to impart any sense of how
the players of that position actually play on the floor, the most egregious among them,
‘role players’, being a position comprised of roughly the same number of players as
about *five* other positions combined. In all, a rough visual estimate tells me that, in this
analysis, roughly one-third of all NBA players wind up in this ‘role player’ position; this
is problematic, to say the least.
My aim in this study is two-fold: the first section is concerned with defining better
positions, while the second will use these positions to determine if there is an ideal
distribution of player-types on a team.
  
  
## Data
  
Data was pulled from [Basketball Reference](http://basketball-reference.com) - the site has a handy 'Get Table as CSV' option which made pulling/using this data a snap: 
![basketball reference](https://github.com/tilla232/dsi_capstone/blob/master/img/bbref.png?raw=true)  

The site makes it incredibly easy not only to pull common counting stats for every player in a given season, but also to find the more advanced stats - those that lend a bit more insight into how a player actually spends his time on the floor.
   
## Model  
### Clustering
Clustering is a messy matter to begin with, and was only further complicated, in this study, by the cluster overlap we would almost inherently find, regardless of model selection and parameter tuning.  Our model is built around NBA players, almost none of whom are abjectly *terrible* at any one aspect of the game.  We would expect players from cluster 1 to be at least serviceable when it comes to the skills that players from cluster 2 thrive at, etc.  This fact alone made it hard to quantify success in our clustering, as we would almost expect something like mean silhouette score to have a fairly low cap. 

I was initially using roughly 20 features to cluster upon, and decided some dimensionality reduction could help improve my model's performance.  After some tinkering with sklearn's PCA class, I quickly realized that a dramatic reduction in dimension (n_components = 2) was drastically boosting my silhouette scores, but producing a set of clusters where some made perfect sense, but others were...hard to explain, from a basketball standpoint.   
![cluster snippet](https://github.com/tilla232/dsi_capstone/blob/master/img/cluster_snippet.png?raw=true)  
  
 
I suspected that such intense dimension reduction was making my clustering model cluster based on overall contribution - in a sense, the PCA was effectively calculating an overall performance metric (stats like VORP, WS, BPM, etc.) on the fly; this was decidedly *not* what I was trying to accomplish.  
  
  
~~While these clusters made sense to me, I wanted to quantify them *somehow*, for the sake of both science as well as sanity-checking...I obtained simple numerical data (mean and range) for each feature, for each cluster - this also proved useful in *qualifying* each cluster, as it becamse immediately apparent what skills each cluster exemplified.~~

### Regression
My first attempt at regression was a simple Random Forest model - I knew my data was both sparse and scant, so I set the number of trees to 1000 - as computation time definitely wouldn't be a limiting factor - in hopes of increasing the efficacy of the model.  Running the model a few times quickly revealed that a simple regression model like this would be totally fruitless.  Not only were R-squared results all over the place, but a number of them actually came up negative -- this was somewhat anticipated:
![distribution snippet](https://github.com/tilla232/dsi_capstone/blob/master/img/team_dists.png?raw=true)   
If you try to regress on data like this...you're gonna have a bad time!

My plan to remedy this is to transform data from the previous 3 seasons with my same clustering model (ie, use the same model to label each player-season, dating back to 2013-14), and simply add the resulting player-type distributions on top of the 2016 data, and the total wins on top of the 2016 wins.  This method obviously carries the pretty major assumption that players from each of the last 3 seasons readily fit into the categories I defined with the 2016 data.  As a fan, I can readily justify this by simply noting that the game hasn't changed dramatically in the last 4 seasons...as a data scientist, I need to quantify this assertion at least *a little*.  If this method doesn't prove viable, I can recreate my clustering model using aggregate player-stats over that same period (regardless of team), and create my player-type distribution data using the same methods.  

