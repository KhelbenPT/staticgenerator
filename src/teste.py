import os
import shutil
path = "../content"

def recursive(path):
    for item in os.listdir(path):
        if item == "index.md":
            print(path + "/" + item)
        else:
            newpath = path + "/" + item
            recursive(newpath)

recursive(path)