import uuid

import datetime

from src.common.database import Database

__author__ = 'Qingyun Wu'


class Post:

	def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
		self.blog_id = blog_id
		self.title = title
		self.content = content
		self.author = author
		self.created_date = created_date
		# create an _id if not specified
		self._id = uuid.uuid4().hex if _id is None else _id

	def save_to_mongo(self):
		Database.insert(collection='posts',
						data=self.json())

	def json(self):
		return {
			"_id": self._id,
			"blog_id": self.blog_id,
			"author": self.author,
			"content": self.content,
			"title": self.title,
			"created_date": self.created_date
		}

	# retrieve a post from mongoDB by _id, return a post Obj
	@classmethod
	def from_mongo(cls, id):
		post_data = Database.find_one(collection='posts', query={'_id':id})
		return cls(**post_data)

	# return all the posts from a blog by blog_id
	@classmethod
	def from_blog(cls, blog_id):
		posts_data = Database.find(collection='posts', query={'blog_id': blog_id})
		return [post for post in posts_data]