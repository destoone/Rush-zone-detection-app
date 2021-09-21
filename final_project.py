# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 04:11:47 2021

@author: destine
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

## loading bootstrap
external_stylesheets= [dbc.themes.BOOTSTRAP]

## create app
app= dash.Dash(__name__,external_stylesheets= external_stylesheets) 

## read data
df= pd.read_csv("odds_reduced_.csv")
clubs= df["HomeTeam"].unique()

## indicator graph
fig_indic = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 40,
    delta = {'reference': 40},
    title = {'text': "Total club"}
    ))

## Create table for informations
table_header = [
    html.Thead(html.Tr([html.Th("Informations on the club")]))
]
row1 = html.Tr([html.Td("Club"),html.Td(id="info-club")])
row2 = html.Tr([html.Td("City"),html.Td(id="info-city")])
row3 = html.Tr([html.Td("Country"),html.Td(id="info-country")])
row4 = html.Tr([html.Td("Number home game"),html.Td(id="info-ht")])
row5 = html.Tr([html.Td("Number away game"),html.Td(id="info-at")])
table_body = [html.Tbody([row1, row2, row3, row4,row5])]
table= dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True, responsive=True)

## Months list
months_name= ["Jan","Feb","Mars","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
year_list= [2010,2011,2012,2013,2014,2015,2016,2017,2018]

app.layout= html.Div(
            [
                html.Div(
                        [html.H2("Rush zones detection")],style={"color":"Blue","text-align":"center"}
                        ),
                html.Br(),
                html.Div([html.Img(src="https://cdn.1min30.com/wp-content/uploads/2017/07/Premier-League-1.jpg",alt="Premier league image"),
                        dbc.Card("This app provide elements who permit you to understand better the premier league between the 2010 and 2018 season, it predict also the odds in order to figure out rush zones while bettings", body=True)
                ],style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),
                html.Div([table],style={'width': '40%', 'float': 'center', 'display': 'inline-block'}),
                html.Div([html.P("clubs in England\'s Premier League"),
                        dcc.Dropdown(
                                id='unique-club-column',
                                options=[{'label': i, 'value': i} for i in clubs],
                                value='clubs in England\'s Premier League'
                                ),
                        dcc.Graph(figure=fig_indic)
                        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div(
                            dcc.Tabs(id='tabs-column', value='tab-1', children=[
                            dcc.Tab(label='B365', value='tab-1'),
                            dcc.Tab(label='IW', value='tab-2'),
                            dcc.Tab(label='LB', value='tab-3'),
                            dcc.Tab(label='WH', value='tab-4'),
                            ])
                        ),
                html.Div(html.Div(dcc.Graph(id="graph-current"),style={"width":"70%","float":"left"})),
                html.Div(html.Div(dcc.Graph(id="graph-predict"),style={"width":"70%","float":"right"})),
                html.Div(dcc.Slider(
                    id='crossfilter-year--slider',
                    min=df['years'].min(),
                    max=df['years'].max(),
                    value=df['years'].max(),
                    marks={str(years): str(years) for years in df['years'].unique()},
                    step=None
                    )
                    , style={'width': '49%', 'padding': '0px 20px 20px 20px',"float":"left"}),
                html.Div(
                        dcc.Slider(
                    id='crossfilter-month--slider',
                    min=df['months'].min(),
                    max=df['months'].max(),
                    value=df['months'].max(),
                    marks={str(months_num): months_name[months_num-1] for months_num in df['months'].unique()},
                    step=None
                    )
                    ,style={'width': '49%', 'padding': '0px 20px 20px 20px',"float":"right"}
                    )
            ]
        )

@app.callback(
        Output("info-club","children"),
        Output("info-city","children"),
        Output("info-country","children"),
        Output("info-ht","children"),
        Output("info-at","children"),
        Input("unique-club-column","value")
        )
def update_info(unique_club_column):
    club= "".join(df.loc[df["HomeTeam"]==unique_club_column].head(1)["HomeTeam"].values)
    city= "".join(df.loc[df["HomeTeam"]==unique_club_column].head(1)["ville"].values)
    country= ""
    if len(club)!=0:
        country= "England"
    number_ht= "".join(df.loc[df["HomeTeam"]==unique_club_column].head(1)["number_ht"].values.astype("str"))
    number_at= "".join(df.loc[df["AwayTeam"]==unique_club_column].head(1)["number_at"].values.astype("str"))
    return club,city,country,number_ht,number_at

@app.callback(
        Output("graph-current","figure"),
        Output("graph-predict","figure"),
        Input("tabs-column","value"),
        Input("crossfilter-year--slider","value"),
        Input("crossfilter-month--slider","value")
        )
def update_tabs(tabs_column,year_slider,month_slider):
    df_year= df.loc[df["years"]==year_slider]
    df_month= df_year.loc[df_year["months"]==int(month_slider)]
    if tabs_column=="tab-1": 
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["B365H"].values,
                            mode='lines+markers',
                            name='B365 Home win odds',line=dict(color='#0023F6', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["B365D"].values,
                            mode='lines+markers',
                            name='B365 Draw odds',line=dict(color='#0CA0EB', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["B365A"].values,
                            mode='lines+markers', name='B365 away win odds',line=dict(color='#00F6C3', width=3)))
        fig1.update_layout(title='Odds current values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_B365H"].values,
                            mode='lines+markers',
                            name='B365 Home win odds',line=dict(color='#9C0D13', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_B365D"].values,
                            mode='lines+markers',
                            name='B365 Draw odds',line=dict(color='#FF2500', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_B365A"].values,
                            mode='lines+markers', name='B365 away win odds',line=dict(color='#FF0D13', width=3)))
        fig2.update_layout(title='Odds predicted values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
        
    if tabs_column=="tab-2":
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["IWH"].values,
                            mode='lines+markers',
                            name='IW Home win odds',line=dict(color='#0023F6', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["IWD"].values,
                            mode='lines+markers',
                            name='IW Draw odds',line=dict(color='#0CA0EB', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["IWA"].values,
                            mode='lines+markers', name='IW away win odds',line=dict(color='#00F6C3', width=3)))
        fig1.update_layout(title='Odds current values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_IWH"].values,
                            mode='lines+markers',
                            name='IW Home win odds',line=dict(color='#9C0D13', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_IWD"].values,
                            mode='lines+markers',
                            name='IW Draw odds',line=dict(color='#FF2500', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_IWA"].values,
                            mode='lines+markers', name='IW away win odds',line=dict(color='#FF0D13', width=3)))
        fig2.update_layout(title='Odds predicted values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
    if tabs_column=="tab-3":
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["LBH"].values,
                            mode='lines+markers',
                            name='LB Home win odds',line=dict(color='#0023F6', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["LBD"].values,
                            mode='lines+markers',
                            name='LB Draw odds',line=dict(color='#0CA0EB', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["LBA"].values,
                            mode='lines+markers', name='LB away win odds',line=dict(color='#00F6C3', width=3)))
        fig1.update_layout(title='Odds current values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_LBH"].values,
                            mode='lines+markers',
                            name='LB Home win odds',line=dict(color='#9C0D13', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_LBD"].values,
                            mode='lines+markers',
                            name='LB Draw odds',line=dict(color='#FF2500', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_LBA"].values,
                            mode='lines+markers', name='LB away win odds',line=dict(color='#FF0D13', width=3)))
        fig2.update_layout(title='Odds predicted values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
    if tabs_column=="tab-4":
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["WHH"].values,
                            mode='lines+markers',
                            name='WH Home win odds',line=dict(color='#0023F6', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["WHD"].values,
                            mode='lines+markers',
                            name='WH Draw odds',line=dict(color='#0CA0EB', width=3)))
        fig1.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["WHA"].values,
                            mode='lines+markers', name='WH away win odds',line=dict(color='#00F6C3', width=3)))
        fig1.update_layout(title='Odds current values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_WHH"].values,
                            mode='lines+markers',
                            name='WH Home win odds',line=dict(color='#9C0D13', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_WHD"].values,
                            mode='lines+markers',
                            name='WH Draw odds',line=dict(color='#FF2500', width=3)))
        fig2.add_trace(go.Scatter(x=[float(i) for i in range(df_month.shape[0])],
                                  y=df_month["prediction_WHA"].values,
                            mode='lines+markers', name='WH away win odds',line=dict(color='#FF0D13', width=3)))
        fig2.update_layout(title='Odds predicted values',
                   xaxis_title='Odds number',
                   yaxis_title='odds values')
    return fig1,fig2


if __name__=="__main__":
    app.run_server(debug=True)