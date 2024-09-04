import os
import json

#############################################################

def load(animation_file_dir):
    with open(animation_file_dir, "r") as anifile:
        return json.load(anifile)
    
def save(animation_file_dir, content):
    with open(animation_file_dir, "w") as anifile:
        os.truncate(animation_file_dir, 0)
        anifile.seek(0)
        json.dump(content, anifile)

def reset(animation_file_dir):
    os.truncate(animation_file_dir, 0)

#############################################################