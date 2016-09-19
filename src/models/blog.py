import uuid
import datetime
from src.common.database import Database
from src.models.post import Post

__author__ = 'Qingyun Wu'


class Blog(object):
	# in default, the blog id will be automatically created by uuid.uudi4().hex
	def __init__(self, author, title, description, author_id, _id=None):
		self.author = author
		self.author_id = author_id
		self.title = title
		self.description = description
		self._id = uuid.uuid4().hex if _id is None else _id

	def new_post(self, title, content, date=datetime.datetime.utcnow()):
		post = Post(blog_id=self._id,
					title=title,
					content=content,
					author=self.author,
					created_date=date)
		post.save_to_mongo()

	# return all the posts of the blog by blog_id
	def get_posts(self):
		return Post.from_blog(self._id)

	def save_to_mongo(self):
		Database.insert(collection='blogs',
						data=self.json())
	# convert a blog obj to a json obj
	def json(self):
		return {
			'author': self.author,
			'author_id': self.author_id,
			'title': self.title,
			'description': self.description,
			'_id': self._id
		}
	# return a blog obj from MongoDB by blog _id
	@classmethod
	def from_mongo(cls, _id):
		blog_data = Database.find_one(collection='blogs',
									  query={'_id': _id})
		return cls(**blog_data)

	# return all blogs objs from MongoDB by author_id
	@classmethod
	def find_by_author_id(cls, author_id):
		blogs = Database.find(collection='blogs',
							  query={'author_id': author_id})
		return [cls(**blog) for blog in blogs]