import sqlite3
from flask import Flask, render_template, request, url_for, flash, jsonify, redirect, abort, session, make_response, send_file, send_from_directory
import pdfkit
import platform
import os, logging 
import subprocess
from decouple import config
import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import HTTPException, NotFound, abort
from jinja2 import TemplateNotFound

app = Flask(__name__)
app.config['SECRET_KEY'] = 'S#perS3crEt_007' #generate secret key https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx example: 3777217A25432646294A404E635266556A586E3272357538782F413F4428472D4B6150645367566B5970337336763979244226452948404D6251655468576D5A7134743777217A25432A462D4A614E645266556A586E3272357538782F413F4428472B4B6250655368566B5970337336763979244226452948404D635166546A576E5A7134743777217A25432A462D4A614E645267556B58703273357638782F413F4428472B4B6250655368566D597133743677397A244226452948404D635166546A576E5A7234753778214125442A462D4A614E645267556B58703273357638792F423F4528482B4B6250655368566D597133743677397A24432646294A40
# or bPeShVmYq3t6w9z$B&E)H@McQfTjWnZr4u7x!A%D*F-JaNdRgUkXp2s5v8y/B?E(H+KbPeShVmYq3t6w9z$C&F)J@NcQfTjWnZr4

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10 # max file size 10mb
app.config['UPLOAD_PATH'] = '/'
# ------------------------------------------------------------------------------------



basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	CSRF_ENABLED = True
	SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object('app.Config')

db = SQLAlchemy(app) # flask-sqlalchemy
bc = Bcrypt(app) # flask-bcrypt

lm = flask_login.LoginManager(   ) # flask-loginmanager
lm.init_app(app)       # init the login manager

class Users(db.Model, flask_login.UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique = True)
	email = db.Column(db.String(120), unique = True)
	password = db.Column(db.String(500))

	def __init__(self, username, email, password):
		self.username = username
		self.password = password
		self.email = email

	def __repr__(self):
		return str(self.id) + ' - ' + str(self.username)

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self

# ------------------------------------------------------------------------------------

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
	if request.blueprint == 'api':
		abort(HTTPStatus.UNAUTHORIZED)
	return redirect(url_for('login'))
    
@login_manager.user_loader
@lm.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = None
	success = False
	if request.method == 'GET': 
		return render_template( 'register.html', msg=msg )
	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"] 
		email = request.form["email"]
		user_by_username = Users.query.filter_by(username=username).first()
		user_by_email = Users.query.filter_by(email=email).first()
		if user_by_username or user_by_email:
			msg = 'Error: User exists!'
		else:
			# pw_hash = bc.generate_password_hash(password)
			user = Users(username, email, password)
			user.save()
			msg = 'User created, please <a href="' + url_for('login') + '">login</a>'
			success = True
	else:
		msg = 'Input error'
	return render_template('register.html',msg=msg, success=success )

@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = None
	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"]
		user = Users.query.filter_by(username=username).first()
		if user:
			# if bc.check_password_hash(user.password, password):
			if (user.password == password):
				flask_login.login_user(user)
				return redirect(url_for('index'))
			else:
				msg = "Wrong password. Please try again."
		else:
			msg = "Unknown user"
	return render_template( 'login.html', msg=msg)
    
# ------------------------------------------------------------------------------------

def get_db_connection():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn


def get_pathways_columns():
	conn = get_db_connection()
	results = conn.execute("PRAGMA table_info(pathways)")
	data = results.fetchall()
	pathways_columns = [i[1] for i in data] # i[0] id, i[1] column names
	conn.close()
	if pathways_columns is None:
		abort(404)
	return pathways_columns

def get_pathways(pathways_id):
	conn = get_db_connection()
	post = conn.execute('SELECT * FROM pathways WHERE id = ?',(pathways_id,)).fetchone()
	conn.close()
	if post is None:
		abort(404)
	return post

def get_ids_from_pathways():
	conn = get_db_connection()
	data = conn.execute('SELECT id FROM pathways').fetchall()	
	ids = [i[0] for i in data]
	conn.close()
	if data is None:
		abort(404)
	return ids

def get_ids_columns():
	conn = get_db_connection()
	results = conn.execute("PRAGMA table_info(id)")
	data = results.fetchall()
	ids_columns = [i[1] for i in data]
	conn.close()
	if ids_columns is None:
		abort(404)
	return ids_columns
	
# -------------------------------------------------------------------------------------

