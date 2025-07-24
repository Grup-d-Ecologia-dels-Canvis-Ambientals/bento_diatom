import os
import shlex
import zipfile
import shutil
import random
from pathlib import Path
import sys

OUT_FOLDER = "data"
SRC_DIR = "20250619_mv"
N_TEST = 10

def organize_dirs():
    # Creating dirs
    sets = ["train","test"]
    classes = ["dead", "alive"]

    os.mkdir(OUT_FOLDER)
    for s in sets:
        os.mkdir( os.path.join(OUT_FOLDER, s) )
        for c in classes:
            os.mkdir( os.path.join(OUT_FOLDER, s, c) )

    base = Path(SRC_DIR)
    dead = []
    for dirpath in base.rglob('*'):
        if dirpath.is_dir() and ( any( sub in dirpath.name.lower() for sub in ['mort','mortes']) ):        
            dead.extend([file for file in dirpath.glob('*.png')])


    alive = []
    for dirpath in base.rglob('*'):
        if dirpath.is_dir() and ( any( sub in dirpath.name.lower() for sub in ['viu','vives']) ):
            alive.extend([file for file in dirpath.glob('*.png')])

    random.shuffle(dead)
    random.shuffle(alive)

    for file in alive[:N_TEST+1]:
        shutil.copy(file, os.path.join(OUT_FOLDER, "test","alive") )
    for file in dead[:N_TEST+1]:
        shutil.copy(file, os.path.join(OUT_FOLDER, "test","dead") )

    for file in alive[N_TEST+1:]:
        shutil.copy(file, os.path.join(OUT_FOLDER, "train","alive") )
    for file in dead[N_TEST+1:]:
        shutil.copy(file, os.path.join(OUT_FOLDER, "train","dead") )

    print("Moved images, final folder breakdown")
    for s in ["test","train"]:
        for label in ["dead","alive"]:
            if s == 'test': 
                if label == 'dead':
                    n = len(dead[:N_TEST])
                else:
                    n = len(alive[:N_TEST])
            elif s == 'train':
                if label == 'dead':
                    n = len(dead[N_TEST:])
                else:
                    n = len(alive[N_TEST:])
            print(f"Set '{s}', label '{label}', count {n} images")

def unzip_pictures():
    # Unzip file
    print('Extracting pictures...')
    with zipfile.ZipFile("20250619_mv.zip", 'r') as zip_ref:
        zip_ref.extractall()        

def unzip_weights():
    print('Extracting weights...')
    with zipfile.ZipFile("doa_diatom_model.zip", 'r') as zip_ref:
        zip_ref.extractall()

def download_weight_files():
    print('Download network weights...')
    url = 'https://creaf-my.sharepoint.com/:u:/g/personal/a_escobar_creaf_uab_cat/EUkPMCLqDH5Ej1-DjqnAUFwBunz3pCfS6F0-N6sjr4agrA?e=KFgeRv&download=1'
    os.system(f"wget --content-disposition -c --read-timeout=5 --tries=0 {shlex.quote(url)}")

def download_image_files():
    # Download file
    print('Downloading image files...')
    url = 'https://creaf-my.sharepoint.com/:u:/g/personal/a_escobar_creaf_uab_cat/EbiE91YiW6ZKo6FkF4nsBocBEHvKCyNjNDWIQA9fJ5krug?e=VdUvw5&download=1'
    os.system(f"wget --content-disposition -c --read-timeout=5 --tries=0 {shlex.quote(url)}")    

def cleanup():
    print("Deleting files and uncompressed folder")
    try:
        shutil.rmtree(OUT_FOLDER)
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(SRC_DIR)
    except FileNotFoundError:
        pass

    if os.path.exists("20250619_mv.zip"):
        os.remove("20250619_mv.zip")
    
    if os.path.exists("doa_diatom_model.pth"):
        os.remove("doa_diatom_model.pth")

    if os.path.exists("doa_diatom_model.zip"):
        os.remove("doa_diatom_model.zip")

def main():
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == 'w':
        download_weight_files()
        unzip_weights()
    else:
        cleanup()
        download_weight_files()
        download_image_files()        
        unzip_pictures()
        unzip_weights()
        organize_dirs()
            

if __name__ == "__main__":
    main()