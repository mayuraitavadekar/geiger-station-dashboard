from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask
from datetime import datetime, timedelta

# turn off cavets warnings of pandas:
pd.options.mode.chained_assignment = None #default='warn'

# get context from core Dash
app = Dash(__name__)

server = app.server

# set page title
app.title="Geiger Station 1"

# function to server the plots
def serve_plots():
	
	# read the data from csv file
	df = pd.read_csv('./static/data-v1.csv', index_col="timestamp", parse_dates=True)

	# df.timestamp = pd.to_datetime(df.timestamp)
	# df.set_index('timestamp', inplace=True)

	# create new dataframe with %change on each feature
	# pct_change_df = df.pct_change() # get the percent change; calculation over each row in all cols
	# get the last 60 rows
	# pct_change_last_hour = pct_change_df.tail(60)
	
	main_df = df.resample('H').sum()
	main_df.drop(main_df.head(1).index,inplace=True)
	main_df.drop(main_df.tail(1).index,inplace=True)
	
	now = main_df.reset_index()['timestamp'].iloc[-1].date()
	yesterday = main_df.reset_index()['timestamp'].iloc[-1].date() - timedelta(days=1)
	lastmonth = main_df.reset_index()['timestamp'].iloc[-1].date() - timedelta(days=31)
	
	one_day_df = main_df.loc[yesterday:now]
	one_month_df = main_df.loc[lastmonth:now]
	
	# calculate % change on maindf
	main_df["gc_pct"] = ((main_df['GC'] - main_df['GC'].mean())/main_df['GC'].mean())*100
	main_df["hum_pct"] = ((main_df['humidity'] - main_df['humidity'].mean())/main_df['humidity'].mean())*100
	main_df["temp_pct"] = ((main_df['temperature'] - main_df['temperature'].mean())/main_df['temperature'].mean())*100
	main_df["hi_pct"] = ((main_df['heat-index'] - main_df['heat-index'].mean())/main_df['heat-index'].mean())*100
	main_df['temp_pct_scaled'] = 0.1*main_df['temp_pct']
	main_df['hum_pct_scaled'] = 0.1*main_df['hum_pct']
	main_df['gc_m_avg'] = 0.1*main_df.rolling('6H').gc_pct.mean()

	# calculate % change on oneday_df
	one_day_df["gc_pct"] = ((one_day_df['GC'] - one_day_df['GC'].mean())/one_day_df['GC'].mean())*100
	one_day_df["hum_pct"] = ((one_day_df['humidity'] - one_day_df['humidity'].mean())/one_day_df['humidity'].mean())*100
	one_day_df["temp_pct"] = ((one_day_df['temperature'] - one_day_df['temperature'].mean())/one_day_df['temperature'].mean())*100
	one_day_df["hi_pct"] = ((one_day_df['heat-index'] - one_day_df['heat-index'].mean())/one_day_df['heat-index'].mean())*100
	one_day_df['temp_pct_scaled'] = 0.1*one_day_df['temp_pct']
	one_day_df['hum_pct_scaled'] = 0.1*one_day_df['hum_pct']
	one_day_df["gc_m_avg"] = one_day_df.rolling('6H').gc_pct.mean()


	# calculate % change on lastmonth_df
	one_month_df["gc_pct"] = ((one_month_df['GC'] - one_month_df['GC'].mean())/one_month_df['GC'].mean())*100
	one_month_df["hum_pct"] = ((one_month_df['humidity'] - one_month_df['humidity'].mean())/one_month_df['humidity'].mean())*100
	one_month_df["temp_pct"] = ((one_month_df['temperature'] - one_month_df['temperature'].mean())/one_month_df['temperature'].mean())*100
	one_month_df["hi_pct"] = ((one_month_df['heat-index'] - one_month_df['heat-index'].mean())/one_month_df['heat-index'].mean())*100
	one_month_df['temp_pct_scaled'] = 0.1*one_month_df['temp_pct']
	one_month_df['hum_pct_scaled'] = 0.1*one_month_df['hum_pct']
	one_month_df["gc_m_avg"] = one_month_df.rolling('6H').gc_pct.mean()
	
	one_day_df = one_day_df.reset_index()
	one_month_df = one_month_df.reset_index()
	main_df = main_df.reset_index()
		
	# plot graph0
	# minute_df = df.copy()

	# minute_df_gc_mean = minute_df.GC.mean()
	# minute_df_temp_mean = minute_df.temperature.mean()
	# minute_df_hum_mean = minute_df.humidity.mean()


	# minute_df["gc_pct_change"] = ((minute_df.GC - minute_df_gc_mean)/minute_df_gc_mean)
	# minute_df["temp_pct_change"] = ((minute_df.temperature - minute_df_temp_mean)/minute_df_temp_mean)
	# minute_df["hum_pct_change"] = ((minute_df.humidity - minute_df_hum_mean)/minute_df_hum_mean)

	# take last 60 rows
	# minute_df = minute_df.tail(60).reset_index()
	# fig0 = go.Figure()
	# fig0.add_trace(
		# go.Scatter(x=minute_df['timestamp'], y=minute_df['gc_pct_change'], mode="lines+markers",
				  # line=dict(color="red", shape="spline", smoothing=0.6), name="GC"),
	# )
	# fig0.add_trace(
		# go.Scatter(x=minute_df['timestamp'], y=minute_df['temp_pct_change'], mode="lines+markers",
				  # line=dict(color="green", shape="spline", smoothing=0.6, dash="dot"), name="Temp"),
	# )
	# fig0.add_trace(
		# go.Scatter(x=minute_df['timestamp'], y=minute_df['hum_pct_change'], mode="lines+markers",
				  # line=dict(color="blue", shape="spline", smoothing=0.6, dash="dot"), name="Humidity"),
	# )

	# fig0.update_layout(
		# xaxis_title="", 
		# yaxis_title="% Change", 
		# margin=dict(pad=10), 
		# title={
			# 'text': "Last 60 Minutes",
			# 'y':0.9,
			# 'x':0.5,
			# 'xanchor': 'center',
			# 'yanchor': 'top'}
	# )
	

	# plot graph1
	fig1 = go.Figure()
	fig1.add_trace(
		go.Scatter(x=one_day_df['timestamp'], y=one_day_df['gc_pct'], mode="lines+markers",
				  line=dict(color="red", shape="spline", smoothing=0.6), name="GC"),
	)
	fig1.add_trace(
		go.Scatter(x=one_day_df['timestamp'], y=one_day_df['temp_pct_scaled'], mode="lines+markers",
				  line=dict(color="#990099", shape="spline", smoothing=0.6, dash="dot"), name="Temp Scaled 0.1%"),
	)
	fig1.add_trace(
		go.Scatter(x=one_day_df['timestamp'], y=one_day_df['hum_pct'], mode="lines+markers", 
				  line=dict(color="black", shape="spline", smoothing=0.6, dash="dot"), name="Humidity"),
	)

	fig1.update_layout(
		xaxis_title="", 
		yaxis_title="% Change", 
		margin=dict(pad=10), 
		title={
			'text': "Last 24 Hours",
			'y':0.9,
			'x':0.5,
			'xanchor': 'center',
			'yanchor': 'top'}
	)
	
	# plot graph2
	fig2 = go.Figure()
	fig2.add_trace(
		go.Scatter(x=one_month_df['timestamp'], y=one_month_df['gc_pct'], mode="lines",
				  line=dict(color="red", shape="spline", smoothing=0.6), name="GC"),
	)
	fig2.add_trace(
		go.Scatter(x=one_month_df['timestamp'], y=one_month_df['temp_pct_scaled'], mode="lines",
				  line=dict(color="#990099", shape="spline", smoothing=0.6, dash="dot"), name="Temp Scaled 0.1%"),
	)
	fig2.add_trace(
		go.Scatter(x=one_month_df['timestamp'], y=one_month_df['hum_pct'], mode="lines", 
				  line=dict(color="black", shape="spline", smoothing=0.6), name="Humidity"),
	)

	fig2.update_layout(
		xaxis_title="", 
		yaxis_title="% Change", 
		margin=dict(pad=10), 
		title={
			'text': "Last 31 Days",
			'y':0.9,
			'x':0.5,
			'xanchor': 'center',
			'yanchor': 'top'}
	)
	
	# plot graph3
	fig3 = go.Figure()
	fig3.add_trace(
		go.Scatter(x=main_df['timestamp'], y=main_df['gc_pct'], mode="lines",
				  line=dict(color="red", shape="spline", smoothing=0.6), name="GC"),
	)
	fig3.add_trace(
		go.Scatter(x=main_df['timestamp'], y=main_df['temp_pct_scaled'], mode="lines",
				  line=dict(color="#990099", shape="spline", smoothing=0.6, dash="dot"), name="Temp Scaled 0.1%"),
	)
	fig3.add_trace(
		go.Scatter(x=main_df['timestamp'], y=main_df['hum_pct'], mode="lines", 
				  line=dict(color="black", shape="spline", smoothing=0.6), name="Humidity"),
	)

	fig3.update_layout(
		xaxis_title="", 
		yaxis_title="% Change", 
		margin=dict(pad=10), 
		title={
			'text': "All Data",
			'y':0.9,
			'x':0.5,
			'xanchor': 'center',
			'yanchor': 'top'}
	)

	fig3.update_layout(xaxis_title="Last 30 Days", yaxis_title="% Change")
	
	# following are graph for moving avarage/rolling avarage
	# plot graph4
	fig4 = go.Figure()
	fig4.add_trace(
		go.Scatter(x=one_day_df['timestamp'], y=one_day_df['gc_m_avg'], mode="lines+markers",
				  line=dict(color="red", shape="spline", smoothing=0.6), name="GC Rolling Average 6H"),
	)
	fig4.add_trace(
		go.Scatter(x=one_day_df['timestamp'], y=one_day_df['temp_pct_scaled'], mode="lines+markers",
				  line=dict(color="#990099", shape="spline", smoothing=0.6, dash="dot"), name="Temp Scaled 0.1%"),
	)
	fig4.add_trace(
		go.Scatter(x=one_day_df['timestamp'], y=one_day_df['hum_pct'], mode="lines+markers", 
				  line=dict(color="black", shape="spline", smoothing=0.6, dash="dot"), name="humidity"),
	)

	fig4.update_layout(
		xaxis_title="", 
		yaxis_title="% Change", 
		margin=dict(pad=10), 
		title={
			'text': "Last 24 Hours",
			'y':0.9,
			'x':0.5,
			'xanchor': 'center',
			'yanchor': 'top'}
	)
	
	# plot graph 5
	fig5 = go.Figure()
	fig5.add_trace(
		go.Scatter(x=one_month_df['timestamp'], y=one_month_df['gc_m_avg'], mode="lines",
				  line=dict(color="red", shape="spline", smoothing=0.6), name="GC Rolling Average 6H"),
	)
	fig5.add_trace(
		go.Scatter(x=one_month_df['timestamp'], y=one_month_df['temp_pct_scaled'], mode="lines",
				  line=dict(color="#990099", shape="spline", smoothing=0.6, dash="dot"), name="Temp scaled 0.1%"),
	)
	fig5.add_trace(
		go.Scatter(x=one_month_df['timestamp'], y=one_month_df['hum_pct_scaled'], mode="lines", 
				  line=dict(color="black", shape="spline", smoothing=0.6), name="Humidity Scaled 0.1%"),
	)

	fig5.update_layout(
		xaxis_title="", 
		yaxis_title="% Change", 
		margin=dict(pad=10), 
		title={
			'text': "Last 31 Days",
			'y':0.9,
			'x':0.5,
			'xanchor': 'center',
			'yanchor': 'top'}
	)
	
	# all data
	# plot graph 6
	fig6 = go.Figure()
	fig6.add_trace(
		go.Scatter(x=main_df['timestamp'], y=main_df['gc_m_avg'], mode="lines",
				  line=dict(color="red", shape="spline", smoothing=0.6), name="GC Rolling Average 6H"),
	)
	fig6.add_trace(
		go.Scatter(x=main_df['timestamp'], y=main_df['temp_pct_scaled'], mode="lines",
				  line=dict(color="#990099", shape="spline", smoothing=0.6, dash="dot"), name="Temp Scaled 0.1%"),
	)
	fig6.add_trace(
		go.Scatter(x=main_df['timestamp'], y=main_df['hum_pct_scaled'], mode="lines", 
				  line=dict(color="black", shape="spline", smoothing=0.6), name="Humidity Scaled 0.1%"),
	)

	fig6.update_layout(
		xaxis_title="", 
		yaxis_title="% Change", 
		margin=dict(pad=10), 
		title={
			'text': "All Data",
			'y':0.9,
			'x':0.5,
			'xanchor': 'center',
			'yanchor': 'top'}
	)
	
	return (
		html.Div(children=[
			
			html.Div(id="boxes",children=[
				html.Div(id="leftbox",children=[
						html.Img(src=app.get_asset_url("logo2.jpeg"), style={"height": "140px", "width": "280px"})
				]),
				
				# do not touch this component
				html.Div(id="middlebox",children=[
					html.H1(children="Geiger Station 1", style={"text-align": "center"}),
					html.Div(children="Address: NSC Rm124, GSU, Atlanta, GA", style={"text-align": "center", "color": "blue"}),
				]),
				
				html.Div(id="rightbox",children=[
					html.Img(src=app.get_asset_url("station-img.jpg"), style={"height": "140px", "width": "280px"})
				]),
			]),
						
			html.Hr(),
			
			html.Div(children=[
				html.P(children=["""This page shows the real-time measurement of background radiation using a """, html.A("Geiger Counter", href="https://en.wikipedia.org/wiki/File:Geiger_counter.jpg"), """. 
				The objective of this measurement is to monitor the changes of the background radiation together with the variations of the meteorological data. 
				The background radiation consists of ionizing particles produced from cosmic ray showers in the atmosphere and beta and gamma rays from the surrounding 
				building materials and/or soil. One of the goals of this measurement is to provide independent assessment of the variations of the 
				radon measurement on site."""]),
			], style={"text-align": "justify", "text-justify": "inter-word", "margin-left": "30px", "margin-right": "30px"}),
			
			html.Div(children=[
				html.P(children="""The plots below show time-series of percentage change of Geiger counts (in each minute) such as
				the hourly count percentage change in last 24 hours, in last 30 days and the complete dataset."""),
			], style={"text-align": "justify", "text-justify": "inter-word", "margin-left": "30px", "margin-right": "30px"}),
			
			html.Hr(),
			
			# insert graphs as html components
			# html.Div(children=[
				# dcc.Graph(
					# config={
						# 'displaylogo': False,
						# 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
					# },
					# id="example-graph-0",
					# figure=fig0,
				# ),
			# ]),
			
			html.Div(children=[
				dcc.Graph(
					config={
						'displaylogo': False,
						'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
					},
					id="example-graph-1",
					figure=fig1,
				),
			]),
			
			html.Div(children=[
				dcc.Graph(
					config={
						'displaylogo': False,
						'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
					},
					id="example-graph-2",
					figure=fig2,
				),
			]),
			
			html.Div(children=[
				dcc.Graph(
					config={
						'displaylogo': False,
						'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
					},
					id="example-graph-3",
					figure=fig3,
				),
			]),
			
			html.Div(children=[
				html.H3(children="- - - - - - - - ", style={"text-align": "center", "color": "black"}),
			]),
			
			html.Div(children=[
				dcc.Graph(
					config={
						'displaylogo': False,
						'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
					},
					id="example-graph-4",
					figure=fig4,
				),
			]),
			
			html.Div(children=[
				dcc.Graph(
					config={
						'displaylogo': False,
						'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
					},
					id="example-graph-5",
					figure=fig5,
				),
			]),
			
			html.Div(children=[
				dcc.Graph(
					config={
						'displaylogo': False,
						'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
					},
					id="example-graph-6",
					figure=fig6,
				),
			]),
			
			
			# time component
			html.Div(children=[
				html.Div(children="Last Updated: {}".format((datetime.now() - timedelta(minutes=15)).strftime("%m-%d-%Y-%H:%M:%S")), style={"text-align": "center", "color": "blue"}),
			]),
			
		])
	)
	



# create html layout
app.layout = serve_plots

if __name__ == '__main__':
	app.run_server(debug=True)


