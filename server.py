from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'mydb')   
@app.route('/')
def index():
	email = mysql.query_db("SELECT * FROM email")
	print email
	return render_template('index.html', emails = email)
@app.route('/email', methods=['POST'])
def validate():
	if len(request.form['email']) < 1:
	    flash("Email cannot be blank!")
	elif not EMAIL_REGEX.match(request.form['email']):
	    flash("Invalid Email Address!")
	else:
	    flash("Success!") 
	if EMAIL_REGEX.match(request.form['email']): 
		query = "INSERT INTO email (emailaddress, created_at, updated_at) VALUES (:email, NOW(), NOW())"
		data = {
		         'email': request.form['email']
		       }
		mysql.query_db(query, data)
	return redirect('/sucess')
@app.route('/sucess')
def page():
	email = mysql.query_db("SELECT * FROM email")
	return render_template('sucess.html', emails = email)

@app.route('/remove_email/<email_id>', methods=['GET'])
def delete(email_id):
    query = "DELETE FROM email WHERE id = :id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/sucess')
app.run(debug=True)
