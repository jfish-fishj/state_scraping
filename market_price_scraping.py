"""
Description: Webscrape data from Bangladesh Websiter
Author: Harrison Mitchell
Date Modified: 08/27/2020
"""

# import statements
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import csv
import pickle
from pathos.multiprocessing import ProcessingPool as Pool
from webdriver_manager.chrome import ChromeDriverManager
from itertools import islice
import datetime as dt
import math
import os
# initialize webdriver


##################################################### Definitions #####################################################

# months_back = 12  # select how many months back your desired start date is
months_for = 11  # select how many months forward you want to scrape
# months_run = months_back - months_for

# order of loop (from out to in) is as follows:
# loops through all subdistricts, through all months, through each day of the week, through each week of the month

# my_dictionary = {}
def get_day_month_from_day(num_days):
    todays_date = dt.datetime.now() # get todays date
    start_day = dt.datetime.strptime('2019-01-01', '%Y-%m-%d')
    increment_date = start_day + dt.timedelta(days=num_days-1)
    increment_month = abs(increment_date.month - todays_date.month) + 12*(start_day.year-todays_date.year)
    increment_day = abs(increment_date.day - todays_date.day)
    # days
    row_column = [abs((increment_day % 7) ) + 1, abs(increment_day % 5 ) +1 ]
    return increment_month, row_column

def load_webpage(driver, sleep_time = 4):
    """
    :param driver: takes a chrome driver instance
    :return: loads the dialy market price website. then sleeps
    """
    driver.get('http://dam.gov.bd/market_daily_price_report?L=E')
    time.sleep(sleep_time)

def click_months(driver, months_back, z, i, j):
    """
    From http://dam.gov.bd/market_daily_price_report?L=E , tries to click a certain number of months backwards
    :param driver: takes a chrome driver instance
    :param months_back: number of months back to click
    :param z: tbh, no idea
    :param i: day of the week
    :param j: week in the month
    :return:
    """

    prev_month = driver.find_element_by_class_name('xdsoft_prev')

    date_button = driver.find_element_by_id("date")
    date_button.click()
    time.sleep(2)

    # This gets you to your "starting month"
    x = 0
    while x < months_back - z:
        prev_month.click()
        x = x + 1
    time.sleep(2)

    # Goes through days of the month
    day_xpath = "/html/body/div[2]/div[1]/div[2]/table/tbody/tr[{}]/td[{}]/div".format(j, i)
    my_day = driver.find_element_by_xpath(day_xpath)
    my_day.click()
    time.sleep(2)

def select_location(driver,a,b,c,d):
    """
    From http://dam.gov.bd/market_daily_price_report?L=E , navigates to desired location
    :param driver: chrome driver instance
    :param a: Division to scroll to. I.e. 1 corresponds to the first division, 2 to 2nd, etc.
    :param b: District to scroll to
    :param c: Upazila to scroll to
    :param d: Market to scroll to
    :return:
    """
    # Goes through each division, etc you're a smart reader I'm sure
    select_div = Select(driver.find_element_by_id("drp_division_eng"))
    select_div.select_by_index(a)
    time.sleep(4)

    select_dis = Select(driver.find_element_by_id("drp_district_eng"))
    select_dis.select_by_index(b)
    time.sleep(4)

    select_upa = Select(driver.find_element_by_id("drp_subdistrict_eng"))
    select_upa.select_by_index(c)
    time.sleep(4)

    select_mkt = Select(driver.find_element_by_id("drp_market_eng"))
    select_mkt.select_by_index(d)

# select_price = Select(driver.find_element_by_xpath('//*[@id="PriceType_id"]'))
#
# gen_button = driver.find_element_by_css_selector("input[type='submit']")
#
# date_button = driver.find_element_by_id("date")
# date_scroller = driver.find_element_by_css_selector('div.xdsoft_label.xdsoft_year')
# prev_month = driver.find_element_by_class_name('xdsoft_prev')
#
# select_div = Select(driver.find_element_by_id("drp_division_eng"))
#
# options_div = select_div.options
#
# counter = 1

# for index_div in range(0, len(options_div)):
#     select_div.select_by_index(index_div)
#
#     time.sleep(2)
#
#     select_dis = Select(driver.find_element_by_id("drp_district_eng"))
#
#     options_dis = select_dis.options
#
#     for index_dis in range(0, len(options_dis)):
#         select_dis.select_by_index(index_dis)
#
#         time.sleep(2)
#
#         select_upa = Select(driver.find_element_by_id("drp_subdistrict_eng"))
#
#         options_upa = select_upa.options
#
#         for index_upa in range(0, len(options_upa)):
#             select_upa.select_by_index(index_upa)
#
#             time.sleep(2)
#
#             select_mkt = Select(driver.find_element_by_id("drp_market_eng"))
#
#             options_mkt = select_mkt.options
#
#             for index_mkt in range(0, len(options_mkt)):
#
#                 time.sleep(2)
#
#                 my_dictionary["obvs{0}".format(counter)] = "{}_{}_{}_{}".format(index_div, index_dis, index_upa, index_mkt)
#
#                 counter = counter + 1
#
#             select_upa.deselect_by_index(index_upa)
#
#             time.sleep(1)
#
#         select_dis.deselect_by_index(index_dis)
#
#         time.sleep(1)
#
#     select_div.deselect_by_index(index_div)
#
# print(my_dictionary)
#
# f = open("full_dictionary.pkl", "wb")
# pickle.dump(my_dictionary,f)
# f.close()
def get_prices(driver, months_back, z,a,b,c,d,j,i):
    """

    :param driver: Chrome webdriver instance
    :param months_back: Number of months you want to scrape. Works by scraping x months back from todays date.
    :param z: Tbh Not sure what this does
    :param a: Division to scroll to. I.e. 1 corresponds to the first division, 2 to 2nd, etc.
    :param b: District to scroll to
    :param c: Upazila to scroll to
    :param d: Market to scroll to
    :param j: Week in month to select
    :param i: day of the week to select
    :return: Navigates to desired part of website and return an na_check to see if that webpage should be written to csv
    """

    load_webpage(driver=driver)
    try:
        click_months(driver=driver, months_back=months_back, z=z, i=i, j=j)
    except NoSuchElementException:
        print('No such element exception, trying to reload page and scrape again')
        load_webpage(driver=driver)
        click_months(driver=driver, months_back=months_back, z=z, i=i, j=j)

    try:
        select_location(driver=driver,a=a, b=b,c=c,d=d)
    except NoSuchElementException:
        print('No such element exception, trying to reload page and scrape again')
        load_webpage(driver=driver)
        click_months(driver=driver, months_back=months_back, z=z, i=i, j=j)
        select_location(driver=driver, a=a, b=b, c=c, d=d)

    na_check = driver.find_element_by_xpath('//*[@id="frm_filter"]/div/div[4]/div[2]/button/span[1]').text
    return na_check

def get_table(driver):
    select_price = Select(driver.find_element_by_xpath('//*[@id="PriceType_id"]'))
    select_price.select_by_index(1)
    time.sleep(1.5)

    gen_button = driver.find_element_by_css_selector("input[type='submit']")
    gen_button.click()
    time.sleep(2)

    # Now actually writing the table, I'm sure there are more efficient ways of
    # Doing this but hey it's not too slow
    table = driver.find_element_by_xpath('//*[@id="printArea"]/div[2]/table')
    dater = driver.find_element_by_xpath('//*[@id="printArea"]/div[1]')
    rawtitle = driver.find_element_by_xpath('//*[@id="printArea"]/div[1]').text
    titlefinal = rawtitle.replace("\n", "")
    titlefinal = titlefinal.replace("Daily Market Price List ofDistrict - ", "")
    titlefinal = titlefinal.replace(" , Market - ", "_")
    titlefinal = titlefinal.replace("Date: ", "_")
    titlefinal = titlefinal.replace("/", "_")
    return [table, titlefinal]


def scrape_prices(months_for, suffix, my_dictionary, download_folder, skip_vals):
    months_back = 12
    months_run = months_back - months_for
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('http://dam.gov.bd/market_daily_price_report?L=E')
    with open(skip_vals) as text_file:
        skip_list = [link.rstrip() for link in text_file]
    text_file = open(skip_vals, mode='a+')
    for z in range(0,12): # months in a year
        for i in range(1, 8): # days of the week
            for j in range(1, 6):  # weeks of the month
                for value in my_dictionary.values():
                    value = value + '_' + str(i) + '_' + str(j) + '_' + str(z)
                    if value not in skip_list:
                        print(value)
                        newval = value.replace("{", "")
                        newval = newval.replace("}_{", " ")
                        newval = newval.replace("}", "")
                        newval = newval.replace("_", " ")
                        a, b, c, d, e, f, g = (int(x) for x in newval.split())
                        try:
                            # get num_click from e
                            # num_month_clicks = get_day_month_from_day(e)[0]
                            # row_column = get_day_month_from_day(e)[1]
                            # Have to refresh page each time
                            na_check = get_prices(
                                    driver=driver,
                                    a=a,
                                    b=b,
                                    c=c,
                                    d=d,
                                    i=i,
                                    j=j,
                                    months_back=months_back,
                                    z=g
                                )

                        except NoSuchElementException:
                            print('Unable to access element for {}'.format(value))
                            # reload the web page
                            na_check = get_prices(
                                driver=driver,
                                a=a,
                                b=b,
                                c=c,
                                d=d,
                                i=i,
                                j=j,
                                months_back=months_back,
                                z=z
                            )
                        if na_check == 'No Market Found!':
                            print("no market here")
                            text_file.write('{} \n'.format(value))
                        else:
                            time.sleep(1.5)
                            try:
                                results = get_table(driver=driver)
                            except NoSuchElementException:
                                na_check = get_prices(
                                    driver=driver,
                                    a=a,
                                    b=b,
                                    c=c,
                                    d=d,
                                    i=i,
                                    j=j,
                                    months_back=months_back,
                                    z=g
                                )
                                results = get_table(driver=driver)
                            table = results[0]
                            titlefinal = results[1]

                            with open(download_folder + titlefinal + '.csv', 'w', newline='') as csvfile:
                                wr = csv.writer(csvfile)
                                # wr.writerow(c.text for c in dater.find_elements_by_xpath('//*[@id="printArea"]/div[1]'))
                                for row in table.find_elements_by_css_selector('tr'):
                                    wr.writerow([d.text for d in row.find_elements_by_css_selector('th')])
                                    wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
                            text_file.write('{} \n'.format(value))
                            time.sleep(3)
                    else:
                        print('skipping {}'.format(value))


                time.sleep(10)

def split_dicts(dictionary, n_partions):
    dict_list = []
    it = iter(dictionary)
    SIZE = len(dictionary) // n_partions
    for i in range(0, len(dictionary), SIZE):
        dict_list.append({k: dictionary[k] for k in islice(it, SIZE)})
    return dict_list


if __name__ =='__main__':
    with open('/Users/joefish/Downloads/dict_1st_half.pickle', 'rb') as f:
        my_dictionary = pickle.load(f)
    # dict_vals = my_dictionary.values()
    list_of_suffixes = ['_' + str(x) for x in range(1, 366)]
    # dict_vals_duplicated_suffix = [x + suffix for suffix in list_of_suffixes for x in dict_vals]
    # new_list = [str(x) for x in range(len(dict_vals_duplicated_suffix))]
    # new_dict = dict(zip(new_list, dict_vals_duplicated_suffix))
    list_of_dicts = split_dicts(my_dictionary, n_partions=4)
    get_day_month_from_day(1)
    with Pool(4) as p:
        p.map(scrape_prices, [months_for]*len(list_of_dicts), list_of_suffixes*len(list_of_dicts), list_of_dicts,
              ['/Users/joefish/Desktop/market_prices/']*len(list_of_dicts),
              ['/Users/joefish/Desktop/market_prices/skip_vals.txt']*len(list_of_dicts))
    p.close()
    p.join()

