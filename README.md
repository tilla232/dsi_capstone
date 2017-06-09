  
# A Winning Formula    

## Table of Contents  
1. [Abstract](#abstract)  
2. [Data](#data)  
3. [Model](#model)
    * [Clustering](#clustering)
    

  
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
![basketball reference](https://github.com/tilla232/dsi_capstone/blob/master/img/Screen%20Shot%202017-06-08%20at%2011.51.07%20AM.png?raw=true)  

As you can see, the site makes it incredibly easy to pull common stats for every player in a given season, but it also makes equally as easy to find the more advanced stats - those that lend a bit more insight into how a player actually spends his time on the floor.
   
## Model  
### Clustering
Clustering is a messy matter to begin with, and was only further complicated, in this study, by the cluster overlap we would almost inherently find, regardless of model selection and parameter tuning.  Our model is built around NBA players, almost none of whom are abjectly *terrible* at any one aspect of the game.  We would expect players from cluster 1 to be at least serviceable when it comes to the skills that players from cluster 2 thrive at, etc.  This fact alone made it hard to quantify success in our clustering, as we would almost expect something like mean silhouette score to have a fairly low cap.  
  
Nevertheless, I was at least able to use silhouette score on a simple K-Means algorithm to choose a suitable number of clusters at k = 13 - shout out to Mr. Alagappan - and a manual inspection of the clusters confirmed that I was on the right track.  One cluster - which I would call 'play-making big men' - contained players like Marc Gasol, Nikola Jokic, Giannis Antetokounmpo, and DeMarcus Cousins.  While these players do have some marked differences from one to the next (Gasol and Jokic, for example, could be considered insanely *un*athletic next to the other two), they definitely occupy the same milieu on the court: their team's offenses tend to run through them, and they are notably great passers for their size.  Another cluster, 'true centers', contains players like Bismack Biyombo, Dwight Howard, Hassan Whiteside, and Rudy Gobert.  These are players who have a huge defensive impact both in rim protection and rebounding, and not much of an offensive game outside of 6 feet from the basket.  

While these clusters made sense to me, I wanted to quantify them *somehow*, for the sake of both science as well as sanity-checking...I obtained simple numerical data (mean and range) for each feature, for each cluster - this also proved useful in *qualifying* each cluster, as it becamse immediately apparent what skills each cluster exemplified.

