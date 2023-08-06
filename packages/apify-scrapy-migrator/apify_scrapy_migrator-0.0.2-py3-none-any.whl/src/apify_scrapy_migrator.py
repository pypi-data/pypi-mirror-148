import os
import sys
import argparse
import subprocess

from .create_files import create_dockerfile, create_main_py, create_apify_json, create_input_schema


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--migrate", help="Wraps scrapy project with files to be pushed to Apify platform",
                        type=str, dest='migrate_folder')
    parser.add_argument("-i", "--update-input", help="Creates or updates 'INPUT_SCHEMA.json'. Default value is '.'",
                        type=str, dest='input_folder', const='.', nargs='?')
    parser.add_argument("-r", "--update-reqs", help="Creates or updates 'requirements.txt'. Default value is '.'",
                        type=str, dest='reqs_folder', const='.', nargs='?')
    args = parser.parse_args()

    if args.migrate_folder:
        wrap_scrapy(args.migrate_folder)
    else:
        if args.input_folder:
            _get_and_update_spiders_and_input(args.input_folder)
        if args.reqs_folder:
            update_reqs(args.reqs_folder)


def update_reqs(dst):
    """
    Creates or updates requirements.txt of a project. Runs pipreqs. If requirements exists, appends with pipreqs result
    :param dst: destination of scrapy project
    :return: boolean of successfulness
    """
    if not os.path.exists(os.path.join(dst, 'scrapy.cfg')):
        print('Select root directory with "scrapy.cfg" file.')
        return False

    import pipreqs
    if os.path.exists(os.path.join(dst, 'requirements.txt')):
        os.rename(os.path.join(dst, 'requirements.txt'), os.path.join(dst, 'requirements_tmp'))
        print(dst)
        subprocess.run(["pipreqs", dst])
        with open(os.path.join(dst, 'requirements.txt'), "a") as reqs:
            with open(os.path.join(dst, 'requirements_tmp'), "r") as tmp:
                for line in tmp:
                    reqs.write(line)
        os.remove(os.path.join(dst, 'requirements_tmp'))
    else:
        subprocess.run(["pipreqs", dst])

    return True


def _get_and_update_spiders_and_input(dst):
    """
    Creates or updates INPUT_SCHEMA.json of a project
    :param dst: destination of scrapy project
    :return: tuple of (name, path) of spider and tuple of (name, default_value) of inputs
    """
    # TODO: Should I expect other spiders dir location?
    spiders_dir = get_spiders_folder(dst)

    if not spiders_dir:
        print("Cannot find subdirectory 'spiders'.")
        return None

    # TODO: What to do if multiple spiders? Maybe create multiple directory with as individual actors
    spiders = get_spiders(spiders_dir)

    if len(spiders) == 0:
        print('No spiders found in "spiders" subdirectory.')
        return None

    inputs = get_inputs(spiders[0][1])
    create_input_schema(dst, spiders[0][0], inputs)

    return spiders, inputs


def wrap_scrapy(dst: str):
    """
    Wrap scrapy project with files to be executable on Apify platform
    :param dst: directory which will be wrap with files
    """

    files_in_dir = os.listdir(dst)
    files = ['requirements.txt', 'main.py', 'Dockerfile', 'apify.json', 'INPUT_SCHEMA.json']

    # check if in scrapy root folder
    if 'scrapy.cfg' not in files_in_dir:
        print('Select root directory with "scrapy.cfg" file.')
        return False

    # check if files that will be created exist
    for file in files:
        if file in files_in_dir:
            print("If these files exists, they will be overwritten: 'requirements.txt', 'main.py', 'Dockerfile', "
                  "'apify.json', 'INPUT_SCHEMA.json'. Do you wish to continue? [Y/N]")
            answer = sys.stdin.read(1)[0]
            if not (answer == 'y' or answer == 'Y'):
                return False
            else:
                break

    spiders, inputs = _get_and_update_spiders_and_input(dst)

    is_correct = True
    if spiders is not None:
        is_correct = create_input_schema(dst, spiders[0][0], inputs)

    if not is_correct:
        return False

    return create_dockerfile(dst) and create_apify_json(dst) and create_main_py(dst, spiders[0][0], spiders[0][1]) \
           and update_reqs(dst)


