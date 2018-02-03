import csv
import json
import sys

#add enum for emotions here 
# 0 - happy 
# 1 - meh 
# 2 - sad 

class Post: 

	def __init__(self, text, emotion, num_of_likes):
		self.text = text 
		self.emotion = emotion 
		self.num_of_likes = num_of_likes

	@property 
	def text(self):
		return self.text

	@property
	def emotion(self):
		return self.emotion 

	@property
	def num_of_likes(self):
		return self.num_of_likes

	def serialize(self):
		return {
			'text': self.text, 
			'emotion': self.emotion,
			'num_of_likes': self.num_of_likes
		}