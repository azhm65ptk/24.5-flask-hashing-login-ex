
from flask import Flask, render_template, redirect, session

from models import connect_db, db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import FeedbackForm, RegisterForm, LoginForm
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback_ex"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
    " home page is sign up page "
    return redirect ('/register')


@app.route('/register',methods=["GET", "POST"])
def register():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name=form.first_name.data
        last_name=form.last_name.data 
        email=form.email.data

        user=User.register(username,password,email,first_name, last_name)

        db.session.commit()
        session['username']=user.username

        return redirect(f"/users/{user.username}")
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    '''login form to handle login'''
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    form= LoginForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user= User.authenticate(username, password)

        if user:
            session['username']=user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors=['Invalid Username or password']
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    '''log out'''
    session.pop("username")
    return redirect('/')


@app.route('/users/<username>')
def show_user(username):
    ''' example page for log-in-user'''

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user=User.query.get(username)

    return render_template("show.html",user=user)

@app.route('/users/<username>/delete', methods=["POST"])
def remove_user(username):
    '''remove user and redirect to login page'''

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user=User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/register')



@app.route('/users/<username>/feedback/new', methods=["GET","POST"])
def add_new_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form=FeedbackForm()

    if form.validate_on_submit():
        title=form.title.data
        content= form.content.data

        feedback= Feedback(title=title, content=content, username= username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("newfeedback.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET","POST"])
def update_feedback(feedback_id):
    '''show update feedback form '''

    
    feedback=Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form=FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title=form.title.data
        feedback.content=form.content.data
        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    return render_template('editfeedback.html', form=form , feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=["GET","POST"])
def delete_feedback(feedback_id):
    '''delete feedback'''

    

    feedback=Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.username}')
