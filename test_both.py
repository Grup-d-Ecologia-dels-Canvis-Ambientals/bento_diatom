
from pathlib import Path
from tqdm import tqdm
from test_helper import *

SPECIES = ["gomphonema","hannea","nitzschia","nocell"]
CATEGORIES = ["alive","dead"]
SETS = ["test", "train"]

def main():
    for category in CATEGORIES:
        for setname in SETS:
            for especie in SPECIES:
                expected_value = especie + "_" + category
                base = Path(get_base_dir(expected_value, setname))
                n_files = get_n_files_in_dir(base)
                hits = 0
                misses = 0
                total = 0
                if n_files > 0:
                    with tqdm(total=n_files) as pbar:
                        for file in base.rglob('*'):
                            classification = query_image(file, "http://localhost:3000/classify_both")
                            if classification == expected_value:
                                hits = hits + 1
                            else:
                                misses = misses + 1
                            total = total + 1
                            pbar.update(1)                        
                        print("---------------------------------------------------")
                        print("")
                        print(f"Pictures should be predicted as '{expected_value}'")
                        print(f"Pictures come from set '{setname}'")
                        print(f"Number of files {n_files}")
                        print('Results breakdown:')
                        print(f'Hits:{hits}/{total}')
                        print(f'Misses:{misses}/{total}')
                        accuracy = '{0:.2f}%'.format(((hits)/total)*100)
                        print(f'Accuracy:{accuracy}')
                        print("")
                        print("---------------------------------------------------")
                        pbar.clear()

                    

if __name__ == "__main__":
    main()