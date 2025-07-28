from pathlib import Path
from tqdm import tqdm
from test_helper import *

CATEGORIES = ["alive","dead"]
SETS = ["test", "train"]

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
                    itis = query_image(file,"http://localhost:3000/classify_doa")
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
