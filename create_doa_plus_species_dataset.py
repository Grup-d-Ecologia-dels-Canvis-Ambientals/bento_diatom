import os
from pathlib import Path
import random
import shutil
import shlex
import zipfile

OUT_FOLDER = "data_combined"
SRC_DIR = "20250619_mv"
N_TEST = 10

alias = {
    "gomphonema" : "str66",
    "hannea": "str35",
    "nitzschia": "str05",
    "nocell": "no_cells"
}

def unzip_weights():
    print('Extracting weights...')
    with zipfile.ZipFile("doa_diatom_model.zip", 'r') as zip_ref:
        zip_ref.extractall()
    with zipfile.ZipFile("enhanced_diatom_model_cpu.zip", 'r') as zip_ref:
        zip_ref.extractall()

def unzip_pictures():
    # Unzip file
    print('Extracting pictures...')
    with zipfile.ZipFile("20250619_mv.zip", 'r') as zip_ref:
        zip_ref.extractall()        

def download_image_files():
    # Download file
    print('Downloading image files...')
    url = 'https://creaf-my.sharepoint.com/:u:/g/personal/a_escobar_creaf_uab_cat/EbiE91YiW6ZKo6FkF4nsBocBEHvKCyNjNDWIQA9fJ5krug?e=VdUvw5&download=1'
    os.system(f"wget --content-disposition -c --read-timeout=5 --tries=0 {shlex.quote(url)}")

def download_weight_files():
    print('Download network weights...')
    url = 'https://creaf-my.sharepoint.com/:u:/g/personal/a_escobar_creaf_uab_cat/EUkPMCLqDH5Ej1-DjqnAUFwBunz3pCfS6F0-N6sjr4agrA?e=KFgeRv&download=1'
    os.system(f"wget --content-disposition -c --read-timeout=5 --tries=0 {shlex.quote(url)}")
    # It's a private repo. Temporary solution, moved it to onedrive...
    url = 'https://creaf-my.sharepoint.com/:u:/g/personal/a_escobar_creaf_uab_cat/EQyXilqBxzRNgI9nYzuZcDMBo22AmyO2LzSNEmyNl89Vrg?e=vLUudc&download=1'
    os.system(f"wget --content-disposition -c --read-timeout=5 --tries=0 {shlex.quote(url)}")

def get_files_by_class(doa, species):
    search_doa = []
    if doa == "dead":
        search_doa = ['mort','mortes']
    else:
        search_doa = ['viu','vives']
    search_species = alias[species]
    base = Path(SRC_DIR)
    files = []    
    for dirpath in base.rglob('*'):        
        if dirpath.is_dir():
            if search_species == 'no_cells':
                contains_doa = True
                contains_species = search_species in dirpath.name.lower()
            else:
                contains_doa = any( sub in dirpath.name.lower() for sub in search_doa)            
                contains_species = search_species in dirpath.name.lower()
            if contains_doa and contains_species:
                files.extend([file for file in dirpath.glob('*.png')])                            
    return files

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

    if os.path.exists("enhanced_diatom_model_cpu.pth"):
        os.remove("enhanced_diatom_model_cpu.pth")

    if os.path.exists("enhanced_diatom_model_cpu.zip"):
        os.remove("enhanced_diatom_model_cpu.zip")

def init_classfile_dict():    
    class_files = {
        "train":{ "alive": {}, "dead": {}},
        "test":{ "alive": {}, "dead": {}}
    }
    return class_files

def organize_dirs():
    sets = ["train","test"]
    classes_species = ["gomphonema", "hannea", "nitzschia", "nocell"]
    classes_doa = ["dead", "alive"]
    
    class_files = init_classfile_dict()

    os.mkdir(OUT_FOLDER)
    for s in sets:
        os.mkdir( os.path.join(OUT_FOLDER, s) )
        for species in classes_species:
            for doa in classes_doa:
                os.mkdir( os.path.join(OUT_FOLDER, s, species + "_" + doa) )
                current_class_files = get_files_by_class(doa,species)
                class_files[s][doa][species] = current_class_files
    
    for s in sets:
        for species in classes_species:
            if species == 'nocell':
                files = class_files[s][doa][species]
                random.shuffle(files)
                for file in files[:N_TEST+1]:
                    shutil.copy(file, os.path.join(OUT_FOLDER, "test",species + "_dead") )
                for file in files[N_TEST+1:]:
                    shutil.copy(file, os.path.join(OUT_FOLDER, "train",species + "_dead") )
            else:
                for doa in classes_doa:
                    try:
                        files = class_files[s][doa][species]
                        random.shuffle(files)
                        for file in files[:N_TEST+1]:
                            shutil.copy(file, os.path.join(OUT_FOLDER, "test",species + "_" + doa) )
                        for file in files[N_TEST+1:]:
                            shutil.copy(file, os.path.join(OUT_FOLDER, "train",species + "_" + doa) )
                    except:
                        print(f"No files for {s} - {doa} - {species}")

def main():
    cleanup()
    download_weight_files()
    download_image_files()        
    unzip_pictures()
    unzip_weights()
    organize_dirs()    
    

if __name__ == "__main__":
    main()