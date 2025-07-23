import requests
from pathlib import Path
import os
import fnmatch
from tqdm import tqdm

CATEGORIES = ["alive","dead"]
SETS = ["test", "train"]

def get_base_dir(category, setname):
    path = os.path.join("data",setname,category)
    return path

def get_n_files_in_dir(path):
    count = len(fnmatch.filter(os.listdir(path), '*.*'))
    return count

def query_image(path):
    with open(path, "rb") as f:
        res = requests.post("http://localhost:3000/classify", files={"image": f})
        return res.text
    return None

def main():    
    for category in CATEGORIES:
        for setname in SETS:
            base = Path(get_base_dir(category,setname))
            n_files = get_n_files_in_dir(base)
            hits = 0
            misses = 0
            total = 0
            with tqdm(total=n_files) as pbar:
                for file in base.rglob('*'):
                    itis = query_image(file)
                    if itis == category:
                        hits = hits + 1
                    else:
                        misses = misses + 1
                    total = total + 1
                    pbar.update(1)                
                pbar.clear()                
                print("---------------------------------------------------")
                print("")
                print(f"Pictures should be predicted as '{category}'")
                print(f"Pictures come from set '{setname}'")
                print(f"Number of files {n_files}")
                print('Results breakdown:')
                print(f'Hits:{hits}/{total}')
                print(f'Misses:{misses}/{total}')
                accuracy = '{0:.2f}%'.format(((hits)/total)*100) 
                print(f'Accuracy:{accuracy}')
                print("")
                print("---------------------------------------------------")    
                

if __name__ == "__main__":
    main()
