import os
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv('my_sql_config.env')

app = Flask(__name__)
CORS(app)
mysql = MySQL(app)

# MySQL configurations
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')

#------------------------------------------------------------------
# GET COURSES
#------------------------------------------------------------------

@app.route('/get_courses', methods=['GET'])
def get_courses():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT CourseID, CourseTitle FROM Courses')
    courses = cursor.fetchall()
    cursor.close()
    courses = [{'CourseID': course[0], 'CourseTitle': course[1]} for course in courses]
    return jsonify(courses)

#------------------------------------------------------------------
# GET MODULES
#------------------------------------------------------------------

@app.route('/get_modules/<course_id>', methods=['GET'])
def get_modules(course_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT ModuleNo, ModuleTitle FROM Modules WHERE CourseID = %s', (course_id,))
    modules = cursor.fetchall()
    cursor.close()
    modules = [{'ModuleNo': module[0], 'ModuleTitle': module[1]} for module in modules]
    return jsonify(modules)

#------------------------------------------------------------------
# GET ASSIGNMENTS
#------------------------------------------------------------------

@app.route('/get_assignments/<module_no>', methods=['GET'])
def get_assignments(module_no):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT AssignmentID, AssignmentTitle FROM Assignments WHERE ModuleNo = %s', (module_no,))
    assignments = cursor.fetchall()
    cursor.close()
    assignments = [{'AssignmentID': assignment[0], 'AssignmentTitle': assignment[1]} for assignment in assignments]
    return jsonify(assignments)

if __name__ == '__main__':
    app.run(debug=True)