from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:grUwWx+rVv6jHEwr=EKAkaaU2cRkxU@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)





@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['post-title']
        new_post = Post(new_title, new_content)
        db.session.add(new_post)
        db.session.commit()

    posts = Post.query.all()
    return render_template('index.html', title="It's a-Blogio",
        posts=posts)





if __name__ == '__main__':
    app.run()
