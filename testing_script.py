from instaloader import Instaloader, Post, Profile, load_structure_from_file
import time
from datetime import datetime
import json
from bson import json_util
import collections

data_json_file = ()
with open("userlist_instaloaders.json", 'r') as f:
	data_json_file = json.loads(f.read())

time.sleep(5) 

L = Instaloader()
username = "caliwuras"
password = "tujuh117"
L.login(username, password) 

try:
	L.load_session_from_file(username)
except FileNotFoundError:
	L.context.log("Session file does not exist yet - Logging in.")
if not L.context.is_logged_in:
	L.interactive_login(username)
	L.save_session_to_file()

for loop_userlist in data_json_file:
	profiles = Profile.from_username(L.context, loop_userlist)

	json_data = []
	for post in profiles.get_posts():
		vals = {
			"id" : post.owner_id,
			"user" : post.profile,
			"image_url" : post.url,
			"date" : str(post.date.date()),
			"time" : str(post.date.time()),
			"unix_timestamp" : datetime.timestamp(post.date),
			"post_location" : post.location,
			"hashtags" : post.caption_hashtags,
			"raw_text" : post.caption,
			"comments_count" : post.comments,
			"likes_count" : post.likes,
			"followers_count" : profiles.followers,
			"following_count" : profiles.followees,
			# "code" : ,	
		}
		print(json.dumps(vals, indent=4))
		print ("")
		json_data.append(vals)

	with open(loop_userlist+'.json', 'w') as write_json:
		# for loop_data in json_data:
		json.dump(json_data, write_json, indent=4)
		# json_data.append(node_dict)

