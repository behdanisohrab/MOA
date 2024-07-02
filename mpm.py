import git  # For interacting with git repositories
import os  # For file system operations
import shutil  # For high-level file operations
import json  # For JSON handling


def delete_cache_in_folder(folder_path):
    try:
        file_list = os.listdir(folder_path)  # List all files in the directory
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove file
            elif os.path.isdir(file_path):
                # Recursive call for directories
                delete_cache_in_folder(file_path)
    except FileNotFoundError as e:
        pass  # Ignore if the folder is not found
    except PermissionError as e:
        print(f"Permission denied")  # Print permission error


def check_file_and_extract_type(name):
    file_path = os.path.join(f"mpm_cache/{name}", "Information.json")

    if not os.path.exists(file_path):
        print("Error: The Information.json file was not found")
        return

    try:
        with open(file_path, "r") as file:
            data = json.load(file)  # Load JSON data
            file_type = data.get("type")

            if file_type:
                return file_type  # Return the type if it exists
            else:
                print("Error: The Information.json file is corrupted")
    except json.JSONDecodeError:
        print("Error: The Information.json file is not a valid JSON")


def extract_repository_name(url):
    url_parts = url.split("/")
    repository_name = url_parts[-1].split(".")[0]
    return repository_name  # Extract and return the repository name


def clone_repository(url):
    repo_path = "mpm_cache"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)  # Remove existing repo_path if it exists
    git.Repo.clone_from(url, repo_path)  # Clone the repository
    return extract_repository_name(url)


def move_files(source_dir, destination_dir):
    files = os.listdir(source_dir)  # List all files in the source directory
    for file in files:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)
        shutil.move(source_file, destination_file)  # Move each file


def installer(p_type, name):
    base_dir = f"mpm_cache/{name}"
    if p_type == "engine":
        move_files(base_dir, "/searx/engines/")  # Move engine files
    elif p_type == "answerer":
        move_files(base_dir, "/searx/answerers/")  # Move answerer files
    elif p_type == "plugin":
        move_files(base_dir, "/searx/plugins/")  # Move plugin files
    elif p_type == "theme":
        move_files(os.path.join(base_dir, "static"),
                   "/searx/static/")  # Move theme files
    else:
        print(f"Unknown package type: {p_type}")  # Handle unknown types


def plugin_remover(plugin_name):
    current_directory = os.getcwd()  # Get current working directory
    plugin_path = f"{current_directory}/searx/plugins/{plugin_name}.py"
    if os.path.exists(plugin_path):
        os.remove(plugin_path)  # Remove the plugin file
        print("The plugin has been successfully removed.")
    else:
        print("Error: Plugin not found")


def engine_remover(engine_name):
    current_directory = os.getcwd()  # Get current working directory
    engine_path = f"{current_directory}/searx/engines/{engine_name}.py"
    if os.path.exists(engine_path):
        os.remove(engine_path)  # Remove the engine file
        print("The engine has been successfully removed.")  # Corrected message
    else:
        print("Error: Engine not found")  # Corrected message


def lister():
    current_directory = os.path.dirname(os.path.abspath(
        __file__))  # Get directory of the current script
    categories = ["engines", "answerers", "plugins", "static/themes"]
    ret = ""

    for category in categories:
        path = os.path.join(current_directory, f"searx/{category}")
        if os.path.exists(path):
            items = [item for item in os.listdir(
                path) if item != "__init__.py" and not item.endswith("__pycache__")]
            # List items in the category
            ret += f"\n{category}:\n" + ", ".join(items) + "\n"
        else:
            # Handle empty categories
            ret += f"\n{category}:\nNo items found.\n"

    return ret  # Always return the ret variable


text = '''
===== mpm MOA package manager =====

To install the package:
>>> install <git url>

To remove the engine:
>>> remove -e <engine name> or r -e <engine name>

To remove the plugin:
>>> remove -p <plugin name> or r -p <plugin name>

For the list of packages:
>>> list
'''
print(text)
delete_cache_in_folder('mpm_cache')  # Clear the cache directory
while True:
    command = input(">>>")
    words = command.split()
    first_word = words[0] if words else ""

    if first_word in ("install", "i"):
        if len(words) >= 2:
            second_word = words[1]
            pack_name = clone_repository(second_word)  # Clone the repository
            pack_type = check_file_and_extract_type(
                pack_name)  # Check the package type
            if pack_type:
                installer(pack_type, pack_name)  # Install the package
            else:
                print("Package type not found.")
                continue
        else:
            print("Package name is missing.")
            continue

    elif first_word in ("remove", "r"):
        if len(words) >= 3:  # Ensure there are enough arguments
            argument = words[1]
            second_word = words[2]
            if argument == "-p":
                confirmation = input(
                    "Are you sure to delete this plugin? (yes/y or no/n)")
                if confirmation == "yes" or confirmation == "y":
                    plugin_remover(second_word)  # Remove the plugin
                else:
                    print("Delete canceled.")
            elif argument == "-e":
                confirmation = input(
                    "Are you sure to delete this engine? (yes/y or no/n)")
                if confirmation == "yes" or confirmation == "y":
                    engine_remover(second_word)  # Remove the engine
                else:
                    print("Delete canceled.")
            else:
                print("Argument not found.")
        else:
            print("Invalid command syntax.")
    elif first_word in ("list", "l"):
        print(lister())  # List all installed packages
    elif first_word == "exit":
        break
    elif first_word == "":
        pass
    else:
        print("No such command found")
