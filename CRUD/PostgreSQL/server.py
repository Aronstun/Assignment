from urllib import response
from flask import Flask, request, Response, jsonify #importing libraries
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__) #creating an instance of the Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost/Employees'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

# the class Employee will inherit the db.Model of SQLAlchemy
class Employee(db.Model):
    __tablename__ = 'employees'  # creating a table name
    empid = db.Column(db.Integer, primary_key=True)  # this is the primary key
    name = db.Column(db.String(80), nullable=False)
    # nullable is false so the column can't be empty
    email=db.Column(db.String(30), nullable=False)


    #Function to display the output as JSON
    def json(self):
        return {'emp_id': self.empid, 'name': self.name, 'email':self.email}

    #Function to add employee to the database
    def add_employee(_name, _email):
        '''function to add employee to database using _name, _email'''
        # creating an instance of Employee constructor
        new_employee = Employee(name=_name, email=_email)
        db.session.add(new_employee)  # add new movie to database session
        db.session.commit()  # commit changes to session

    #Function to get all the employees in the database
    def get_all_employees():
        '''function to get all employees in the database'''
        return [Employee.json(employee) for employee in Employee.query.all()]

    #Function to get an employee in the database with the emp_id as a parameter.
    def get_employee(_empid):
        '''function to get movie using the id of the movie as parameter'''
        data=Employee.query.filter_by(empid=_empid)
        if data.count():
            return Employee.json(Employee.query.filter_by(empid=_empid).first())
        else:
            return "Employee not found"
        # Movie.json() coverts our output to the json format defined earlier
        # the filter_by method filters the query by the id
        # since our id is unique we will only get one result
        # the .first() method will get that first value returned

    #Function to update an employee in the database. 
    #After we filter by emp_id, we will update the name and email of the employee and then commit the changes.
    def update_employee(_empid, _name,_email):
        '''function to update the details of an employee using the empid, name and email as parameters'''
        employee_update = Employee.query.filter_by(empid=_empid).first()
        employee_update.name = _name
        employee_update.email = _email
        db.session.commit()

    #Function to delete the employee from the database. We will filter by the id and the .delete() method will delete the movie.
    def delete_employee(_empid):
        '''function to delete an employee from the database using the empid of the employee as a parameter'''
        data=Employee.query.filter_by(empid=_empid)
        if data.count():
            data.delete()
            db.session.commit()
            return "Employee deleted"
        else:
            return "Employee not found"
        

db.create_all()

@app.route('/employee', methods=['POST'])
def add_employee():
    '''Function to add new movie to our database'''
    request_data = request.get_json()  # getting data from client
    Employee.add_employee(request_data["name"],request_data["email"])
    response = Response("Employee added", 201, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['DELETE'])
def remove_employee(empid):
    '''Function to delete movie from our database'''
    del_msg=Employee.delete_employee(empid)
    response = Response(del_msg, status=200, mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['GET'])
def get_employee(empid):
    data=json.dumps(Employee.get_employee(empid))
    response=Response(data,status=200,mimetype='application/json')
    return response

@app.route('/employee/<int:empid>', methods=['PUT'])
def update_employee(empid):
    request_data = request.get_json()
    Employee.update_employee(empid, request_data['name'], request_data['email'])                            
    response = Response("Employee Updated", status=200, mimetype='application/json')
    return response     

@app.route('/employee', methods=['GET'])
def get_employees():
    '''Function to get all the movies in the database'''
    return jsonify({'Employees': Employee.get_all_employees()})

app.run(debug=True,port=5000)
