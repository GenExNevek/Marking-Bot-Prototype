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

@app.route('/display_assignment', methods=['GET'])
def display_assignment():
    course = request.args.get('course')
    module = request.args.get('module')
    assignment = request.args.get('assignment')
    
    cursor = mysql.connection.cursor()
    
    try:
        cursor.execute('SELECT CourseName FROM Courses WHERE CourseID = %s', (course,))
        course_name = cursor.fetchone()[0]
        
        cursor.execute('SELECT ModuleName FROM Modules WHERE ModuleID = %s', (module,))
        module_name = cursor.fetchone()[0]
        
        cursor.execute('SELECT AssignmentName, AssignmentText FROM Assignments WHERE AssignID = %s', (assignment,))
        assignment_name, assignment_text = cursor.fetchone()

        cursor.execute('SELECT TaskID, TaskText FROM Tasks WHERE AssignID = %s', (assignment,))
        tasks = [list(task) for task in cursor.fetchall()]

        for task in tasks:
            cursor.execute('SELECT ObjectiveID, ObjectiveText FROM LearningObjectives WHERE TaskID = %s', (task[0],))
            task.append([list(objective) for objective in cursor.fetchall()])

            for objective in task[2]:
                cursor.execute('SELECT QuestionID, QuestionText FROM Questions WHERE ObjectiveID = %s', (objective[0],))
                objective.append([list(question) for question in cursor.fetchall()])

                for question in objective[2]:
                    cursor.execute('SELECT EvidenceText FROM SuggestedEvidence WHERE QuestionID = %s', (question[0],))
                    question.append(cursor.fetchone()[0])
        
        return jsonify({
        'CourseName': course_name,
        'ModuleName': module_name,
        'AssignmentName': assignment_name,
        'AssignmentText': assignment_text,
        'Tasks': tasks
    })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


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