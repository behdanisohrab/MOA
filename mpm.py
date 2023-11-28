import git
import os
import shutil
import json
def delete_folder_cache():
    file_list = os.listdir("mpm_cache")
    for file_name in file_list:
        file_path = os.path.join("mpm_cache", file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            delete_folder_cache(file_path)


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

    elif p_type == "answerer":
        destination_file = os.path.join("/searx/answerers/", file)
        files = os.listdir("/mpm_cache")

        for file in files:
            source_file = os.path.join("/mpm_cache", file)
            shutil.move(source_file, destination_file)

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
    comand = import(">>>")
    words = comand.split()
    second_word = words[1]
    first_word = words[0]
    if first_word == "install" or "i":
        pack_name = clone_repository(second_word)
        pack_type = check_file_and_extract_type(pack_name)
        if pack_type:
            instaler(pack_type, pack_name)
        else:
            continue


    elif first_word == "remove" or "r":

    elif first_word == "list" or "l":

    elif first_word == "exit":

    else:
