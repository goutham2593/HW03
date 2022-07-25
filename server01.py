#!/usr/bin/python3

# standard library
import sqlite3 as sql

# python3 -m pip install flask
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# Main page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addrec',methods = ['POST'])
def addrec():
    try:
        nm = request.form['nm']         # student name
        grd = request.form['grd']     # student grade
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            # Query
            cur.execute("INSERT INTO students (name,grade) VALUES (?,?)",(nm,grd) )
            # Execute
            con.commit()
        # notifier message
        msg = "Record successfully added"
        
    except:
        con.rollback()  # incase of failure
        msg = "error in insert operation"    #message

    finally:
        con.close()     # close connection
        return render_template("home.html",msg = msg)
    
#delete record
@app.route('/delrec',methods = ['POST'])
def delrec():
    try:
        sid = request.form['id']         # student id
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE from students where id = ? ",(sid))
            con.commit()
        msg = "Record successfully Deleted"
        
    except:
        con.rollback()  
        msg = "error in delete operation"

    finally:
        con.close()
        return render_template("home.html",msg = msg)    #

#Bonus part: Update record
@app.route('/updrec',methods = ['POST'])
def updrec():
    try:
        sid = request.form['id']         # student id
        name = request.form['name']     # student name
        grade = request.form['grade']
        
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE students set name = ?, grade = ? where id = ? ",(name,grade,sid))
            con.commit()

        msg = "Record updated successfully"
        
    except:
        con.rollback() 
        msg = "error in update operation"

    finally:
        con.close()
        return render_template("home.html",msg = msg)


# List of all students into result page
@app.route('/lista')
def list_students():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from students")           # get all information from the students
    
    rows = cur.fetchall()
    return render_template("result.html",rows = rows)


# List of all students who have grade more then 85 into result page
@app.route('/listp')
def list_students_pass():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from students where grade > 84")           # get all information from students
    
    rows = cur.fetchall()
    return render_template("result.html",rows = rows)

if __name__ == '__main__':
    try:
        # ensure the sqliteDB is created
        con = sql.connect('database.db')
        print("Database connectivity is OK")
        #con.execute('DROP TABLE students')
        con.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, grade TEXT)')
        print("Table created successfully")
        con.close()
        # begin Flask Application 
        app.run(host="0.0.0.0", port=2224, debug = True)
    except:
        print("Error Running application")

