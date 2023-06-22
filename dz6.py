import sys
import os
from pathlib import Path
import uuid
import shutil


CATEGORIES = {'DOCUMENTS':['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'],
              'IMAGES':['.JPEG', '.PNG', '.JPG', '.SVG'],
              'AUDIO':['.MP3', '.OGG', '.WAV', '.AMR'],
              'VIDEO':['.AVI', '.MP4', '.MOV', '.MKV'],
              'ARCHIVES':['.ZIP', '.GZ', '.TAR']}


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

BAD_SYMBOL = ("%","*"," ","-") 
TRANS = {}
    
def normalize(name):
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    for i in BAD_SYMBOL:
        TRANS[ord(i)] = "_"
    normalize_name = name.translate(TRANS) 
    return normalize_name 
    

def move_file(path:Path, root_dir:Path, categorie:str):
    target_dir = root_dir.joinpath(categorie)

    if not target_dir.exists():
        print(f"Make {target_dir}")
        target_dir.mkdir()

    new_name = target_dir.joinpath(f'{normalize(path.stem)}{path.suffix}')          
    
    if new_name.exists():
        new_name = new_name.with_name(f'{new_name.stem}-{uuid.uuid4()}{path.suffix}')
    path.rename(new_name)


def get_categories(path:Path):
    ext = path.suffix.upper()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Others"


def sort_folder(path:Path):
    for item in path.glob("**/*"):  
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def delete_empty_folder(path:Path):
    flag =True
    while flag == True:
        flag = False
        for item in path.glob("**\*"):  
            if item.is_dir():
                try:    
                    item.rmdir()
                    flag = True
                except:
                    ...

               
def unpack_archive_(path):
    target_dir = path.joinpath("ARCHIVES")
    if not target_dir.exists():
        print("No archive folder")
    else:
        for item in target_dir.glob("**\*"):  
            if item.is_file():
                if item.suffix.upper() in CATEGORIES['ARCHIVES']:
                    path_to_unpack_ = target_dir.joinpath(item.stem)
                    shutil.unpack_archive(item,path_to_unpack_)
                    os.remove(item)


def main():
    try:
        path = Path(sys.argv[1])
        print(f' try path {path}')
    except IndexError:
        print("No path to folder")
        return "No path to folder"
    if not path.exists():
        print(f"Folder with path {path} does not exist")
        return f"Folder with path {path} does not exist"
    
    sort_folder(path)
    delete_empty_folder(path)
    unpack_archive_(path)

main()