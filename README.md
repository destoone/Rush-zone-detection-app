# Rush-zone-detection-app
The rush zone detection application is an application that gives you the possibility to see how the odds trend varies in order to determine where the rushes are in sports betting. Then trains models to predict the odds. 

### App structure
`Used dependencies & technologies:` We have an application entirely coded in python, so we will need to install [python](https://www.python.org/downloads/) as well as some libraries like [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/). We will use the Dash framework, which you can find [here](https://dash.plotly.com/dash-enterprise), or a [tutorial](https://dash.plotly.com/installation) that allows you to take the basics of the framework. So Dash is a python framework dedicated to the developers of machine learning applications. Dash uses [Flask](https://flask.palletsprojects.com/en/2.0.x/) behind it which will allow us to use the necessary web components for our web application. 
So we will make a separate treatment, a treatment that will allow us to make our analysis, our visualizations and our predictions. To do this we will use [scikit-learn](https://scikit-learn.org/stable/) and a notebook as editor.

### Introduction 
`The goal:` Here the goal is to determine the rush zones, what we call by rush is what represents the highest odds for each game. We will use a database of Premier League between 2010 and 2018. So we will start by presenting the Premier League, the different teams.

![](https://github.com/destoone/Rush-zone-detection-app/blob/main/rush_1.JPG)

We will also have the possibility to see the information about the different teams, there are four terminals that represent the different online platforms where bets are made. So we have B365, IW, LB and WH, so we will navigate through the different terminals. 

![](https://github.com/destoone/Rush-zone-detection-app/blob/main/rush_2.JPG)

Now we will move to the visualization of our data, we start by seeing the current values of our odds. And respectively for all our terminals.

![](https://github.com/destoone/Rush-zone-detection-app/blob/main/rush_3.JPG)

And as said above, after processing and choosing our variables as well as our models, predictions are made on our odds.

Then in order to better understand our graphs we have put filters on the years and months.

![](https://github.com/destoone/Rush-zone-detection-app/blob/main/rush_4.JPG)

Finally you will find the code [here](https://github.com/destoone/Rush-zone-detection-app/blob/main/final_project.py), after completion you can test the application on the address http://127.0.0.1:8050/


Thanks and enjoy it 😉
