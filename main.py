from firebase import firebase
import json
import pprint


firebase = firebase.FirebaseApplication('https://retroactive-d25de.firebaseio.com')

def get_all_posts (): 
	return firebase.get('/posts', None)

def get_posts_with_emotion (emotion): 
	posts = firebase.get('/posts', None)
	specific_posts = [] 

	for post in posts: 
		if post['emotion'] == emotion: 
			specific_posts.append(post) 

	return specific_posts
 
def add_post (text, emotion, num_of_likes = 0): 
	posts = firebase.get('/posts', None)
	firebase.put('posts', len(posts), {"text": text, "emotion": emotion, "num_of_likes": num_of_likes})

def add_like(index):
	post = firebase.get('/posts/' + str(index), None)

	if post:
		firebase.delete('/posts', index)
		firebase.put('posts', index, {"text": post['text'], "emotion": post['emotion'], "num_of_likes": post['num_of_likes'] + 1})

# pprint.pprint(get_all_posts())

#add_post("testing the add to the post list", 2, 1)
pprint.pprint(patch_test())