 # flask(framework), render a template so we can get ride of string text
from flask import Flask, render_template, request, redirect, url_for      
from flask_sqlalchemy import SQLAlchemy #library

app = Flask(__name__)
# '///' relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # path name to database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)     # for each entry, makes a column. Make each item special
    title = db.Column(db.String(100))  #max chars type in
    complete = db.Column(db.Boolean)  # keep track if item completed

#if we want to add something to the site or url, we have to add a new function
@app.route('/')
def index(): # shows our list = query 
    # show all todos
    todo_list = Todo.query.all()  #returns list of items from our database
    print(todo_list)
    return render_template('base.html', todo_list= todo_list) # allows us to use the template, and access the todo list

# we want to make a route to our update and delete option
@app.route('/add', methods=['POST']) #fixed route
def add():
    # add new item
    title = request.form.get('title')  #getting info html
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index')) #direct user to index page

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit() #making changes
    return redirect(url_for('index'))
  

@app.route('/delete/<int:todo_id>') 
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index')) #updates the action to homepage


if __name__ == '__main__':
    db.create_all()  #create database

    # new_todo = Todo(title='todo 1', complete=False)
    # db.session.add(new_todo)
    # db.session.commit()

    app.run(debug=True)