@app.route('/')
def index():
	# if not flask_login.current_user.is_authenticated:
		# return redirect(url_for('login'))
	try:
		return render_template('index.html')
	except TemplateNotFound:
		return render_template('page-404.html'), 404
	except:
		return render_template('page-500.html'), 500
	# return render_template('index.html')
	
@app.route('/about/')
def about():
	conn = get_db_connection()
	posts = conn.execute('SELECT * FROM about WHERE type="developer"').fetchall()
	conn.close()
	return render_template('about.html', posts=posts)

def import_csv(filename):
	file_to_import = open(filename, "r")
	content = file_to_import.readlines()
	file_to_import.close()
	
	result = insert_to_db(content)
	
	# print(content)
	return True

	
def insert_to_db(content):
	conn = get_db_connection()
	pathways_columns = get_pathways_columns()	 
	
	# print(pathways_columns)
	
	# print(content[0])
	header = content[0]
	# print(pathways_columns)
	
	columns = header.split(",")
	# print(columns)
	
	columns_to_add = []
	columns_existing = []
	
	for index1,item1 in enumerate(pathways_columns):
		for index2,item2 in enumerate(columns):
			if (pathways_columns[index1] == columns[index2]):
				columns_existing.append(columns[index2])
			else:
				columns_to_add.append(columns[index2])
	
	# print(columns_to_add)
	
	for item in columns_to_add:
		try:
			alter_query = "alter table pathways ADD COLUMN " + item + " REAL default 0;"
			# print("---------------------------------------------------")
			# print(alter_query)
			# print("---------------------------------------------------")
			conn = get_db_connection()
			result = conn.execute(alter_query)
			conn.commit()
			conn.close()
		except:
			continue
			
	print(content)
	
	header = content[0][3:-1]
	insert_query = "INSERT INTO pathways (" + header + ") VALUES\n"
	for i in range(1,len(content)):
		# print(row.split("\n"))		
		temp = content[i].split(",")
		insert_query = insert_query + "("
		for item in range(1,len(temp)):
			insert_query = insert_query + str(temp[item].strip()) + ","
			# print(item)
		insert_query = insert_query[0:-1]
		insert_query = insert_query + "),"
	insert_query = insert_query[0:-1]
	insert_query = insert_query + ";"
	print("---------------------------------------------------")
	print(insert_query)
	print("---------------------------------------------------")
	
	conn = get_db_connection()
	result = conn.execute(insert_query)
	conn.commit()
	conn.close()
	
	print("DB - success - createPathways()")
	print(result)
	
	return True
	
# -------------------------------------------------------------------------------------

@app.route('/listPathways/')
@flask_login.login_required
def listPathways():
	conn = get_db_connection()
	data = conn.execute('SELECT id FROM pathways').fetchall()
	pathways_ids = [i[0] for i in data]
	pathways_columns = get_pathways_columns()
	conn.close()
	return render_template('listPathways.html', pathways_ids=pathways_ids, pathways_columns_len=len(pathways_columns), pathways_columns=pathways_columns)

@app.route('/listPathways/json/', methods=('POST',))
def listPathwaysJSON():
	try:
		selected_column = request.form["pathways_select_column"]
		selected_id = request.form["pathways_select_id"]
	except:		
		flash("Please choose a pathway ID from the list")
		return redirect(url_for('listPathways'))
		print("Choose a pathway ID below")
		
	conn = get_db_connection()
	query = "SELECT "+selected_column+" FROM pathways"
	query1 = "SELECT "+selected_id+" FROM id"
	ids_results = conn.execute(query1).fetchall()
	pathways_results = conn.execute(query).fetchall()
	conn.close()
	#refiner

	csv_file = open("id_results.csv","w")
	line_to_write = ""
	for row in ids_results:
		for item in row:
			# print(item)
			csv_file.writelines(str(item) + "\n")		
	csv_file.close()

	csv_file = open("pathways_results.csv","w")
	line_to_write = ""
	for row in pathways_results:
		for item in row:
			# print(item)
			csv_file.writelines(str(item) + "\n")
			
	csv_file.close()
	
	refiner_results = subprocess.check_output("Rscript refiner.R ", shell= True)
	temp = str(refiner_results.strip())
	temp = temp.replace("[1]","")
	temp = temp.replace("b","")
	temp = temp.replace("\"","")
	temp = temp.replace("\'","")
	temp = temp.replace("-","")
	refiner_result = []
	refiner_result.append(temp)
	print(temp)
		
	return jsonify(refiner_result)
	
	
