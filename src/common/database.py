__author__ = 'Qingyun Wu'

from pymongo import MongoClient


class Database(object):
	URI = "mongodb://127.0.0.1:27017"
	DATABASE = None

	@staticmethod
	def initialize():
		# set up a client connected to MongoDB on host
		client = MongoClient(Database.URI)
		# this will create a database in MongoDB if non-exists
		Database.DATABASE = client["fullstack"]

	@staticmethod
	def insert(collection, data):
		Database.DATABASE[collection].insert(data)
	# return a cursor
	@staticmethod
	def find(collection, query):
		return Database.DATABASE[collection].find(query)
	# return the first json obj, not a cursor
	@staticmethod
	def find_one(collection, query):
		return Database.DATABASE[collection].find_one(query)