import datetime
import uuid
from flask import session
from src.common.database import Database
from src.models.blog import Blog

__author__ = 'Qingyun Wu'


class User(object):
	def __init__(self, email, password, _id=None):
		self.email = email
		self.password = password
		self._id = uuid.uuid4().hex if _id is None else _id

	@classmethod
	def get_by_email(cls, email):
		data = Database.find_one(collection="users", query={"email": email})
		if data is not None:
			return cls(**data)

	# return a user obj by its _id
	@classmethod
	def get_by_id(cls, _id):
		data = Database.find_one(collection="users", query={"_id": _id})
		if data is not None:
			return cls(**data)

	# check whether a login is valid
	@staticmethod
	def login_valid(email, password):
		# Check whether a user's email matches the password they sent us
		user = User.get_by_email(email)
		if user is not None:
			# Check the password
			return user.password == password
		return False

	@staticmethod
	def register(email, password):
		user = User.get_by_email(email)
		if user is None:
			# User doesn't exist, so we can create one, cls means User
			new_user = User(email, password)
			new_user.save_to_mongo()
			# set the session to be the new user created
			session['email'] = email
			return True
		else:
			# User exists :(
			return False

	@staticmethod
	def login(user_email):
		# login_valid has already been called
		session['email'] = user_email

	@staticmethod
	def logout():
		session['email'] = None

	# get all the blogs from the current user
	def get_blogs(self):
		return Blog.find_by_author_id(self._id)

	# create a new blog
	def new_blog(self, title, description):
		blog = Blog(author=self.email,
					title=title,
					description=description,
					author_id=self._id)
		blog.save_to_mongo()

	# create new post of this blog
	@staticmethod
	def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
		blog = Blog.from_mongo(blog_id)
		blog.new_post(title=title,
					  content=content,
					  date=date)

	def json(self):
		return {
			"email": self.email,
			"_id": self._id,
			"password": self.password
		}

	# call user.save_to_mongo to save the current user to MongoDB
	def save_to_mongo(self):
		Database.insert("users", self.json())
