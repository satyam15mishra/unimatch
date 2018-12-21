from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
import os
from tabledef import *
#from dummydata import *
from sqlalchemy.orm import sessionmaker
import csv
import numpy as np 
import pandas as pd 
import random

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('homepage.html')
	
	else:
		return render_template('quiz.html')	

@app.route('/reg', methods=['GET','POST'])
def do_registration():
	
	Session = sessionmaker(bind = engine)
	s = Session()
	
	if request.method == 'POST':
		
		q = s.query(User).filter(User.username.in_([request.form['username']]))
		result = q.first()
		if result:
			return render_template('errorlog1.html')

		if request.form['password'] != request.form['confirm_password']:
			return render_template('errorlog2.html')
		
		USEX = ""
		UPET = ""
		user = User(request.form['username'].lower(), request.form['password'], USEX, UPET)

		s.add(user)
		s.commit()
		return render_template('errorlog3.html')
	
	else:
		return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
	
	Session = sessionmaker(bind = engine)
	s = Session()

	global USERN
	global PASSWD

	POST_USERNAME = str(request.form['username']).lower()
	USERN = POST_USERNAME	
	POST_PASSWORD = str(request.form['password'])
	PASSWD = POST_PASSWORD

	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
	result = query.first()
	if result:
		session['logged_in'] = True
	else:
		return 'wrong credentials'
	
	return home()

@app.route('/results', methods=['GET', 'POST'])
def results():
	
	Session = sessionmaker(bind = engine)
	s = Session()

	sex = request.form['sex']
	pet = request.form['pet']
	slf = request.form['self']
	hngout = request.form['hangout']

	USEX = str(sex)
	UPET = str(pet)

	details = User(USERN, PASSWD, USEX, UPET)
	s.add(details)
	s.commit()

	#assigned different weights
	if USEX == "Guys":
		USEX = 80
	else:
		USEX = 20
	if UPET == "Dogs":
		UPET = 70
	else:
		UPET = 40

	new_entry = [USERN, USEX, UPET]
	# the ab stands for append binary mode. append mode also works but leaves alternate rows blank
	with open('userdata.csv', 'ab') as csvfile: 
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(new_entry)
	
	#kmeans clustering
	dataset = pd.read_csv('userdata.csv')
	X = dataset.iloc[:, [1, 2]].values
	from sklearn.cluster import KMeans
	wcss = []
	for i in range(1, 11):
   		kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
   		kmeans.fit(X)
   		wcss.append(kmeans.inertia_)
	kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state = 42)
	y_kmeans = kmeans.fit_predict(X)	
	j=[]
	new_data = kmeans.predict([[USEX, UPET]])
	for i in y_kmeans:
		if new_data == i:
			j.append(i)		
	ans = random.choice(j)
	UCLUST = ans

	clustered = [USERN, UCLUST]
	with open('maindata.csv', 'ab') as mainfile:
		writer = csv.writer(mainfile)
		writer.writerow(clustered)
	mainfile.close()

	sarray =[]
	count = 0
	with open('maindata.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			sarray.append(r)
			count += 1
		
	barray=[]
	for main_i in range(0,count):
		if str(ans) == sarray[main_i][1]:
			barray.append(sarray[main_i][0])

	fmatch = random.choice(barray)

	return render_template('results.html', sex = sex, pet = pet, slf = slf, hngout = hngout, USERN = USERN, UCLUST = UCLUST, fmatch=fmatch)

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return home()

if __name__ == "__main__":
	app.run(debug = True)