@app.route('/listPathways/json2/', methods=('POST',))
def listPathwaysJSON2():
	conn = get_db_connection()
	selected_id = request.form["pathways_select_id"]
	pathways = conn.execute('SELECT * FROM pathways WHERE id='+selected_id).fetchall()
	conn.close()
	result = [{k: item[k] for k in item.keys()} for item in pathways]
	return jsonify(result)

@app.route('/listPathwaysWithID/', methods=('POST',))
def listPathwaysWithID():
	# try:
		# selected_id = request.form["pathways_select_id"]
	# except:		
		# flash("Please choose a pathway ID from the list")
		# return redirect(url_for('listPathways'))
		# print("Choose a pathway ID below")
		
	# try:
		# print(request.form["json_choice"])
		# if request.form["json_choice"]=="checked":
			# print("json_choice checked")
			# return redirect(url_for('listPathwaysJSON'), code=307)
	# except:
		# print("json_choice unchecked")
		
	# conn = get_db_connection()
	# selected_id = request.form["pathways_select_id"]
	# pathways = conn.execute('SELECT * FROM pathways WHERE id='+selected_id).fetchall()
	# pathways_columns = get_pathways_columns()
	# conn.close()
	# return render_template('listPathwaysWithID.html', pathways=pathways, pathways_columns=pathways_columns)
	
	try:
		selected_column = request.form["pathways_select_column"]
		selected_id = request.form["pathways_select_id"]
	except:		
		flash("Please choose a pathway ID from the list")
		return redirect(url_for('listPathways'))
		print("Choose a pathway ID below")
		
	try:
		print(request.form["json_choice"])
		if request.form["json_choice"]=="checked":
			print("json_choice checked")
			return redirect(url_for('listPathwaysJSON'), code=307)
	except:
		print("json_choice unchecked")
		
	conn = get_db_connection()
	query = "SELECT "+selected_column+" FROM pathways"
	query1 = "SELECT "+selected_id+" FROM id"
	ids_results = conn.execute(query1).fetchall()
	pathways_results = conn.execute(query).fetchall()
	conn.close()
	#refiner

	csv_file = open("id_results.csv","w")
	line_to_write = ""
	for row in ids_results:
		for item in row:
			# print(item)
			csv_file.writelines(str(item) + "\n")		
	csv_file.close()

	csv_file = open("pathways_results.csv","w")
	line_to_write = ""
	for row in pathways_results:
		for item in row:
			# print(item)
			csv_file.writelines(str(item) + "\n")
			
	csv_file.close()
	
	refiner_results = subprocess.check_output("Rscript refiner.R ", shell= True)
	temp = str(refiner_results.strip())
	temp = temp.replace("[1]","")
	temp = temp.replace("b","")
	temp = temp.replace("\"","")
	temp = temp.replace("\'","")
	refiner_result = temp.replace("-","")
	print(temp)
	
	return render_template('listPathwaysWithID.html', refiner_result=refiner_result, selected_column=selected_column, selected_id=selected_id)

@app.route('/listPathwaysWithID2/', methods=('POST',))
def listPathwaysWithID2():
	try:
		selected_id = request.form["pathways_select_id"]
	except:		
		flash("Please choose a pathway ID from the list")
		return redirect(url_for('listPathways'))
		print("Choose a pathway ID below")
		
	try:
		print(request.form["json_choice2"])
		if request.form["json_choice2"]=="checked":
			print("json_choice2 checked")
			return redirect(url_for('listPathwaysJSON2'), code=307)
	except:
		print("json_choice2 unchecked")
		
	conn = get_db_connection()
	selected_id = request.form["pathways_select_id"]
	pathways = conn.execute('SELECT * FROM pathways WHERE id='+selected_id).fetchall()
	pathways_columns = get_pathways_columns()
	conn.close()
	return render_template('listPathwaysWithID2.html', pathways=pathways, pathways_columns=pathways_columns)
	

