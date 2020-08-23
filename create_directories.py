import os
import shutil
import re
from data_constants import *

# function to make directories of states to hold webscraping output
# makes all the directories and returns a dictionary w/ states and their paths
def make_directories(base_directory, state_list):
    state_dict = {}
    try:
        os.makedirs(base_directory )
    except OSError as error:
        print(error)

    for state in state_list:
        path = os.path.join(base_directory, state)
        state_dict[state] = path
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
    return state_dict

# function for moving files w/ state prefixes
def move_state_files(from_directory,file_list, state_dict, state_dict_new):
    for state in state_dict:
        state_files = [file for file in file_list if re.search('^{}_'.format(state), file) and file not in os.listdir(state_dict[state])]
        for file in state_files:
            print('moving {} to {}'.format(file, state_dict_new[state]))
            shutil.copy(from_directory + file, state_dict_new[state])

# function for moving files without state prefixes that are unclear
def move_unclear_files(from_directory,state_regex, state_dict, state_dict_new, file_list):
    for file in file_list:
        if not re.search(state_regex, file) and file not in os.listdir(state_dict['Unclear']):
            print('moving {} to {}'.format(file, state_dict_new['Unclear']))
            shutil.copy(from_directory + file, state_dict_new['Unclear'])

# function for moving files w/ out state prefixes
def move_files(from_directory,file_list, to_directory, exclude_directory=False):
    try:
        os.makedirs(to_directory )
    except OSError as error:
        print(error)
    if exclude_directory is not False:
        state_files = [file for file in file_list if file not in os.listdir(to_directory) and
                       re.search(r'\([0-9]+\)\.[a-z]+$', file) is None and
                       file not in os.listdir(exclude_directory)]
    else:
        state_files = [file for file in file_list if file not in os.listdir(to_directory) and
                        re.search(r'\([0-9]+\)\.[a-z]+$', file) is None]
    for file in state_files:
        print('moving {} to {}'.format(file, to_directory))
        shutil.copy(from_directory + file, to_directory)


if __name__ == '__main__':

    # make new directories to hold webscraping output
    state_dict = make_directories(base_directory= webscraping_output + 'all_files/', state_list=state_list)
    state_dict_new = make_directories(base_directory=webscraping_output + 'new_files/', state_list=state_list)

    # move webscraping output to correct folder
    # move new files
    move_state_files(state_file_list, state_dict, state_dict_new)
    move_unclear_files(state_regex, state_file_list, state_dict, state_dict_new)
    # move to all files
    move_state_files(state_file_list, state_dict, state_dict)
    move_unclear_files(state_regex, state_file_list, state_dict, state_dict)

    # repeat for emilys data
    emily_dict = make_directories(emily_base_directory, state_list=emily_state_list)



