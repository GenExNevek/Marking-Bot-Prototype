import os
from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv('../mysql_config.env')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Add this line to set a secret key for your Flask application
CORS(app)
mysql = MySQL(app)

# MySQL configurations
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')

#--------------------------------------------------
# GET COURSES
#--------------------------------------------------

@app.route('/get_courses', methods=['GET'])
def get_courses():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT CourseID, CourseTitle FROM Courses')
        courses = cursor.fetchall()
        courses = [{'CourseID': course[0], 'CourseTitle': course[1]} for course in courses]
    finally:
        cursor.close()
    return jsonify(courses)

#--------------------------------------------------
# GET MODULES
#--------------------------------------------------

@app.route('/get_modules/<course_id>', methods=['GET'])
def get_modules(course_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT ModuleNo, ModuleTitle FROM Modules WHERE CourseID = %s', (course_id,))
        modules = cursor.fetchall()
        modules = [{'ModuleNo': module[0], 'ModuleTitle': module[1]} for module in modules]
    finally:
        cursor.close()
    return jsonify(modules)

#--------------------------------------------------
# GET ASSIGNMENTS
#--------------------------------------------------

@app.route('/get_assignments/<module_no>', methods=['GET'])
def get_assignments(module_no):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT AssignmentID, AssignmentTitle FROM Assignments WHERE ModuleNo = %s', (module_no,))
        assignments = cursor.fetchall()
        assignments = [{'AssignmentID': assignment[0], 'AssignmentTitle': assignment[1]} for assignment in assignments]
    finally:
        cursor.close()
    return jsonify(assignments)

#--------------------------------------------------
# ASSIGN USER
#--------------------------------------------------

@app.route('/assign_user', methods=['POST'])
def flask_assign_user():
    username = request.json['username']
    result = assign_user(username)
    return jsonify(result)

#--------------------------------------------------
# CREATE USER
#--------------------------------------------------

@app.route('/create_user', methods=['POST'])
def flask_create_user():
    username = request.json['username']
    result = create_user(username)
    return jsonify(result)

def assign_user(username):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT UserID FROM Users WHERE Name = %s", (username,))
        result = cursor.fetchone()
        if result is None:
            return {'status': 'error', 'message': 'User does not exist'}
        else:
            session['user_id'] = result[0]
            return {'status': 'success'}
    finally:
        cursor.close()

def create_user(username):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO Users (Name) VALUES (%s)", (username,))
        mysql.connection.commit()
        session['user_id'] = cursor.lastrowid
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': 'An error occurred: {}'.format(str(e))}
    finally:
        cursor.close()

if __name__ =='__main__':
    app.run(debug=True)