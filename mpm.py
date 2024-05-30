import git
import os
import shutil
import json
import logging
logging.basicConfig(level=logging.INFO)


def delete_cache_in_folder(folder_path):
    try:
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                delete_cache_in_folder(file_path)
    except FileNotFoundError as e:
        logging.warning(f"Folder not found: {folder_path}")
    except PermissionError as e:
        logging.error(f"Permission denied")


def check_file_and_extract_type(name):
    file_path = os.path.join(f"mpm_cache/{name}", "Information.json")

    if not os.path.exists(file_path):
        print("Error: The Information.json file was not found")
        return

    with open(file_path, "r") as file:
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                file_type = data.get("type")

                if file_type:
                    return file_type
                else:
                    logging.error(
                        "Error: The Information.json file is corrupted")
        except json.JSONDecodeError:
            logging.error(
                "Error: The Information.json file is not a valid JSON")


def extract_repository_name(url):
    url_parts = url.split("/")
    repository_name = url_parts[-1].split(".")[0]
    return repository_name


def clone_repository(url):
    repo_path = "mpm_cache"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    git.Repo.clone_from(url, repo_path)
    return extract_repository_name(url)


def move_files(source_dir, destination_dir):
    files = os.listdir(source_dir)
    for file in files:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)
        shutil.move(source_file, destination_file)


def installer(p_type, name):
    base_dir = f"mpm_cache/{name}"
    if p_type == "engine":
        move_files(base_dir, "/searx/engines/")
    elif p_type == "answerer":
        move_files(base_dir, "/searx/answerers/")
    elif p_type == "plugin":
        move_files(base_dir, "/searx/plugins/")
    elif p_type == "theme":
        move_files(os.path.join(base_dir, "static"), "/searx/static/")
    else:
        logging.error(f"Unknown package type: {p_type}")


def lister():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    categories = ["engines", "answerers", "plugins", "static/themes"]
    ret = ""

    for category in categories:
        path = os.path.join(current_directory, f"searx/{category}")
        if os.path.exists(path):
            items = [item for item in os.listdir(
                path) if item != "__init__.py" and not item.endswith("__pycache__")]
            ret += f"\n{category}:\n" + ", ".join(items) + "\n"
        else:
            ret += f"\n{category}:\nNo items found.\n"
    return ret

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


text = '''
mpm MOA package manager

To install the package:
install <git url>

To remove the package:
remove <package name>

For the list of packages:
list
'''
print(text)
delete_cache_in_folder('mpm_cache')
while True:
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
                logging.warning("Package type not found.")
                continue
        else:
            print("Package name is missing.")
            continue

    elif first_word in ("remove", "r"):
        print("remove functionality not implemented")
    elif first_word in ("list", "l"):
        print(lister())
    elif first_word == "exit":
        break
    else:
        print("No such command found")