@app.route('/createPathways/', methods=('GET', 'POST'))
@flask_login.login_required
def createPathways():
	pathways_columns = get_pathways_columns()
	if request.method == 'POST':
		for item in request.form:
			if not item:
				flash(str(item) + ' is required!')
		
		insert_query = "INSERT INTO pathways ("
		for item in request.form:
			insert_query = insert_query + item + ","
		insert_query = insert_query[0:-1]
		insert_query = insert_query + ") VALUES("
		for item in request.form:
			insert_query = insert_query + request.form[item] + ","
		insert_query = insert_query[0:-1]
		insert_query = insert_query + ")"
		
		try:	
			conn = get_db_connection()
			result = conn.execute(insert_query)
			# print("--------------------------------------------------------------------\n\n\n\n")
			# print(insert_query)
			# print("--------------------------------------------------------------------\n\n\n\n")
			print("DB - success - createPathways()")
			print(result)
			conn.commit()
			conn.close()
			return redirect(url_for('listPathways'))
		except sqlite3.Error as err:
			print("DB - failed - createPathways()")
			print(err)
			return redirect(url_for('listPathways'))

	return render_template('createPathways.html', pathways_columns_len=len(pathways_columns), pathways_columns=pathways_columns)
	
@app.route('/editPathways/<int:id>/', methods=('GET', 'POST'))
@flask_login.login_required
def editPathways(id):
	pathways = get_pathways(id)
	pathways_columns = get_pathways_columns()

	if request.method == 'POST':		
		conn = get_db_connection()
		update_query = 'UPDATE pathways SET '
		for item in request.form:
			update_query = update_query + item + "="+ request.form[item] +", "
		update_query = update_query[0:-2] # delete comma at the end of query
		update_query = update_query + " WHERE id=" + str(id)
				
		try:
			conn = get_db_connection()
			result = conn.execute(update_query)
			# print("--------------------------------------------------------------------\n\n\n\n")
			# print(update_query)
			# print("--------------------------------------------------------------------\n\n\n\n")
			flash("Pathways ID="+ str(pathways["id"]) +" was successfully updated!")
			print("DB - success - editPathways("+str(id)+")")
			print(result)
			conn.commit()
			conn.close()
			return redirect(url_for('listPathways'))
		except sqlite3.Error as err:
			flash(err)
			print("DB - failed - editPathways("+str(id)+")")
			print(err)
			return redirect(url_for('listPathways'))

	return render_template('editPathways.html', pathways=pathways, pathways_len=len(pathways), pathways_columns=pathways_columns)
	
@app.route('/deletePathways/<int:id>/', methods=('POST',))
@flask_login.login_required
def deletePathways(id):
	pathways = get_pathways(id)	
	
	try:
		conn = get_db_connection()
		result = conn.execute('DELETE FROM pathways WHERE id = ?', (id,))
		print("DB - success - deletePathways("+str(id)+")")
		print(result)
		conn.commit()
		conn.close()
		flash("Pathways ID="+ str(pathways["id"]) +" was successfully deleted!")
		return redirect(url_for('listPathways'))
	except sqlite3.Error as err:
		print("DB - failed - deletePathways("+str(id)+")")
		print(err)
		return redirect(url_for('listPathways'))

@app.route('/pathways/pdf/<id>')
def pathways_output_pdf(id):
	pathways = get_pathways(id)
	pathways_columns = get_pathways_columns()
	if platform.system() == 'Windows':
		conf = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
	else:
		WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
		conf = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

	#print(pathways)
	#print(pathways_columns)
	html = render_template("pathways_id_pdf.html",pathways=pathways, pathways_columns=pathways_columns)
	print(html)
	options = {"enable-local-file-access": None}
	pdf = pdfkit.from_string(html, False, configuration=conf, options=options)
	
	response = make_response(pdf)
	response.headers["Content-Type"] = "application/pdf"
	#response.headers["Content-Disposition"] = "inline; filename=pathways_id_"+str(id)+".pdf"
	return response

@app.route('/pathways_download/<filename>')
def pathways_download(filename):
	return send_file(filename, as_attachment=True)

@app.route('/pathways_download_sample_csv/')
def pathways_download_sample_csv():
	return send_file("sample_pathways.csv", as_attachment=True)
	
@app.route('/pathways/uploadCSV/', methods=('POST',))
@flask_login.login_required
def uploadCSVforPathways():
	uploaded_file = request.files["csv_file"]
	if uploaded_file.filename != "":
		print(uploaded_file.filename)
		uploaded_file.save("uploaded_pathways.csv") #uploaded_file.filename
		flash('file uploaded successfully')
		
		result = import_csv("uploaded_pathways.csv")
		
	return redirect(url_for('listPathways'))

# -------------------------------------------------------------------------------------

