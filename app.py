"""Blogly application."""

from flask  import Flask, render_template, request, flash, jsonify, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, Post_Tag
from datetime import date

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

@app.route('/users/<int:id>/posts/new/', methods=['GET', 'POST'])
def show_add_form_post(id):
    user=User.query.get(id)
    tags = Tag.query.all()
    if request.method == 'GET':
        return render_template('/new_post_form.html', title='New post', user=user,tags=tags)
    else:
        new_post = Post(title = request.form['title'],
                        content = request.form['content'],
                        created_at = date.today(),
                        user_id = id)
        db.session.add(new_post)
        db.session.commit()
        for tag in request.form.getlist('post_tags'):
            new_post_tag = Post_Tag(post_id=new_post.id,
                                    tag_id=tag)
            db.session.add(new_post_tag)
            db.session.commit()
        
        
    return render_template('/user_details.html', title='User details', user=user)

@app.route('/posts/<int:post_id>/')
def show_post(post_id):
    post=Post.query.get(post_id)
    user=User.query.get(post.user_id)
    return render_template('/post_details.html', title='Post details', post=post, user=user)


@app.route('/posts/<int:post_id>/delete/', methods=['POST'])
def delete_post(post_id):
    post=Post.query.get(post_id)
    user=User.query.get(post.user_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return render_template('/user_details.html', title='User details', user=user)

@app.route('/posts/<int:post_id>/edit/')
def edit_post(post_id):
    post=Post.query.get(post_id)
    tags=Tag.query.all()
    return render_template('/edit_post.html', title='Edit post', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit/', methods=['POST'])
def save_post_edits(post_id):
    post=Post.query.get(post_id)
    user=User.query.get(post.user_id)    
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    Post_Tag.query.filter_by(post_id=post_id).delete()
    for tag in request.form.getlist('post_tags'):
            new_post_tag = Post_Tag(post_id=post_id,
                                    tag_id=tag)
            db.session.add(new_post_tag)
    db.session.commit()
    return render_template('/user_details.html', title='User details', user=user)

@app.route('/tags/')
def show_tag_list():
    tags=Tag.query.all()
    return render_template('tags.html', title="Tags list", tags=tags)

@app.route('/tags/<int:id>/')
def show_tag(id):
    tag=Tag.query.get(id)
    return render_template('tag_details.html', title='Tag details', tag=tag)

@app.route('/tags/new/')
def show_add_tag_form():
    return render_template('add_or_create_tag.html', title='Add a tag')

@app.route('/tags/new/', methods=['POST'])
def add_new_tag():
    new_tag = Tag(name=request.form['name'])
    db.session.add(new_tag)
    db.session.commit()
    tags=Tag.query.all()
    return render_template('tags.html', title='Tags list', tags=tags)

@app.route('/tags/<int:id>/edit/', methods=['GET'])
def show_edit_tag_form(id):
    tag=Tag.query.get(id)
    return render_template('add_or_create_tag.html', title='Edit a tag', tag=tag)

@app.route('/tags/<int:id>/edit/', methods=['POST'])
def save_tag_updates(id):
    tag=Tag.query.get(id)
    tag.name=request.form['name']
    db.session.add(tag)
    db.session.commit()
    tags=Tag.query.all()
    return render_template('tags.html', title='Tags list', tags=tags)

@app.route('/tags/<int:id>/delete/', methods=['POST'])
def delete_tag(id):
    Post_Tag.query.filter_by(tag_id=id).delete()
    Tag.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/tags/')

    





    


