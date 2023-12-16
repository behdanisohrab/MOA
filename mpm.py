import git
import os
import shutil
import json
def delete_cache_in_folder(folder_path):
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            delete_cache_in_folder(file_path)
def delete_folder_cache():
    cache_folder = 'mpm_cache'
    delete_cache_in_folder(cache_folder)


def check_file_and_extract_type(name):
    file_path = os.path.join(f"mpm_cache/{name}", "Information.json")

    if not os.path.exists(file_path):
        print("Error: The Information.json file was not found")
        return

    with open(file_path, "r") as file:
        data = json.load(file)
        file_type = data.get("type")

        if file_type:
            return file_type
        else:
            print("Error: The Information.json file is corrupted")



def extract_repository_name(url):
    url_parts = url.split("/")
    repository_name = url_parts[-1]
    repository_name = repository_name.split(".")[0]
    return repository_name



def clone_repository(url):
    git.Repo.clone_from(url, "mpm_cache")



def instaler(p_type, name):

    if p_type == "engine":
        destination_file = os.path.join("/searx/engines/", file)
        files = os.listdir(f"/mpm_cache/{name}")

        for file in files:
            source_file = os.path.join(f"/mpm_cache/{name}", file)
            shutil.move(source_file, destination_file)

    elif p_type == "answerer":
        destination_file = os.path.join("/searx/answerers/", file)
        files = os.listdir("/mpm_cache")

        for file in files:
            source_file = os.path.join("/mpm_cache", file)
            shutil.move(source_file, destination_file)

    elif p_type == "plugin":
        destination_file = os.path.join("/searx/plugins/", file)
        files = os.listdir("/mpm_cache")

        for file in files:
            source_file = os.path.join("/mpm_cache", file)
            shutil.move(source_file, destination_file)
    elif p_type == "theme":
        destination_file = os.path.join("/searx/static/", file)
        files = os.listdir("/mpm_cache/static")

        destination_file_templates = os.path.join("/searx/static/", file)
        files_templates = os.listdir("/mpm_cache/static")

        for file in files:
            source_file = os.path.join("/mpm_cache", file)
            shutil.move(source_file, destination_file)
        for file in files_templates:
            source_file = os.path.join("/mpm_cache", file)
            shutil.move(source_file, destination_file_templates)

def lister():
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # print engines
    contents = os.listdir(current_directory + "/searx/engines/")
    filtered_items = [item for item in contents if item != "__init__.py" and not item.endswith("pycache")]
    engines = ""
    for item in contents:
        if item == "__init__.py" or item.endswith("__pycache__"):
            continue
        else:
            engines += item + "  "

    # print answerers
    contents = os.listdir(current_directory + "/searx/answerers/")
    answerers = ""
    for item in contents:
        if item == "__init__.py" or item.endswith("__pycache__"):
            continue
        answerers += item + ", "

    # print plugins
    contents = os.listdir(current_directory + "/searx/plugins/")
    plugins = ""
    for item in contents:
        if item == "__init__.py" or item.endswith("__pycache__"):
            continue
        plugins += item + ", "

        # print themes
    contents = os.listdir(current_directory + "/searx/static/themes/")
    themes = ""
    for item in contents:
        themes += item + ", "

    ret = f'''
engines:
{engines}

answerers:
{answerers}

plugins:
{plugins}

themes:
{themes}

    '''
    return ret
text = ''' mpm MOA package manager
To install the package:
install <git url>

To remove the package:
remove <package name>

For the list of packages:
list
'''
print(text)

while True:
    delete_folder_cache()
    command = input(">>>")
    words = command.split()
    first_word = words[0] if words else ""

    if first_word in ("install", "i"):
        if len(words) >= 2:
            second_word = words[1]
            pack_name = clone_repository(second_word)
            pack_type = check_file_and_extract_type(pack_name)
            if pack_type:
                installer(pack_type, pack_name)
            else:
                continue
        else:
            print("Package name is missing.")
            continue

    elif first_word in ("remove", "r"):
        print("test")
    elif first_word in ("list", "l"):
        print(lister())
    elif first_word == "exit":
        break
    else:
        print("No such command found")
