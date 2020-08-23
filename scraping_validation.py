import os
from selenium import webdriver
from create_directories import make_directories, move_unclear_files, move_state_files
from court_order_scraping import scrape_urls
from data_constants import *
import re
import csv
import sys
import glob
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import *
import io
from pathlib import Path
import warnings
import time
import datetime
import pandas as pd
ts = time.time()
log_path = st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def compare_directories(directory1, directory2, state_regex=False):
    if state_regex is not False:
        files_not_found = [file for file in os.listdir(directory1) if file not in os.listdir(directory2)]
    else:
        files_not_found = [file for file in os.listdir(directory1) if re.sub(state_regex,'', file) not in os.listdir(directory2)]
    print('number files in directory1 not in direcotry 2 is {}'.format(len(files_not_found)))
    print(len(os.listdir(directory2)))
    print(len(os.listdir(directory1)))
    if len(files_not_found) > 0:
        print('\n'.join(files_not_found))

def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    return data

def write_to_log(text,tabs = 0,clearLog=False, new_log=log_path,doPrint=True, warn=False):
    text = str(text)
    if clearLog:
        f = open( Path('/Users/joefish/Desktop/state_webscraping/webscraping_validation/logs/log_{}.txt'.format(new_log)), "w+")
    else:
        f = open( Path('/Users/joefish/Desktop/state_webscraping/webscraping_validation/logs/log_{}.txt'.format(new_log)), "a+")
    text = text.rjust(len(text) + tabs*3)
    if tabs == 0:
        f.write("\n")
    f.write(text+ "\n")
    if doPrint:
        print(text)
    if warn:
        warnings.warn(text)



if __name__ == '__main__':
    write_to_log('New webscraping run on {}'.format(st), clearLog=True)
    # get all files on emilys spreadsheet
    # try:
    #     os.mkdir(emily_download_path)
    # except OSError as error:
    #     print(error)
    # scrape_urls(emily_dict, download_path=emily_download_path)
    # make_directories(emily_base_directory, state_list=emily_state_list)
    # maxInt = sys.maxsize
    #
    # while True:
    #     # decrease the maxInt value by factor 10
    #     # as long as the OverflowError occurs.
    #
    #     try:
    #         csv.field_size_limit(maxInt)
    #         break
    #     except OverflowError:
    #         maxInt = int(maxInt / 10)
    # el = []
    # with open('/Users/joefish/Desktop/state_webscraping/checked_files_scraper.txt') as checked_files:
    #     file_list = [re.sub('%20', ' ', link.rstrip()) for link in checked_files]
    # checked_files = open('/Users/joefish/Desktop/state_webscraping/checked_files_scraper.txt', mode='a+')
    # with open('/Users/joefish/Desktop/state_webscraping/partial_scraper.csv', mode='a+', newline='') as pdf_text:
    #     write = csv.writer(pdf_text)
    #     for file in os.listdir('/Users/joefish/Desktop/state_webscraping/all_files/'):
    #         if file not in file_list:
    #             container = []
    #             try:
    #                 text = []
    #                 parsed_text = pdfparser('/Users/joefish/Desktop/state_webscraping/all_files/' + file)
    #                 # remove quote characters
    #                 parsed_text = re.sub('"', '', parsed_text)
    #                 parsed_text = re.sub("'", '', parsed_text)
    #                 text.append(parsed_text)
    #                 el.append(text)
    #                 container.append(text)
    #                 write.writerows(container)
    #                 write_to_log('Coverted {} to txt'.format(file))
    #             except (ValueError, PDFTextExtractionNotAllowed, PDFSyntaxError,PSEOF) as e:
    #                 write_to_log('Unable to process {}'.format(file), warn=True)
    #             checked_files.write('\n{}'.format(re.sub('%20', ' ', file)))
    #         else:
    #             write_to_log('{} already checked'.format(file))

    # writing the data into the file
    # file = open('/Users/joefish/Desktop/state_webscraping/full_scraper.csv', 'w+', newline='')
    # with file:
    #     write = csv.writer(file)
    #     write.writerows(el)
    # open csv of parsed pdfs and convert to list
    parsed_pdf_text = open('/Users/joefish/Desktop/state_webscraping/partial_scraper_text.txt', 'r').read()
    checked_states = []
    with open('/Users/joefish/Desktop/state_webscraping/checked_states_law.txt', 'r') as inputfile:
        for row in csv.reader(inputfile):
            checked_states.append(row[0])
    # print(len(results))
    # directory where all downloaded pdfs are
    base_directory = '/Users/joefish/Downloads/drive-download-20200702T194617Z-001/'
    # create empty dataframe to hold analysis
    df = pd.DataFrame(columns=['state', 'file', 'was_scraped'])
    # create empty list to hold rows of dataframe
    rows = []
    for state in os.listdir(base_directory):
        for file in glob.iglob(base_directory + state + '/**/*.pdf',  recursive=True):
            if state not in checked_states:
                try:
                    text = pdfparser(file)
                    text = re.sub('"', '', text)
                    text = re.sub("'", '', text)
                except (ValueError, PDFTextExtractionNotAllowed, PDFSyntaxError,PSEOF, TypeError) as e:
                    write_to_log('Unable to process {}'.format(file), warn=True)
                    text = 'Unable to process {}'.format(file)
                if text in parsed_pdf_text:
                    was_scraped = 1
                else:
                    was_scraped = 0
                results_list = [state, file, was_scraped]
                print(results_list)
                rows.append(results_list)
        checked_states.append(state)
        state_df = pd.DataFrame(rows, columns=['state', 'file', 'was_scraped'])
        df = pd.concat([df, state_df])
        df.to_csv('/Users/joefish/Desktop/state_webscraping/scraper_analysis.csv')
        with open('/Users/joefish/Desktop/state_webscraping/checked_states_law.txt', 'a+') as inputfile:
            for state in checked_states:
                inputfile.write('\n{}'.format(state))
