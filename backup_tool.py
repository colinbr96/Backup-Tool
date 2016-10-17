from pathlib import Path
import shutil

#========================================================== PRESETS

LOCATIONS = ''
BACKUP = ''

#========================================================== HELPERS

def prompt(message: str) -> 'inputted':
    try:
        inputted = input(message)
        return inputted
    except(KeyboardInterrupt):
        print("\nGoodbye!")
        exit()


def file_prompt(message: str) -> Path:
    while(True):
        path = fix_user_paths(Path(prompt(message)))
        if not path.exists():
            print("    ERROR: The path \"{}\" does not exist.\n".format(path))
        elif not path.is_file():
            print("    ERROR: The path \"{}\" is not a file.\n".format(path))
        else:
            break
    return path


def destination_prompt(message: str) -> Path:
    while(True):
        path = fix_user_paths(Path(prompt(message)))
        if path.exists() and not path.is_dir():
            print("    ERROR: The path \"{}\" is not a folder.\n".format(path))
        else:
            break
    return path


def yes_or_no_prompt(message: str) -> bool:
    while(True):
        try:
            confirm = input("{} (Y/N): ".format(message))
            if confirm not in {'Y', 'N'}:
                print("ERROR: Please input \"Y\" or \"N\"")
            else:
                break
        except(KeyboardInterrupt):
            print("\nGoodbye!")
            exit()
    return confirm == 'Y'


def fix_user_paths(p: Path) -> Path:
    parts = p.parts
    if parts[0] == '~':
        p = p.home().joinpath('/'.join(parts[1:len(parts)]))
    return p

#========================================================== MAIN FUNCTIONS

def configure() -> (str, str):
    configuration = ['', '']
    if LOCATIONS and yes_or_no_prompt("Use preset location file \"{}\"?".format(LOCATIONS)):
        configuration[0] = LOCATIONS
    else:
        configuration[0] = file_prompt("Path to backup locations file: ")
    print("")
    if BACKUP and yes_or_no_prompt("Use preset backup folder \"{}\"?".format(BACKUP)):
        configuration[1] = Path(BACKUP)
    else:
        configuration[1] = destination_prompt("Path to backup destination: ")

    return configuration


def load_locations(locations_file: Path) -> [Path]:
    locations = []
    with locations_file.open() as file:
        for line in file:
            line = line.strip()
            path = fix_user_paths(Path(line))
            if(path.exists()):
                locations.append(path)
                print("    Added \"{}\"".format(path))
            else:
                print("    ERROR: The path \"{}\" does not exist.".format(path))
    print("")
    return locations


def backup(locations: [Path], destination: Path):
    if destination.exists():
        print("Destination \"{}\" already exists.".format(destination))
        if not yes_or_no_prompt("    Erase contents and continue?".format(destination)):
            print("\nAborted backup.")
            return
        shutil.rmtree(str(destination))
    
    for location in locations:
        print("    Backing up \"{}\"".format(location))
        shutil.copytree(str(location), str(destination.joinpath(location.name)))

    destination.touch()
    print("\nBackup complete!")

#========================================================== START

def main():
    print("BACKUP TOOL -- by Colin Brown\n")
    locations_file, destination_dir = configure()
    print("\nStarting backup process...")

    locations = load_locations(locations_file)
    if locations:
        backup(locations, destination_dir)
    else:
        print("\nAborted backup.")

if __name__ == '__main__':
    main()