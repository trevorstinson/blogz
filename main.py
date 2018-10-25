from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:antennae-kernel-suchlike-union@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'jKYgF}8gqmcJgzxA'





class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='blog.owner_id')
    

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


@app.route('/')
def send_to_index():
    return redirect('/blog')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_username = request.form['login-username']
        login_password = request.form['login-password']
        user = User.query.filter_by(username=login_username).first()

        if not user:
            username_error = "Username does not exist."
            return render_template('login.html', username_error=username_error, username='')
        elif not check_pw_hash(login_password, user.pw_hash):
            password_error = "Incorrect password."
            return render_template('login.html', password_error=password_error, username=login_username)
        else:
            session['username'] = login_username
            return redirect('/')


    return render_template('login.html')



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')



@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'GET':
        return render_template('signup.html', title="Sign Up")

    if request.method == 'POST':
        # Get info from filled form
        new_username = request.form['new-username']
        new_password = request.form['new-password']
        new_password_verify = request.form['new-password-verify']

        # Set blank errors to avoid crashing
        username_error = ''
        password_error = ''
        verify_error = ''

        # Set error message for empty username
        if new_username == '':
            username_error = 'Please enter a valid username.'
        elif len(new_username) <= 3:
            username_error = 'Please enter a username with 4 or more characters.'
        # Set error message for non-matching verification
        if new_password != new_password_verify or new_password_verify == '':
            verify_error = "Please verify your password."
            password_error = 'Please reenter your password.'
        # Set error message for empty password
        if new_password == '':
            password_error = 'Please enter a valid password.'
        elif len(new_password) <= 3:
            password_error = 'Please enter a password with 4 or more characters.'

        # Get any user with same username from database
        user_exists = User.query.filter_by(username=new_username).first()

        if user_exists:
            username_error = 'This username is already taken.'


        # Reload on same page if either field was empty
        if username_error or password_error or verify_error:
            return render_template('/signup.html', title="Sign Up", new_username=new_username, 
                    username_error=username_error, password_error=password_error, verify_error=verify_error)

        # If all fields were filled, add new post to database
        new_user = User(new_username, new_password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        # flash("Logged in")

        # Then redirect to new post page
        return redirect('/newpost')



@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'GET':
        post_id = request.args.get('id')

        if post_id == None:
            # Get all blogposts and render a reverse-chronological listing by ID
            blogposts = Blog.query.order_by("id desc").all()
            return render_template('index.html', title="It's-a Me, Blogio",
                blogposts=blogposts, index_active="active")

        if post_id != None:
            # Get single blogpost by id and render its page
            blogpost = Blog.query.filter_by(id=post_id).first()
            return render_template('post.html', title="It's-a Me, Blogio",
                blogpost=blogpost)
    



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('newpost.html', title="Let's Make a Post", newpost_active="active")

    if request.method == 'POST':
        # Get info from filled form
        new_title = request.form['blog-post-title']
        new_body = request.form['blog-post-body']

    # Set error message for empty title or body
    if new_title == '':
        flash('Your post needs a name.', 'title-error')
    if new_body == '':
        flash("You didn't write anything!", 'body-error')



    # Redirect back to /newpost if either field was empty
    if new_title == '' or new_body == '':

        # Save any content that *was* added to form
        if new_title != '':
            flash(new_title, 'title-extant')
        if new_body != '':
            flash(new_body, 'body-extant')

        return redirect('/newpost')

    # If all fields were filled, add new post to database
    new_post = Blog(new_title, new_body)
    db.session.add(new_post)
    db.session.commit()

    # Then redirect to page of new post
    return redirect('/blog?id={0}'.format(new_post.id))



if __name__ == '__main__':
    app.run()
