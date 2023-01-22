from httpx import ReadTimeout
import os
import json
import datetime
#from geopy.geocoders import Nominatim


import BeFake.BeFake as BeFake
from utils import sec_to_timestamp

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

#DATA_DIR = "BeFake/data"
DATA_DIR = dir_path + "/../BeFake/data"
#TOKEN_PATH = "BeFake/token.txt"
TOKEN_PATH = dir_path + "/../BeFake/token.txt"

OWN_DIR = dir_path


# uses dict like in info.json
class UIPost():
    def __init__(self, data_dict) -> None:
        self.data_dict = data_dict

        self.id = data_dict.get("id", None)
        self.notification_id = data_dict.get("notificationID", None)
        # important
        self.primary_photo = data_dict.get("photoURL", None)
        self.secondary_photo = data_dict.get("secondaryPhotoURL", None)
        self.caption = data_dict.get("caption", None)
        # metadata
        self.public = data_dict.get("isPublic", None)
        self.retakes = data_dict.get("retakeCounter", None)
        self.latitude = data_dict.get("location", {}).get("_latitude", None)
        self.longitude = data_dict.get("location", {}).get("_longitude", None)
        self.location_name = None
        self.location_name = f"{self.latitude}, {self.longitude}"
        """if self.latitude:
            # this seems to take some time
            cur_loc = Nominatim(user_agent="test").reverse((self.latitude, self.longitude)).raw['address']
            if 'city' in cur_loc:
                if 'city_distroct' in cur_loc:
                    self.location_name = f"{cur_loc['city']}, {cur_loc['city_district']}"
                elif 'suburb' in cur_loc:
                    self.location_name = f"{cur_loc['city']}, {cur_loc['suburb']}"
            elif 'village' in cur_loc:
                self.location_name = f"{cur_loc['village']}, {cur_loc['county']}"
        """
        

        # metadata auf steroirds
        self.media_type = data_dict.get("mediaType", None)
        self.region = data_dict.get("region")
        self.bucket = data_dict.get("bucket")
        # user
        self.owner_id = data_dict.get("ownerID", None)
        self.username = data_dict.get("userName", None)
        self.profile_picture = data_dict["user"].get("profilePicture", {}).get("url", "")
        # times
        self.creationDate = data_dict["creationDate"]["_seconds"]
        self.takenAt = data_dict["takenAt"]["_seconds"]
        self.late_in_seconds = data_dict.get("lateInSeconds", None)
        # interactions
        self.realmojis = [UIRealmoji(realmoji_dict) for realmoji_dict in data_dict.get("realMojis", [])]
        self.comments = [UIComment(comment_dict) for comment_dict in data_dict.get("comment", [])]
    

    def render(self):
        return {
            "id": self.id,
            "url1": self.primary_photo,
            "url2": self.secondary_photo,
            "caption": self.caption,
            "user": {
                "id": self.owner_id,
                "username": self.username,
                "profile_picture": self.profile_picture
            },
            "time": {
                "late": second_stamp(self.late_in_seconds),
                "creationTime": sec_to_timestamp(self.creationDate),
                "takenAt": sec_to_timestamp(self.takenAt),
            },
            "metadata": {
                "retakes": self.retakes,
                "public": self.public,
                "location": {
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "location_name": self.location_name
                }
            },
            "realmojis": [realmoji.render() for realmoji in self.realmojis],
            "comments": [comment.render() for comment in self.comments],
        }


class UIRealmoji():
    def __init__(self, data_dict) -> None:
        self.data_dict = data_dict

        self.id = data_dict.get("id", None)
        self.owner_id = data_dict.get("uid", None)
        self.username = data_dict.get("userName", None)
        self.type = data_dict.get("type", None)
        self.emoji = data_dict.get("emoji", None)
        self.uri = data_dict.get("uri", None)
        if self.username in os.listdir(f"{DATA_DIR}/feeds/friends"):
            self.friend = True
        else:
            self.friend = False
    
    def render(self):
        return {
            "url": self.uri,
            "username": self.username,
            "friend": self.friend
        }


class UIComment():
    def __init__(self, data_dict) -> None:
        self.id = data_dict.get("id", None)
        self.owner_id = data_dict.get("uid", None)
        self.username = data_dict.get("userName", None)
        self.text = data_dict.get("text", None)
        self.time = data_dict["creationDate"]["_seconds"]
    
    def render(self):
        return {
            "username": self.username,
            "text": self.text,
            "time": sec_to_timestamp(self.time)
        }

class UIUser():
    def __init__(self, data_dict) -> None:
        print(data_dict)
        return
    
    def render(self):
        return {

        }


def second_stamp(seconds):
    return str(datetime.timedelta(seconds=seconds))

def latest_posts():
    # for faster reload during development
    #with open(f"{OWN_DIR}/static/json/test.json", "r") as f:
    #    return json.load(f)
    try:
        bf = BeFake.BeFake()
        #bf.load(TOKEN_PATH)
        bf.load("/root/.config/befake/token.txt")
        return_data = [UIPost(elem.data_dict).render() for elem in bf.get_friends_feed()]
    except ReadTimeout:
        return_data = []
    with open(f"{OWN_DIR}/static/json/test.json", "w+") as f:
        json.dump(return_data, f, indent=4)
    return return_data


def users():
    return os.listdir(f"{DATA_DIR}/feeds/friends")
    bf = BeFake.BeFake()
    try:
        bf.load()
    except:
        raise Exception("No token found, are you logged in?")
    usernames = os.listdir(f"{DATA_DIR}/feeds/friends")
    user_ids = []
    for user in usernames:
        example_post_path = os.path.join(
            f"{DATA_DIR}/feeds/friends/{user}",
            os.listdir(f"{DATA_DIR}/feeds/friends/{user}")[0], "info.json"
        )
        with open(example_post_path, "r") as f:
            example_post = json.load(f)
        user_ids.append(example_post["ownerID"])
    
    return [UIUser(user_data).render() for user_data in [
        bf.get_user_profile(user_id) for user_id in user_ids
    ]]
    

def posts(username):
    print("posts called...")
    if username not in os.listdir(f"{DATA_DIR}/feeds/friends"):
        return {"error": "User not found/your not friends with this user"}
    post_ids = [elem for elem in os.listdir(f"{DATA_DIR}/feeds/friends/{username}") if elem != ".DS_Store"]
    return_data = []
    for post_id in post_ids:
        with open(f"{DATA_DIR}/feeds/friends/{username}/{post_id}/info.json", "r") as f:
            cur_data = json.load(f)
        return_data.append(UIPost(cur_data).render())
    return_data = sorted(return_data, key=lambda x: x["time"]["creationTime"], reverse=True)
    return return_data
