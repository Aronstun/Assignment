from flask import Flask,jsonify,request,json #importing classes
from flask_pymongo import PyMongo #importing PyMongo class that manages MongoDB connections to the Flask app

app=Flask(__name__) #creating an instance of Flask
app.config['MONGO_URI']='mongodb://localhost:27017/Employees' #URI connection to the database

mongo=PyMongo(app) #PyMongo connects to the MongoDB server running on port 27017 on localhost, to the database named Employees. 
ab=mongo.db.Employees #Employees database is exposed as the db attribute.


@app.route('/employee', methods=['POST']) #route to add an employee to the databse using the 'POST' method
def add_employee(): #function definition to add the employee
    empid=request.json['empid']
    name=request.json['name']   #empid, name and email are taken as inputs from the user and stored in the respective variables
    email=request.json['email']
    ab.insert_one({'empid':empid, 'name':name, 'email':email}) #inserting the document into the employee collection
    return "Employee Added" 

@app.route('/employee', methods=['GET']) #route to retrieve all the employees from the database using the 'GET' method
def get_employees(): #function definition to get the details of all the employees
    employee=list() #creating an empty list
    for x in ab.find():
        employee.append({'empid':x['empid'],'name':x['name'],'email':x['email']}) #all the employee documents in the database are retrieved and appened to the employee list
    return jsonify(employee)

@app.route('/employee/<empid>', methods=['GET']) #route to retrieve a particular employee from the database by passing the empid using the 'GET' method
def get_employee(empid): #function to get the details of a particular employee
    data=ab.find_one({"empid":empid}) #find_one checks if the employee with empid exists in the databse
    if data: #if the employee exists, then the details of that particular employee are retreived
        return jsonify({'empid':data['empid'],'name':data['name'],'email':data['email']})
    else:
        return "Employee not found!" #if the employee doesn't exist in the database, then the message "Employee not found!" is returned

@app.route('/employee/<empid>',methods=['DELETE']) #route to delete a particular employee from the database by passing the empid using the 'DELETE' method
def delete_employee(empid): #function to delete a particular employee from the database
    data=ab.find_one({"empid":empid}) #find_one checks if the employee with empid exists in the databse
    if data: #if the employee exists, then the particular employee is deleted from the database
        ab.delete_one({"empid":empid})
        return "Employee Deleted" #if the employee doesn't exist in the database, then the message "Employee not found!" is returned
    else:
        return "Employee not found!"
    
@app.route('/employee/<empid>',methods=['PUT']) #route to update a particular employee from the database by passing the empid using the 'PUT' method
def update_employee(empid): #function to update a particular employee in the database
    data=ab.find_one({"empid":empid}) #find_one checks if the employee with empid exists in the databse
    if data: #if the particular employee exists, then the following actions take place
        uname=request.json['name'] #details to be updated are taken from the user
        uemail=request.json['email']
        ab.update_one({"empid":empid}, {"$set": {"name":uname,"email":uemail}}, upsert=False) #These fields are then updated in the database pertaining to that employee
        return "Employee Updated" #success message is returned
    else:
        return "Employee not found!" #if the employee doesn't exist in the database, then the message "Employee not found!" is returned

if __name__=='__main__':
    app.run(debug=True)