def get_spiders_folder(dst):
    """
    Finds spiders folder in scrapy root directory
    :param dst:  scrapy root directory
    :return:  returns path to spiders folder or None
    """
    spiders_dir = None
    for directory in os.listdir(dst):
        if os.path.isdir(os.path.join(dst, directory, 'spiders')):
            spiders_dir = os.path.join(dst, directory, 'spiders')
            break

    return spiders_dir


def get_spiders(spiders_dir):
    """
    Find classes with scrapy.Spider argument in spiders directory
    :param spiders_dir: spiders directory
    :return: array of tuples of (name, path) of spider classes
    """
    spiders = []

    for file in os.listdir(spiders_dir):
        if file.endswith(".py"):
            file_to_read = open(os.path.join(spiders_dir, file), 'r')
            for line in file_to_read.readlines():
                stripped = line.strip()
                if stripped.startswith('class') and stripped.endswith('(scrapy.Spider):'):
                    class_name = stripped.split(' ')[1].split('(')[0]
                    spiders.append((class_name, os.path.join(spiders_dir, file)))
                    break  # TODO: is break OK? I think its better than rewriting it with while loop

    return spiders


def get_inputs(filename):
    """
    Finds input in a file
    :param filename: filename
    :return: array of tuple (name, default_value) of inputs
    """
    file = open(filename, 'r')
    lines = file.readlines()
    GETATTR_SELF = 'getattr(self'
    index = 0

    # find class with spider
    while index < len(lines) and not lines[index].lstrip().startswith('class') and 'scrapy.Spider' not in lines[index]:
        index += 1
    if index >= len(lines):
        return []

    inputs = []

    # find getattr in the current class
    index += 1
    while index < len(lines) and not lines[index].lstrip().startswith('class'):
        if GETATTR_SELF in lines[index]:
            value = get_input(lines[index])
            if value:
                inputs.append(value)
        index += 1

    return inputs


def get_input(line):
    """
    Tries to retrieve name and the default value from the getattr() call
    :param line: line with getattr() method call
    :return: tuple of name,default value. None if value could not retrieve
    """
    GETATTR_SELF = 'getattr(self'
    start_chars = ['\'', '"', '-']
    try:
        index = line.index(GETATTR_SELF) + len(GETATTR_SELF)
    except ValueError:
        # getattr() was not found
        return None

    # find second argument of getattr
    while index < len(line) and line[index] != ',':
        index += 1

    # could not find recognizable
    if index >= len(line):
        return None

    name, index = get_attr_name(line, index + 1)

    if index is None:
        return None

    default_value = get_default_value(line, index + 1)

    # TODO: int
    # TODO: default value for other types than str: [str]? [int]?
    index += 1
    # try to find default value
    while index < len(line) and line[index] != '"' and line[index] != "'":
        index += 1

    if index >= len(line):
        return name, None

    # default value found
    index += 1
    start_index = index
    while index < len(line) and line[index] != '"' and line[index] != "'":
        index += 1

    if index >= len(line):
        return None

    return name, line[start_index:index]


def get_attr_name(line, index):
    """
    Gets attribute name from line until comma. Name can be variable name or string
    :param line: string of a text
    :param index: index of a first letter of a text
    :return: tuple of name and index of the fist non-name letter. I name/index is None, then could not find name
    """
    if index >= len(line):
        return None, None

    # skip overhead
    while index < len(line) and line[index].isspace():
        index += 1

    if index == len(line):
        return None, None

    name = ''
    # read until find string argument
    while index < len(line) and line[index] != '\'' and line[index] != '"' and line[index] != ',':
        name += line[index]
        index += 1

    if index == len(line):
        return None, None

    name = name.strip()
    if (name[0] == '\'' or name[0] == '"') and (name[len(name) - 1] == '\'' or name[len(name) - 1] == '"'):
        name = name[1:-1]

    return name, index


def get_default_value(line, index):
    if index >= len(line):
        return None

    # try to find string or int
    while index < len(line) \
            and not (line[index] == '\'' or line[index] == '"' or line[index] == '-' or line[index].isdigit()):
        index += 1

    if line[index] == '\'' or line[index] == '"':
        stop_char = line[index]

        while index < len(line) and line[index] != stop_char:
            pass


if __name__ == '__main__':
    _get_and_update_spiders_and_input(r'./../../scrapy_project/')
