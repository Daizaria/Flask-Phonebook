 # flask(framework), render a template so we can get ride of string text
from flask import Flask, render_template, request, redirect, url_for      
from flask_sqlalchemy import SQLAlchemy #library

app = Flask(__name__)
# '///' relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # path name to database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)     # for each entry, makes a column. Make each item special
    title = db.Column(db.String(100))  #max chars type in
    complete = db.Column(db.Boolean)  # keep track of items completed

#if we want to add something to the site or url, we have to add a new function
@app.route('/')
def index(): # shows our list = query 
    # show all todos
    contact_list = Contact.query.all()  #returns list of items from our database
    print(contact_list)
    return render_template('base.html', contact_list= contact_list) # allows us to use the template, and access the todo list

# we want to make a route to our update and delete option
@app.route('/add', methods=['POST']) #fixed route
def add():
    # add new item
    title = request.form.get('title')  #getting info html
    new_contact = Contact(title=title, complete=False)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('index')) #direct user to index page

@app.route("/update/<int:contact_id>", methods=["POST","GET"])
def update(contact_id): #contact variable added in html
#     #updates new item
    contact = Contact.query.filter_by(id=contact_id).first()
    #todo_update = Todo.query.get_OR_404(todo_id)

    if request.method == "POST":
        #todo_update.title = request.form['title']
        contact.title = request.form['title']
        try:
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return 'There was an issue while updating that task'
    else:
        #return render_template('update.html', contact_update=contact_update)
        return render_template('update.html', contact=contact)
    
    
  

@app.route('/delete/<int:todo_id>') 
def delete(contact_id):
    contact = Contact.query.filter_by(id=contact_id).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index')) #updates the action to homepage


if __name__ == '__main__':
    db.create_all()  #create database
    # SQLAlchemy.create_all()

    # new_todo = Todo(title='todo 1', complete=False)
    # db.session.add(new_todo)
    # db.session.commit()

    app.run(host ='0.0.0.0', port = 5000, debug = True) 