from urllib import response
from flask import Flask, request, Response, jsonify #importing classes
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__) #creating an instance of the Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost/Employees'   #The database URI used for the connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)    #creating an object of SQLAlchemy

class Employee(db.Model):   # the class Employee will inherit the db.Model of SQLAlchemy
    __tablename__ = 'employees'  # creating a table name
    empid = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False) # nullable is false so the column can't be empty
    email=db.Column(db.String(30), nullable=False)

    def json(self): #Function to display the output as JSON
        return {'emp_id': self.empid, 'name': self.name, 'email':self.email}

    def add_employee(_name, _email):    #Function to add employee to the database using name, email as parameters
        new_employee = Employee(name=_name, email=_email)   # creating an instance of Employee constructor
        db.session.add(new_employee)  # adding a new employee to database session
        db.session.commit()  # commit changes to session

    def get_all_employees():    #Function to get all the employees in the database
        return [Employee.json(employee) for employee in Employee.query.all()]

    def get_employee(_empid):       #Function to get an employee in the database with the emp_id as a parameter.
        data=Employee.query.filter_by(empid=_empid)
        if data.count():    #if the employee with the empid exists the following code gets gets executed
            return Employee.json(Employee.query.filter_by(empid=_empid).first())    
        else:
            return "Employee not found" #if the employee doesn't exist then the error message is returned
        # Employee.json() coverts our output to the json format
        # the filter_by method filters the query by the id
        # since our id is unique we will only get one result
        # the .first() method will get that first value returned

    def update_employee(_empid, _name,_email):  #function to update the details of an employee using the empid, name and email as parameters
        employee_update = Employee.query.filter_by(empid=_empid).first()
        employee_update.name = _name    #After we filter by emp_id, we will update the name and email of the employee and then commit the changes.
        employee_update.email = _email
        db.session.commit()

    def delete_employee(_empid):    #function to delete an employee from the database using the empid of the employee as a parameter
        data=Employee.query.filter_by(empid=_empid)
        if data.count():    #checks if the employee with empid exists in the database
            data.delete()   #deletes the particular employee data from the database with 
            db.session.commit()     #commits the changes
            return "Employee deleted"   #returns the success message
        else:
            return "Employee not found" #if the employee doesn't exist, returns the error message
        

db.create_all() #makes the application create the table in the database

@app.route('/employee', methods=['POST'])   #route to add an employee to the database using the 'POST' method
def add_employee():     #Function to add new employee to the database'''
    request_data = request.get_json()  # getting data from client
    Employee.add_employee(request_data["name"],request_data["email"])   #calling the function add_employee defined in the Employee class
    response = Response("Employee added", 201, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['DELETE'])     #route to delete an employee from the database using the empid through the 'DELETE' method
def remove_employee(empid):     #Function to delete employee from the database'''
    del_msg=Employee.delete_employee(empid)     #calling the function delete_employee defined in the Employee class
    response = Response(del_msg, status=200, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['GET'])    #route to get the details of an employee from the database using the empid through the 'GET' method
def get_employee(empid):    #function to get the details of a particular employee from the database
    data=json.dumps(Employee.get_employee(empid))   #json.dumps() encodes the python object into JSON formatted string
    response=Response(data,status=200,mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['PUT'])    #route to update the details of an employee in the database using the empid through the 'PUT' method
def update_employee(empid): #function to update the details of a particular employee in the database
    request_data = request.get_json()
    Employee.update_employee(empid, request_data['name'], request_data['email'])       #calling the function update_employee defined in the Employee class                     
    response = Response("Employee Updated", status=200, mimetype='application/json')
    return response     

@app.route('/employee', methods=['GET'])    #route to get the details of all the employees in the database
def get_employees():    #Function to get all the employees in the database'''
    return jsonify({'Employees': Employee.get_all_employees()})

app.run(debug=True,port=5000)   #runs the deployment server
