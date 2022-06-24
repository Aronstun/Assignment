from urllib import response
from flask import Flask, request, Response, jsonify #importing classes
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__) #creating an instance of the Flask web application

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost:3306/Employees' #The database URI used for the connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)    #creating an object of SQLAlchemy

class Employee(db.Model):   # the class Employee will inherit the db.Model of SQLAlchemy
    __tablename__ = 'employees'  #defining the table name
    empid = db.Column(db.Integer, primary_key=True)  # empid is the primary key
    name = db.Column(db.String(80), nullable=False)  # nullable is false so the column can't be empty
    email=db.Column(db.String(30), nullable=False)

    def json(self):     #Function to display the output as JSON
        return {'emp_id': self.empid, 'name': self.name, 'email':self.email}

    def add_employee(_name, _email):    #Function to add employee to the database using _name and _email as parameters
        new_employee = Employee(name=_name, email=_email)   # creating an instance of Employee constructor
        db.session.add(new_employee)  # add new employee to database session
        db.session.commit()  # committing changes to the session

    def get_all_employees():    #Function to get all the employees in the database
        return [Employee.json(employee) for employee in Employee.query.all()]   #returns all the employees in the database

    def get_employee(_empid):    #Function to get an employee in the database with the emp_id as a parameter.
        return Employee.json(Employee.query.filter_by(empid=_empid).first())
        # Employee.json() coverts the output to the json format 
        # The filter_by method filters the query by the id
        # Since our id is unique we will only get one result
        # the .first() method will get that first value returned which is an exception here

    def update_employee(_empid, _name,_email):     #function to update the details of an employee using the empid, name and email as parameters
        employee_update = Employee.query.filter_by(empid=_empid).first()
        employee_update.name = _name    #new name is updated for the employee with empid 
        employee_update.email = _email  #new email is updated for the employee with empid 
        db.session.commit()     #changes are committed to the database

    #Function to delete the employee from the database. We will filter by the id and the 
    def delete_employee(_empid):    #function to delete an employee from the database using the empid of the employee as a parameter
        data=Employee.query.filter_by(empid=_empid)
        if data.count():    #if the employee with the empid exists, the following actions will be performed
            data.delete()   #.delete() method will delete the employee.
            db.session.commit() #changes are committed to the database
            return "Employee deleted"   #success message is returned
        else:
            return "Employee not found"     #if the employee doesn't exist, then an error message is returned
        

db.create_all() #makes the application create all the tables defined in the database

@app.route('/employee', methods=['POST'])   #creating a route to add a new employee to the database with the 'POST' method
def add_employee():     
    request_data = request.get_json()  # getting data from client
    Employee.add_employee(request_data["name"],request_data["email"])   #calling the add_employees function
    response = Response("Employee added", 201, mimetype='application/json') 
    return response

@app.route('/employee/<int:empid>', methods=['DELETE']) #creating a route to delete a employee from the database with the 'DELETE' method
def remove_employee(empid):    
    del_msg=Employee.delete_employee(empid)     #calling the delete_employee function
    response = Response(del_msg, status=200, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['GET'])    #creating a route to retrieve a employee from the database 'GET' method
def get_employee(empid):    
    data=json.dumps(Employee.get_employee(empid))   #json.dumps enables the output to be in the string format
    response=Response(data,status=200,mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['PUT'])    #route to retrieve the details of a particular employee using the empid thorugh the 'PUT' method
def update_employee(empid):
    request_data = request.get_json() #.get_json parses the incoming json data and returns it
    Employee.update_employee(empid, request_data['name'], request_data['email'])       #the new details obtained through the user are updated                     
    response = Response("Employee Updated", status=200, mimetype='application/json')
    return response     

@app.route('/employee', methods=['GET'])    #route to get the details of all the employees
def get_employees():    #Function to get all the employees in the database
    return jsonify({'Employees': Employee.get_all_employees()}) #returns all the employees by calling the get_all_employees() function defined in the Employee class

app.run(debug=True,port=5000)   #runs the deployment server

