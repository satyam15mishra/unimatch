from flask import Flask
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask import flash, redirect, render_template, request, session, abort, url_for
import os
from tabledef import *
#from dummydata import *
from sqlalchemy.orm import sessionmaker
import csv
import numpy as np
import pandas as pd
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(16)


uploadfolder = os.path.join('static', 'profile')
#uploadfolder = 'C:\Users\Satyam\Desktop\Code\unimatch\static\profiles'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','gif','png'])
app.config['UPLOAD_FOLDER'] = uploadfolder
def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def make_session_permanent():
	session.permanent = True
	app.permanent_session_lifteime = timedelta(minutes = 5)

@app.errorhandler(400)
def badreq(e):
	return render_template('400.html')

@app.errorhandler(405)
def meth(e):
	return 'No Tresspassing Bro'

@app.route('/')
def unimatch():
	return render_template('unimatch.html')


def messageReceived(methods=['GET', 'POST']):
	print('Message Recieved!')


@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/user')
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

		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return "Upload an image"
		if file and allowed_file(file.filename):
			global filename
			filename = secure_filename(file.filename)
			global iname
			iname = str(request.form['username']) + '.jpg'
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],iname))

		#global E_MAIL
		#POST_EMAIL = request.form['email']
		#E_MAIL = str(POST_EMAIL)
		#r = s.query(User).filter(User.contactinfo.in_([request.form['contactinfo']]))
		q = s.query(User).filter(User.username.in_([request.form['username']]))
		result1 = q.first()
		#result2 = r.first()
		if result1:
			return render_template('errorlog1.html')
		if request.form['password'] != request.form['confirm_password']:
			return render_template('errorlog2.html')

		UTIME = ""
		USEX = ""
		UCOLOR = ""
		UPERSONA = ""
		UWELCOME = ""
		UIRRIT = ""
		UTP = ""
		UDRINK = ""
		UMOVIES = ""
		UCHILL = ""

		user = User(request.form['username'].lower(), request.form['password'], request.form['email'], request.form['contactinfo'],UTIME,
			USEX,UCOLOR, UPERSONA,UWELCOME,UIRRIT,UTP,UDRINK,UMOVIES,UCHILL)

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
	#global CONTACT_INFO
	#global E_MAIL

	POST_USERNAME = str(request.form['username']).lower()
	USERN = POST_USERNAME
	POST_PASSWORD = str(request.form['password'])
	PASSWD = POST_PASSWORD
	#OST_EMAIL = str(request.form['email'])
	#E_MAIL = POST_EMAIL
	#POST_CONTACT = str(request.form['contactinfo'])
	#CONTACT_INFO = POST_CONTACT

	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
	result = query.first()
	if result:
		session['logged_in'] = True
	else:
		return render_template('wrong.html')

	return home()

@app.route('/results', methods=['GET', 'POST'])
def results():

	Session = sessionmaker(bind = engine)
	s = Session()

	time = request.form['time']
	sex = request.form['sex']
	personality = request.form['personality']
	color = request.form['color']
	welcome = request.form['welcome']
	irritate = request.form['irritate']
	timepass = request.form['timepass']
	drink = request.form['drink']
	movies = request.form['movies']
	chill = request.form['chill']
	contactinfo = request.form['contactinfo']

	USEX = str(sex)
	UTIME = str(time)
	UCOLOR = str(color)
	UPERSONA = str(personality)
	UWELCOME = str(welcome)
	UIRRIT = str(irritate)
	UTP = str(timepass)
	UDRINK = str(drink)
	UMOVIES = str(movies)
	UCHILL = str(chill)
	CONTACT_INFO = str(contactinfo)
	E_MAIL = ""

	details = User(USERN, PASSWD, CONTACT_INFO, E_MAIL, UTIME, USEX, UPERSONA, UCOLOR, UWELCOME, UIRRIT, UTP, UDRINK, UMOVIES, UCHILL)
	s.add(details)
	s.commit()

	#assigned different weights
	if UTIME == "morning":
		UTIME = 1
	elif UTIME == "noon":
		UTIME = 2
	else:
		UTIME = 0
	if USEX == "guys":
		USEX = 10
	else:
		USEX = 0
	if UPERSONA == "extrovert":
		UPERSONA = 1
	else:
		UPERSONA = 0
	if UWELCOME == "loud":
		UWELCOME = 1
	else:
		UWELCOME = 0
	if UIRRIT == "let":
		UIRRIT = 0
	else:
		UIRRIT = 1
	if UTP == "movies":
		UTP = 0
	else:
		UTP = 1
	if UDRINK == "coke":
		UDRINK = 0
	else:
		UDRINK = 1
	if UMOVIES == "mainstream":
		UMOVIES = 1
	else:
		UMOVIES = 0
	if UCHILL == "indoors":
		UCHILL = 0
	else:
		UCHILL = 1


	new_entry = [USERN, CONTACT_INFO, UTIME, USEX, UMOVIES, UCHILL, UDRINK, UTP, UIRRIT, UWELCOME, UPERSONA]
	# the ab stands for append binary mode. append mode also works but leaves alternate rows blank
	with open('new_data.csv', 'ab') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(new_entry)

	#kmeans clustering
	dataset = pd.read_csv('new_data.csv')
	X = dataset.iloc[:, [2,3,4,5,6,7,8,9,10]].values
	from sklearn.cluster import KMeans
	wcss = []
	for i in range(1, 11):
		kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
		kmeans.fit(X)
		wcss.append(kmeans.inertia_)
	kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state = 42)
	y_kmeans = kmeans.fit_predict(X)
	j=[]
	new_data = kmeans.predict([[UTIME, USEX, UMOVIES, UCHILL, UDRINK, UTP, UIRRIT, UWELCOME, UPERSONA]])
	for i in y_kmeans:
		if new_data == i:
			j.append(i)
	ans = random.choice(j)
	UCLUST = ans

	clustered = [USERN, UCLUST, CONTACT_INFO]
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
	infoarray = []
	for main_i in range(0,count):
		if str(ans) == sarray[main_i][1]:
			barray.append(sarray[main_i][0])
			infoarray.append(sarray[main_i][2])

	fmatch = random.choice(barray)
	finfo = infoarray[barray.index(fmatch)]
	if USERN == fmatch:
		fmatch = random.choice(barray)
		finfo = infoarray[barray.index(fmatch)]

	#here a function will come which will be responsible for detecting
	#the extension of file and renaming it to fmatch.extension

	imgfolder = '\\'+os.path.join('static','profile') #profiles on localhost
	im_name = fmatch + '.jpg'
	imgurl = '\\'+os.path.join(imgfolder, str(im_name))
	return render_template('results.html', USERN=USERN, CONTACT_INFO=CONTACT_INFO, fmatch=fmatch, finfo=finfo, imgurl=imgurl)

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return unimatch()

if __name__ == "__main__":
	app.run(debug = True)
