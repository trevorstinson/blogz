from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:grUwWx+rVv6jHEwr=EKAkaaU2cRkxU@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)





class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120000))

    def __init__(self, title, body):
        self.title = title
        self.body = body





@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        new_title = request.form['post-title']
        new_body = request.form['post-body']
        new_post = Post(new_title, new_body)
        db.session.add(new_post)
        db.session.commit()

    blogposts = Post.query.all()
    return render_template('index.html', title="It's-a Me, Blogio",
        blogposts=blogposts)





if __name__ == '__main__':
    app.run()
