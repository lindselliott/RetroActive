import csv
import json
import sys

#add enum for emotions here 


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

	# def format_to_csv(self, file):
	# 	output = csv.writer(file, delimiter=',')
	# 	#output.writerow(self[0].keys())  # header row

	# 	import pdb; pdb.set_trace()
	# 	output.writerow(list(self))