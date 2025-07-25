import fnmatch
import os
import requests

def get_n_files_in_dir(path):
    count = len(fnmatch.filter(os.listdir(path), '*.*'))
    return count

def get_base_dir(category, setname):
    path = os.path.join("data_combined",setname,category)
    return path

def query_image(path,url):
    with open(path, "rb") as f:
        res = requests.post(url, files={"image": f})
        return res.text
    return None