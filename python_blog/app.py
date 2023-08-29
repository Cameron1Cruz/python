# Import the Flask, sqlite3, Werkzeug library
from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

# Create a database connection and return it
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Provide a post_id to determine what blog post to return
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# Create the Flask instance and pass the Flask
app = Flask(__name__)
# Set a secret key
app.config['SECRET_KEY'] = 'your secret key'

# Default route added using a decorator, for view function 'index'
# Landing page of my web application - index.html
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Page of specific posts ID'd by the post_id in url
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

# View function that will render a template that shows a form
# you can fill in to create a new blog post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

# Start with flask web app, with debug as True
if (__name__) == "__main__":
    app.run(debug=True)
