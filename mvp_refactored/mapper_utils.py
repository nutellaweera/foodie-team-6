from __future__ import print_function
from ipyfilechooser import FileChooser
from google.cloud import vision
from google.oauth2 import service_account
import pandas as pd
import pyrebase
import csv
import json
import re
import io

# key path (to replace)
VISION_API_KEY_PATH = '/Users/sunellauni/Documents/UWE/IGP/foodie-team-6/keys/cal_key.json'
FIREBASE_API_KEY_PATH = '/Users/sunellauni/Documents/UWE/IGP/foodie-team-6/keys/firebase_key.json'


# Displays a file selected with a specified filter
# ref - https://github.com/crahan/ipyfilechooser
def choose_file(filters):
    f = FileChooser()
    f.filter_pattern = filters
    display(f)
    print(f.selected)
    return f.selected

# Return path to google vision api key
def get_vision_api_key():
    return VISION_API_KEY_PATH

# Return path to firebase key
def get_firebase_key():
    return FIREBASE_API_KEY_PATH


# Initializes the Google Vision API with a selected key file, 
# invokes the API, passing the selected image file,
# and returns the annotated response
# ref - https://codelabs.developers.google.com/codelabs/cloud-vision-api-python#1
def invoke_vision_api(img_path, key_path):
    print(key_path)
    print(img_path)
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()
        
    image = vision.Image(content=content)
    return client.label_detection(image=image)


# Formats the response of the Google Vision API and returns an array of string labels 
def format_api_response(response_string):
    labels = []
    for label in response_string.label_annotations:
        #print(label.description, '(%.2f%%)' % (label.score*100)) # uncomment for debugging labels if required
        labels.append(label.description.lower())
    return labels


# Establishes a connection to a firebase db and returns calorie counts
def connect_to_firebase(firebase_key):
    with open(firebase_key) as json_file:
        firebase_config = json.load(json_file)
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()
    return db.child('CalorieCounts').get()


# Finds and returns a calorie match if the label exists in the database
def find_cal_match(cal_counts, labels):
    calories, match = None, None
    for lbl in labels:
        for item in cal_counts.each():
            if lbl == item.key():
                match = lbl
                calories = item.val()
    return match, calories


# Adds calorie matching data (in csv form) to a firebase datastore
def add_data_to_firebase(db):
    with open('../data/calorie_counts.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        calorie_data = {}
        for row in reader:
            row['Food'] = re.sub("['.','’']",'',row['Food'])
            row['Food'] = re.sub("-",' ',row['Food'])
            row['Food'] = re.sub("é",'e',row['Food'])
            
            calorie_data[row['Food'].lower()] = row['Calories']

    db.child('CalorieCounts').set(calorie_data)

