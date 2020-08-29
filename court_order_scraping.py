from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException
import time
import re
from data_constants import *
from webdriver_manager.chrome import ChromeDriverManager

def scrape_urls(url_dict, download_path, headless=False, downloaded_links=downloaded_links):
    chromeOptions = webdriver.ChromeOptions()
    if headless is not False:
        chromeOptions.add_argument('--headless')
    prefs = {"plugins.always_open_pdf_externally": True,
             'download.default_directory': download_path
             }
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions)
    # driver = webdriver.Chrome(executable_path="/Users/joefish/Downloads/chromedriver", chrome_options=chromeOptions)
    with open(downloaded_links) as text_file:
        link_list = [link.rstrip() for link in text_file]
    text_file = open(downloaded_links, mode='a+')
    for url in url_dict.keys():
        print('scraping {}'.format(url_dict[url][4]))
        driver.get(url)
        driver.implicitly_wait(10)
        if state_url_dict[url][0] is dict:
            if 'click' in state_url_dict[url][0].keys():
                for xpath in state_url_dict[url][0]['click']:
                    driver.find_element_by_xpath(xpath).click()
        h_links = driver.find_elements_by_tag_name('a')
        # link_text=[str(h_link.get_attribute('href')) for h_link in h_links]
        # print('\n'.join(link_text))
        for h_link in h_links:
            try:
                Initial_path = str(h_link.get_attribute('href'))
                if re.search(r'([^/]+)(\.(pdf|xlsx|csv|txt|docx?|rtf|tex))', Initial_path, flags=re.IGNORECASE) is not None or \
                    re.search(r'(download|embedDocument)', Initial_path, flags=re.IGNORECASE) is not None:
                    file_list = [re.sub(r'([^/]+)(\.[a-z]+)',r'\g<1>\g<2>', file, flags=re.IGNORECASE) for file in os.listdir(download_path)]
                    Initial_path = re.sub('%20', ' ', Initial_path)
                    path_regex = re.search(r'([^/]+)(\.(pdf|xlsx|csv|txt|docx?|rtf|tex))', Initial_path, flags=re.IGNORECASE)
                    file_extension = path_regex.group(2) if path_regex is not None else ''
                    file_name = path_regex.group(1) if path_regex is not None else Initial_path
                    file_path = file_name + file_extension
                    new_path = url_dict[url][4] + '_' + file_name + file_extension
                    if file_path not in file_list and new_path not in file_list and file_path + '_' + url_dict[url][4] not in link_list:
                        try:
                            time.sleep(4)
                            h_link.click()
                            total_time = 0
                            print('downloading {} to {}'.format(file_path, download_path))
                            while file_path not in file_list and total_time < 12:
                                file_list = [re.sub(r'([^/]+)(\.[a-z]+)', r'\g<1>\g<2>', file, flags=re.IGNORECASE) for file in
                                             os.listdir(download_path)]
                                time.sleep(4)
                                total_time = total_time + 4
                                # if total_time > 10:
                                #     body = driver.find_element_by_tag_name('body')
                                #     body.send_keys(Keys.COMMAND, 's')
                            if file_path in file_list:
                                print('renaming {} to {} '.format(os.path.join(download_path, Initial_path),
                                                                  os.path.join(download_path, new_path)))
                                os.rename(os.path.join(download_path, file_path), os.path.join(download_path, new_path))
                            else:
                                print('unable to rename {}'.format(file_path))
                        except ElementNotInteractableException:
                            print('PDF not interactable skipping {}'.format(file_path))
                        except ElementClickInterceptedException:
                            print('Click intercepted skipping {}'.format(file_path))
                            # next(file_path)
                        text_file.write('{} \n'.format(file_path + '_' + url_dict[url][4]))
                    else:
                        print('{} already downloaded'.format(file_path))
                        print(h_link.text)
            except StaleElementReferenceException:
                print('stale element, pdf not accessible')
                driver.back()
                # # for tab in range(len(driver.window_handles),1):
                #     driver.switch_to_window(driver.window_handles[tab]).close()
        driver.implicitly_wait(10)

    driver.quit()
    text_file.close()

if __name__ == '__main__':
    scrape_urls(url_dict=state_url_dict, download_path=state_download_path)
    scrape_urls(emily_dict, download_path=emily_download_path)