@app.route('/referenceInterval/')
@flask_login.login_required
def referenceInterval():
	conn = get_db_connection()
	pathways_columns = get_pathways_columns()
	ids = get_ids_from_pathways()
	conn.close()
	return render_template('referenceInterval.html', ids_len=len(ids), ids=ids, pathways_columns_len=len(pathways_columns), pathways_columns=pathways_columns)
	
@app.route('/referenceIntervalResults/', methods=('POST',))
def referenceIntervalResults():
	try:
		selected_column = request.form["pathways_select_column"]
		# selected_id = request.form["pathways_select_id"]
	except:		
		flash("Please choose a pathway name and id from the list")
		return redirect(url_for('referenceInterval'))
		print("Choose a pathway name and id below")
		
	try:
		if request.form["json_choice"]:
			print("json_choice checked")
			return redirect(url_for('referenceIntervalResultsJSON'), code=307)
	except:
		print("json_choice unchecked")
	conn = get_db_connection()
	query = "SELECT "+selected_column+" FROM pathways"
	# query1 = "SELECT "+selected_id+" FROM id"
	# ids_results = conn.execute(query1).fetchall()
	pathways_results = conn.execute(query).fetchall()
	conn.close()
	#refiner

	# csv_file = open("id_results.csv","w")
	# line_to_write = ""
	# for row in ids_results:
		# for item in row:
			# # print(item)
			# csv_file.writelines(str(item) + "\n")		
	# csv_file.close()

	csv_file = open("pathways_results.csv","w")
	line_to_write = ""
	for row in pathways_results:
		for item in row:
			# print(item)
			csv_file.writelines(str(item) + "\n")
			
	csv_file.close()
	
	refiner_results = subprocess.check_output("Rscript refiner_rie.R ", shell= True)
	refiner_result = []
	for line in refiner_results.splitlines():
		temp = str(line.strip())
		temp = temp.replace("b","")
		temp = temp.replace("\"","")
		temp = temp.replace("\'","")
		temp = temp.replace("-","")
		print(temp)
		refiner_result.append(temp)
	
	return render_template('referenceIntervalResults.html', refiner_result=refiner_result, selected_column=selected_column)
	
@app.route('/referenceIntervalResults/json', methods=('POST',))
def referenceIntervalResultsJSON():
	selected_column = request.form["pathways_select_column"]
	# selected_id = request.form["pathways_select_id"]
	conn = get_db_connection()
	query = "SELECT "+selected_column+" FROM pathways"
	pathways_results = conn.execute(query).fetchall()
	conn.close()
	#refiner
	csv_file = open("pathways_results.csv","w")
	line_to_write = ""
	for row in pathways_results:
		for item in row:
			# print(item)
			csv_file.writelines(str(item) + "\n")
			
	csv_file.close()
	refiner_results = subprocess.check_output("Rscript refiner_rie.R "+selected_column, shell= True)
	print(refiner_results)
	
	refiner_result = []
	for line in refiner_results.splitlines():
		temp = str(line.strip())
		temp = temp.replace("b","")
		temp = temp.replace("\"","")
		temp = temp.replace("\'","")
		temp = temp.replace("-","")
		# print(temp)
		refiner_result.append(temp)
	
	result = {}
	for i in range(len(refiner_result)):
		if refiner_result[i]!= "":
			result[i] = refiner_result[i]
			
	# print(result)
	return jsonify(result)
	
@app.route('/refiner/pdf/', methods=('POST',))
def refiner_output_pdf():
	if platform.system() == 'Windows':
		conf = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
	else:
		WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
		conf = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
		
	refiner_result=request.form["refiner_result"].split(",")
	refiner_result=[ x.replace("'","") for x in refiner_result]
	refiner_result=[ x.replace("[","") for x in refiner_result]
	refiner_result=[ x.replace("]","") for x in refiner_result]
	
	selected_column=request.form["selected_column"]
	# selected_id=request.form["selected_id"]
		
	html = render_template("referenceIntervalResults_PDF.html", refiner_result=refiner_result, selected_column=selected_column)

	options = {"enable-local-file-access": None}
	pdf = pdfkit.from_string(html, False, configuration=conf, options=options)
	
	response = make_response(pdf)
	response.headers["Content-Type"] = "application/pdf"
	response.headers["Content-Disposition"] = "inline; filename=refiner_result.pdf"
	return response

	
	
	
	
	
	
	
	
	
	
	
