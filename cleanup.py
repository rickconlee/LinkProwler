import json 
import re
import os

# TODO: open multiple files in this app, but one at a time. 
with open('config.json') as input_file:
    var_name_here = json.load(input_file)

os.listdir()