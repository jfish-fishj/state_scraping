from data_constants import *
from court_order_scraping import *
from scraping_validation import *
from create_directories import *

if __name__ == '__main__':
    # scraping section
    # first scrape state state websites
    # try:
    #     os.mkdir(webscraping_output)
    # except OSError as error:
    #     print(error)
    scrape_urls(url_dict=state_url_dict, download_path=state_download_path)

    # move webscraping output to correct folder
    # move new files
    move_files(
        file_list=state_file_list, from_directory=webscraping_output, to_directory=new_files, exclude_directory=all_files
    )
    # move to all files
    move_files(
        file_list=state_file_list, from_directory=webscraping_output, to_directory=all_files
    )
    # scrape_urls(url_dict=state_url_dict, download_path=state_download_path)
    #
    # # move webscraping output to correct folder
    # # move new files
    # move_files(
    #     file_list=state_file_list, from_directory=webscraping_output, to_directory=new_files, exclude_directory=all_files
    # )
    # # move to all files
    # move_files(
    #     file_list=state_file_list, from_directory=webscraping_output, to_directory=all_files
    # )

    #
    # # validation section
    # # check emilys sheet for updates
    # try:
    #     os.mkdir(emily_base_directory)
    # except OSError as error:
    #     print(error)
    # try:
    #     os.mkdir(emily_download_path)
    # except OSError as error:
    #     print(error)
    # scrape_urls(url_dict=emily_dict, download_path=emily_download_path, downloaded_links='/Users/joefish/Desktop/state_webscraping/emily_links.txt')

    # create new directories to hold scraped data

    # validate emilys list against my output
    # compare_directories(directory1=emily_download_path, directory2=webscraping_output, state_regex=state_regex)
    # MAKING LOTS OF TEST CHANGES
    # testing things to push
    