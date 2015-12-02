#!/usr/bin/python

import os
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.login import LoginManager
import json

import pandas as pd

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
	name = os.environ['USER']
	return render_template('index.html', name=name)


@app.route('/login')
def login():
	pass


@app.route('/overview')
def overview():
	projects = ['AA1', 'AA2']
	return render_template('overview.html', projects=projects)


@app.route('/analysis')
def analyze():
	return render_template('analysis.html')


@app.route('/mock_analysis')
def mock_analysis():
	df = pd.read_csv('testdata/otu_table_L3.txt', sep='\t', index_col=0)
	series = []
	threashold = 0.001 #Lowest fraction to display
	content = {}
	for row in df.iterrows():
		index, data = row
		trunc_index = ';'.join(index.split(';')[1:]) #Remove 'k_Bacteria;'
		if data.max() > threashold:
			content[trunc_index] = data.tolist()

	for key, value in content.items():
		obj = {'name': key, 'data' : value}
		series.append(obj)


	categories = list(df.columns)
	print series

	return render_template('mock_analysis.html', rows=series, series_json=json.dumps(series), categories=categories)



if __name__ == '__main__':
	manager.run()
