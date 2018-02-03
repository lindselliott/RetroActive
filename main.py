#!flask/bin/python

from flask import Flask, url_for
from firebase import firebase
import json
import pprint
from datetime import datetime
from post import Post 
from actionItem import ActionItem
import csv 
import requests

app = Flask(__name__)
firebase = firebase.FirebaseApplication('https://retroactive-d25de.firebaseio.com')

#*************************************************************************** export to csv

@app.route('/export', methods=['GET'])
def export_to_csv():
	current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	file_name = 'exported/Test.csv'
	with open(file_name, 'wb') as csv_file:
		wr = csv.writer(csv_file, delimiter=',')
		# action_items_csv = actions_items_export(test_file)
		_write_action_items_to_csv(wr)
		wr.writerow([])
		_write_posts_to_csv(wr)

	
	
def _write_posts_to_csv(wr): 
	posts = json.loads(get_all_posts())

	wr.writerow(['Posts'])
	wr.writerow([
		"Text",
		"Emotion",
		"Number of Likes"])

	for post in posts: 
		post_obj = Post(
			text = post['text'],
			emotion = post['emotion'],
			num_of_likes = post['num_of_likes'])
		wr.writerow([
			post_obj.text,
			post_obj.emotion,
			post_obj.num_of_likes])


def _write_action_items_to_csv(wr): 
	action_items = json.loads(get_all_action_items())

	wr.writerow(['Action Items'])
	wr.writerow([
		"Written By",
		"Assigned To",
		"Start Date",
		"End Date",
		"Task",
		"Completed"])

	for action_item in action_items: 
		action_obj = ActionItem(
			owner = action_item['owner'],
			assigned_to = action_item['assigned_to'],
			start_date = action_item['start_date'],
			end_date = action_item['end_date'],
			task = action_item['task'],
			completed = action_item['completed'])
		wr.writerow([
			action_obj.owner,
			action_obj.assigned_to,
			action_obj.start_date,
			action_obj.end_date,
			action_obj.task,
			action_obj.completed])

#******************************************************************** ACTIONITEMS

@app.route('/action_items', methods=['GET'])
def get_all_action_items():
	return json.dumps(firebase.get('/action_items', None))

@app.route('/action_items_progress/<int:finished>', methods=['GET'])
def get_action_item_for_progress(finished):
	actionItems = firebase.get('/action_items', None)
	found_actions = [] 

	for actionItem in actionItems: 
		if actionItem['completed'] == finished: 
			found_actions.append(actionItem)

	return json.dumps(found_actions)

# get action items by assigned name
@app.route('/action_items_for/<string:name>', methods=['GET'])
def get_action_items_by_assigned_to(name):
	actionItems = firebase.get('/action_items', None)

	found_actions = [] 

	for actionItem in actionItems: 
		if actionItem['assigned_to'] == name: 
			found_actions.append(actionItem)

	return json.dumps(found_actions)

# get action items by owner name
@app.route('/action_items_by/<string:name>', methods=['GET'])
def get_action_items_by_owner(name):
	actionItems = firebase.get('/action_items', None)

	found_actions = [] 

	for actionItem in actionItems: 
		if actionItem['owner'] == name: 
			found_actions.append(actionItem)

	return json.dumps(found_actions)

def complete_action_item(index):
	action_item = firebase.get('/action_items/' + str(index), None)
	if action_item:
		action_item_obj = ActionItem(
			owner = action_item['owner'],
			assigned_to = action_item['assigned_to'],
			start_date = action_item['start_date'],
			end_date = action_item['end_date'],
			task = action_item['task'],
			completed = True)

		# action_item_ser = action_item_obj.serialize()
		firebase.delete('/action_items', index)
		firebase.put(
			'action_items', 
			str(index), 
			action_item_obj.serialize())

def create_action_item(owner, assigned_to, start_date, end_date, task, completed):
	action_items = firebase.get('/action_items', None)

	length = 0
	if action_items:
		length = len(action_items)

	action_item = ActionItem (
		owner = owner,
		assigned_to = assigned_to,
		start_date = start_date,
		end_date = end_date,
		task = task,
		completed = completed)

	firebase.put(
		'action_items', 
		str(length), 
		action_item.serialize())

def delete_all_action_items():
	return firebase.delete('/action_items', None)

def delete_specific_post(index):
	return firebase.delete('/action_items', index)	

# ***************************************************************************** POSTS 

@app.route('/posts', methods=['GET', 'POST'])
def get_all_posts (): 
	return json.dumps(firebase.get('/posts', None))

@app.route('/posts/<int:emotion>', methods=['GET'])
def get_posts_with_emotion (emotion): 
	posts = firebase.get('/posts', None)
	specific_posts = [] 

	for post in posts: 
		if post['emotion'] == emotion: 
			specific_posts.append(post) 

	return json.dumps(specific_posts)

@app.route("/posts/add/<string:text>,<int:emotion>,<int:num_of_likes>", methods = ['GET', 'POST'])
def add_post (text, emotion, num_of_likes):
	posts = firebase.get('/posts', None)
	firebase.put('posts', len(posts), {"text": text, "emotion": emotion, "num_of_likes": num_of_likes})

	return json.dumps(firebase.get('/posts', None))

@app.route("/posts/like/<int:index>", methods = ['GET', 'POST'])
def add_like(index):
	post = firebase.get('/posts/' + str(index), None)

	if post:
		post_obj = Post(
			text = post['text'],
			emotion = post['emotion'],
			num_of_likes = post['num_of_likes'] + 1)

		firebase.delete('/posts', index)
		firebase.put(
			'posts', 
			str(index), 
			post_obj.serialize())

	return json.dumps(firebase.get('/posts', None))

def delete_all_posts():
	return firebase.delete('/posts', None)

def delete_specific_post(index):
	return firebase.delete('/posts', index)




# export_to_csv()
create_action_item(owner = 'lelliott', 
				   assigned_to = 'lelliott', 
				   start_date = '02/03/2018', 
				   end_date = '02/04/2018', 
				   task = "Do this action item", 
				   completed = False)
#complete_action_item(0)

if __name__ == '__main__':
	app.run(debug=True)