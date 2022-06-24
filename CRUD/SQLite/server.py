from logging import root
from urllib import response
from flask import Flask, request, Response, jsonify #importing libraries
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__) #creating an instance of the Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Employees.db'    #The database URI used for the connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
#creating an instance of db
# the class Employee will inherit the db.Model of SQLAlchemy
class Employee(db.Model):
    __tablename__ = 'employees'  # creating a table name
    empid = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False) # nullable is false so that the column can't be empty
    email=db.Column(db.String(30), nullable=False)

    #Function to display the output as JSON
    def json(self):
        return {'emp_id': self.empid, 'name': self.name, 'email':self.email}

    #Function to add employee to the database
    def add_employee(_name, _email):
        new_employee = Employee(name=_name, email=_email) # creating an instance of Employee constructor
        db.session.add(new_employee)  # add new movie to database session
        db.session.commit()  # commit changes to session

    #Function to get all the employees in the database
    def get_all_employees():
        return [Employee.json(employee) for employee in Employee.query.all()]

    #Function to get an employee in the database with the emp_id as a parameter.
    def get_employee(_empid):
        return Employee.json(Employee.query.filter_by(empid=_empid).first())
        # Employee.json() coverts the output to the json format defined earlier
        # the filter_by method filters the query by the empid. But in this case, since the empid is unique, we will get only one result
        # the .first() method will get that first value returned

    #Function to update an employee in the database. 
    def update_employee(_empid, _name,_email): #empid, name and email are passed as parameters to the update_employee function
        employee_update = Employee.query.filter_by(empid=_empid).first() #empids are filtered initially, which is an exeption here.
        employee_update.name = _name #Employee's name is updated
        employee_update.email = _email #Employee's email is updated
        db.session.commit() #changes are committed to the session

    #Function to delete the employee from the database. We will filter by the id and the .delete() method will delete the movie.
    def delete_employee(_empid): #empid of the employee is passed as the parameter
        data=Employee.query.filter_by(empid=_empid) #Filters the empid using filter_by and stores it in data
        if data.count(): #If the particular empid exists, then the data of that particular employee is deleted
            data.delete()
            db.session.commit() #commit changes to the session
            return "Employee deleted"
        else:
            return "Employee not found" #If the employee with the particular empid doesn't exist, it returns the error message
        

db.create_all() #Creates tables that are associated with the model

@app.route('/employee', methods=['POST']) #creating a route to add employees to the database using the 'POST' method
def add_employee():
    request_data = request.get_json()  # getting data from client
    Employee.add_employee(request_data["name"],request_data["email"])
    response = Response("Employee added", 201, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['DELETE']) #creating a route to delete a employee from the database using the 'DELETE' method by specifying the empid
def remove_employee(empid):
    del_msg=Employee.delete_employee(empid)
    response = Response(del_msg, status=200, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['GET']) #route to get the details of a particular employee by specifying the empid using the 'GET' method
def get_employee(empid):
    data=json.dumps(Employee.get_employee(empid)) #.dumps is used so that the employee details will be in the format of a string
    response=Response(data,status=200,mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['PUT']) #route to update the details of a particular employee using the 'PUT' method
def update_employee(empid):
    request_data = request.get_json()
    Employee.update_employee(empid, request_data['name'], request_data['email'])                            
    response = Response("Employee Updated", status=200, mimetype='application/json')
    return response     

@app.route('/employee', methods=['GET']) #route to get the details of all employees in the database using the 'GET' method
def get_employees():
    return jsonify({'Employees': Employee.get_all_employees()})

app.run(debug=True,port=5000) #runs the deployment server

