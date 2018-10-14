from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:grUwWx+rVv6jHEwr=EKAkaaU2cRkxU@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)





class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def send_to_index():
    return redirect('/blog')



@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        new_title = request.form['blog-post-title']
        new_body = request.form['blog-post-body']
        new_post = Blog(new_title, new_body)
        db.session.add(new_post)
        db.session.commit()

    blogposts = Blog.query.all()
    return render_template('index.html', title="Blog Posts",
        blogposts=blogposts, index_active="active")



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    return render_template('newpost.html', title="Let's Make a Post", newpost_active="active")



if __name__ == '__main__':
    app.run()
