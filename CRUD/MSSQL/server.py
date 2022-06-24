from urllib import response
from flask import Flask, request, Response, jsonify #importing classes
from flask_sqlalchemy import SQLAlchemy
import json
import sqlalchemy
from sqlalchemy import create_engine

app = Flask(__name__) #creating an instance of the Flask app

servername='@LAPTOP-45LE5KMT\\SQLEXPRESS'
dbname='Employees'

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pymssql://abdulvahab:cirrus123@35.232.137.244/empdb" #URI connection to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Employee(db.Model):# the class Employee will inherit the db.Model of SQLAlchemy
    __tablename__ = 'employees'  # employees is the name of the table
    empid = db.Column(db.Integer, primary_key=True)  # empid is the primary key
    name = db.Column(db.String(80), nullable=False)   # nullable is false so the column can't be empty
    email=db.Column(db.String(30), nullable=False)

    def json(self): #Function to display the output as JSON
        return {'emp_id': self.empid, 'name': self.name, 'email':self.email}

    def add_employee(_name, _email):    #Function to add employee to the database using _name and _email as parameters
        new_employee = Employee(name=_name, email=_email)   # the class Employee will inherit the db.Model of SQLAlchemy
        db.session.add(new_employee)  # add new movie to database session
        db.session.commit()  # commit changes to session

    def get_all_employees():    #Function to get all the employees in the database
        return [Employee.json(employee) for employee in Employee.query.all()]

    def get_employee(_empid):       #Function to get an employee in the database with the emp_id as a parameter.
        data=Employee.query.filter_by(empid=_empid)
        if data.count():    #checks if the employee with empid exists in the database
            return Employee.json(Employee.query.filter_by(empid=_empid).first())    #if the employee exists, then the details of that employee are retrieved
        else:
            return "Employee not found"     #if the employee doesn't exist, then the error message is returned
        
    
    def update_employee(_empid, _name,_email):  #function to update the details of an employee using the empid, name and email as parameters
        employee_update = Employee.query.filter_by(empid=_empid).first()    
        employee_update.name = _name    #After we filter by emp_id, we will update the name and email of the employee and then commit the changes.
        employee_update.email = _email
        db.session.commit()

    def delete_employee(_empid):    #function to delete an employee from the database using the empid of the employee as a parameter
        data=Employee.query.filter_by(empid=_empid)
        if data.count():    #check if the employee with empid exists in the database
            data.delete()   #.delete() method will delete the movie.
            db.session.commit() #changes are committed to the database
            return "Employee deleted"
        else:
            return "Employee not found" #if the employee is not found, then the error message will be returned
        

db.create_all() #creates table

@app.route('/employee', methods=['POST'])   #route for adding a new employee to the database using the 'POST' method
def add_employee(): #Function to add new employee to the database using the post method
    request_data = request.get_json()  # getting data from client
    Employee.add_employee(request_data["name"],request_data["email"])
    response = Response("Employee added", 201, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['DELETE']) #route for deleting a employee from the database using the 'DELETE' method
def remove_employee(empid):     #Function to delete movie from the database using empid as a parameter
    del_msg=Employee.delete_employee(empid)
    response = Response(del_msg, status=200, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['GET'])    #route for displaying the details of a particular employee from the database using the 'GET' method
def get_employee(empid):    #function to get the details of a particular employee using empid as a parameter
    data=json.dumps(Employee.get_employee(empid))   #json.dumps converts a python object to a string
    response=Response(data,status=200,mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['PUT'])    #route for updating the details of a particular employee in the database using the 'PUT' method
def update_employee(empid):     #function to update the employee details using empid as a parameter
    request_data = request.get_json()   #fetches the details of the employee with employee id empid
    Employee.update_employee(empid, request_data['name'], request_data['email'])       #updates the details of the particular employee                    
    response = Response("Employee Updated", status=200, mimetype='application/json')
    return response     

@app.route('/employee', methods=['GET'])    #route to get the details of the all the employees in the database
def get_employees():    #Function to get the details all the employees in the database'''
    return jsonify({'Employees': Employee.get_all_employees()})

app.run(debug=True,port=5000)   #runs the deployment server
