from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User
from flask import Flask, render_template, request, session, make_response

__author__ = 'Qingyun Wu'


app = Flask(__name__)  # '__main__'
app.secret_key = "qingyun"


@app.route('/')
def home_template():
	return render_template('home.html')

@app.route('/login')
def login_template():
	session['email'] = None
	return render_template('login.html')

@app.route('/register')
def register_template():
	return render_template('register.html')

# firstly, connect to the database "fullstack"
@app.before_first_request
def initialize_database():
	Database.initialize()

# post action called from "login.html", if valid, go to "profile.html"
# /auth/login will be the URI suffix
@app.route('/auth/login', methods=['POST'])
def login_user():
	# flask request
	email = request.form['email']
	password = request.form['password']

	if User.login_valid(email, password):
		# if valid, set session to be current user email
		session['email'] = email
	else:
		session['email'] = None
	# pass a email value to "profile.html"
	user = User.get_by_email(session['email'])
	blogs = user.get_blogs()
	return render_template("profile.html", email=session['email'], blogs=blogs)


@app.route('/auth/register', methods=['POST'])
def register_user():
	email = request.form['email']
	password = request.form['password']
	# User.register will do the auth job
	User.register(email, password)
	return render_template("profile.html", email=session['email'])


# @app.route('/blogs/<string:user_id>')
# @app.route('/blogs')
# def user_blogs(user_id=None):
# 	if user_id is not None:
# 		user = User.get_by_id(user_id)
# 	else:
# 		user = User.get_by_email(session['email'])
#
# 	blogs = user.get_blogs()
#
# 	return render_template("user_blogs.html", blogs=blogs, email=user.email)


# /blogs/new can do both post and get jobs, by default is "new_blog.html"
# "new_blog.html" post data to /blogs/new, then new blog saved and turn to user_blog function

@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
	if request.method == 'GET':
		return render_template('new_blog.html')
	else:# post: received post data from 'new_blog.html'
		title = request.form['title']
		description = request.form['description']
		user = User.get_by_email(session['email'])

		new_blog = Blog(user.email, title, description, user._id)
		new_blog.save_to_mongo()
		# make_response is to turn to function user_blog with the value user._id
		blogs = Blog.find_by_author_id(user._id)
		return render_template("profile.html", email=session['email'], blogs=blogs)

# go to posts.html
@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
	blog = Blog.from_mongo(blog_id)
	# get all the posts of the current blog
	posts = blog.get_posts()
	return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)


# create new post
@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
	# default page
	if request.method == 'GET':
		# after the form completion, data is post back to /post/new/<sting:blog_id>
		return render_template('new_post.html', blog_id=blog_id)
	else:
		# when received data post by 'new_post.html'
		title = request.form['title']
		content = request.form['content']
		user = User.get_by_email(session['email'])

		new_post = Post(blog_id, title, content, user.email)
		new_post.save_to_mongo()
		# turn to function blogs_posts
		return make_response(blog_posts(blog_id))


if __name__ == '__main__':
	app.run(port=9295, debug=True)
