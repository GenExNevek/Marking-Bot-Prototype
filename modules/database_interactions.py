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
# DISPLAY ASSIGNMENT
#--------------------------------------------------

@app.route('/display_assignment', methods=['GET'])
def display_assignment():
    course = request.args.get('course')
    module = request.args.get('module')
    assignment = request.args.get('assignment')
    
    cursor = mysql.connection.cursor()

    try:
        cursor.execute('SELECT CourseTitle FROM Courses WHERE CourseID = %s', (course,))
        course_title = cursor.fetchone()[0]
        
        cursor.execute('SELECT ModuleTitle FROM Modules WHERE ModuleNo = %s', (module,))
        module_title = cursor.fetchone()[0]
        
        cursor.execute('SELECT AssignmentTitle, AssignmentDescription FROM Assignments WHERE AssignmentID = %s', (assignment,))
        assignment_title, assignment_description = cursor.fetchone()

        cursor.execute('''
            SELECT 
                Tasks.TaskNo,
                Tasks.TaskDescription, 
                LearningObjectives.LearningObjectiveDescription, 
                Questions.QuestionCriteria, 
                Questions.QuestionDescription, 
                SuggestedEvidence.SuggestedEvidenceDescription 
            FROM 
                Tasks 
            INNER JOIN 
                LearningObjectives ON Tasks.TaskNo = LearningObjectives.TaskNo 
            INNER JOIN 
                Questions ON LearningObjectives.LearningObjectiveNo = Questions.LearningObjectiveNo 
            LEFT JOIN 
                SuggestedEvidence ON Questions.QuestionNo = SuggestedEvidence.QuestionNo 
            WHERE 
                Tasks.AssignmentID = %s
        ''', (assignment,))
        task_rows = cursor.fetchall()

        task_details = []
        for row in task_rows:
            task_no = row[0]
            task_description = row[1]
            learning_objective_description = row[2]
            question_criteria = row[3]
            question_description = row[4]
            suggested_evidence_description = row[5]

            task = next((item for item in task_details if item["TaskNo"] == task_no), None)
            if task is None:
                task = {
                    'TaskNo': task_no,
                    'TaskDescription': task_description,
                    'Questions': []
                }
                task_details.append(task)

            question = {
                'LearningObjectiveDescription': learning_objective_description,
                'QuestionCriteria': question_criteria,
                'QuestionDescription': question_description,
                'SuggestedEvidenceDescription': suggested_evidence_description
            }
            task['Questions'].append(question)

        return jsonify({
            'CourseTitle': course_title,
            'ModuleTitle': module_title,
            'AssignmentTitle': assignment_title,
            'AssignmentDescription': assignment_description,
            'TaskDetails': task_details
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