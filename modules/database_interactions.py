import os
from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv

# Get the absolute path to the directory containing this file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the .env file using the absolute path
env_path = os.path.join(current_dir, '..', 'mysql_config.env')
load_dotenv(env_path)

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
# GET ASSIGNMENT DETAILS
#--------------------------------------------------

@app.route('/get_assignment_details/<assign_id>', methods=['GET'])
def get_assignment_details(assign_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
        SELECT 
            Courses.CourseName,
            Modules.ModuleName,
            Assignments.AssignmentName,
            Assignments.AssignmentText,
            Tasks.TaskText,
            LearningObjectives.ObjectiveText,
            Questions.QuestionCriteria,
            Questions.QuestionText,
            SuggestedEvidence.EvidenceText
        FROM Assignments
        INNER JOIN Modules ON Assignments.ModuleID = Modules.ModuleID
        INNER JOIN Courses ON Modules.CourseID = Courses.CourseID
        INNER JOIN Tasks ON Assignments.AssignID = Tasks.AssignID
        INNER JOIN LearningObjectives ON Tasks.TaskID = LearningObjectives.TaskID
        INNER JOIN Questions ON LearningObjectives.ObjectiveID = Questions.ObjectiveID
        INNER JOIN SuggestedEvidence ON Questions.QuestionID = SuggestedEvidence.QuestionID
        WHERE Assignments.AssignID = %s
        ''', (assign_id,))
        assignment_details = cursor.fetchall()
    finally:
        cursor.close()
    return jsonify(assignment_details)


#--------------------------------------------------
# GET COURSES
#--------------------------------------------------

@app.route('/get_courses', methods=['GET'])
def get_courses():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT CourseID, CourseName FROM Courses')
        courses = cursor.fetchall()
        courses = [{'CourseID': course[0], 'CourseName': course[1]} for course in courses]
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
        cursor.execute('SELECT ModuleID, ModuleName FROM Modules WHERE CourseID = %s', (course_id,))
        modules = cursor.fetchall()
        modules = [{'ModuleID': module[0], 'ModuleName': module[1]} for module in modules]
    finally:
        cursor.close()
    return jsonify(modules)

#--------------------------------------------------
# GET ASSIGNMENTS
#--------------------------------------------------

@app.route('/get_assignments/<module_id>', methods=['GET'])
def get_assignments(module_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT AssignID, AssignmentName FROM Assignments WHERE ModuleID = %s', (module_id,))
        assignments = cursor.fetchall()
        assignments = [{'AssignID': assignment[0], 'AssignmentName': assignment[1]} for assignment in assignments]
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
        cursor.execute("SELECT UserID FROM Users WHERE Username = %s", (username,))
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
        cursor.execute("INSERT INTO Users (Username) VALUES (%s)", (username,))
        mysql.connection.commit()
        session['user_id'] = cursor.lastrowid
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': 'An error occurred: {}'.format(str(e))}
    finally:
        cursor.close()

if __name__ =='__main__':
    app.run(debug=True)