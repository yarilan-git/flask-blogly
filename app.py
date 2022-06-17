"""Blogly application."""

from flask  import Flask, render_template, request, flash, jsonify, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config["SECRET_KEY"] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def show_users():
    """ Show existing users """
    users = User.query.all()
    return render_template('users.html', title="Users", users=users)
    

@app.route('/users/new/', methods=['GET'])
def show_user_form():
    """ Display an empty new user form """
    return render_template('create_user.html', title='Add user')

@app.route('/users/new/', methods=['POST'])
def add_user():
    """ Insert a new user to the database """
    new_user = User(first_name=request.form['f_name'],
                    last_name=request.form['l_name'],
                    image_url=request.form['image_url'])
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:id>/', methods=['GET'])
def show_user_details(id):
    """ Show the details of an existing user, view only """
    user=User.query.get(id)
    return render_template('/user_details.html', title='User details', user=user)

@app.route('/users/<int:id>/edit/', methods = ['POST'])
def show_user_edit_page(id):
    """ Show the details of an existing user, and allow updating them """
    user=User.query.get(id)
    return render_template('/update_user.html', title='Edit user', user=user)

@app.route('/users/<int:id>/delete/', methods=['POST'])
def delete_user(id):   
    """ Delete a user and show the remaining users """ 
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')
    
@app.route('/users/<int:id>/save_edits/', methods=['POST'])
def save_edits(id):   
    """ Save in the database any updates made to a user, and show all users """
    user=User.query.get(id)
    user.first_name = request.form['f_name']
    user.last_name = request.form['l_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect('/')
    


