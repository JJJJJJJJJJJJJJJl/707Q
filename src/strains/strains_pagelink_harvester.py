""" 

    Script meant to collect all strains link.

 """

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MAX_PAGE = 344;

""" 
    -> Ok, so 21 button only shows up on the first website access, so
    it could have an initial access, prior to pages scrapping, just 
    to get rid of this button. †get_rid_of_21_button()†

    -> There are currently 344 pages containing 18 strains each.

 """

driver = webdriver.Safari();

def get_rid_of_21_button():
    url = "https://www.leafly.com/strains?itm_source=blast&itm_medium=sp-hero&itm_campaign=trf-all-strain-marquee-usa-all&page=1";
    driver.get(url);
    driver.refresh();
    try:
        button_21 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/button[@data-testid="age-gate-yes-button"]')));
        button_21.click();
    except Exception as e:
        print(e);
    return;

def save_links(link_list):
    file = open('strains_link.txt', 'a');
    for link in link_list:
        file.writelines(link+"\n");

    file.close()
    return;

def get_strains_page_links():
    # This collects all 18 strains in a single page, can we loop it with no problems? lets try :)
    # OK seems to work just fine *-* (thank fcin god...)
    for i in range(1, MAX_PAGE+1):
        strains_link = [];
        try:
            url = "https://www.leafly.com/strains?itm_source=blast&itm_medium=sp-hero&itm_campaign=trf-all-strain-marquee-usa-all&page="+str(i);
            driver.get(url);
            strains_a_element = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/a[@class="p-md"]')));
            for a in strains_a_element:
                link = a.get_attribute('href');
                print(link);
                strains_link.append(link);
            save_links(strains_link);
            print("Page: " + str(i) + " successfully downloaded :)");
        except Exception as e:
            print(e);
            print("Page: " + str(i) + " unsuccessfully downloaded :(");
    return;

def main():
    get_rid_of_21_button();
    get_strains_page_links();
    
    return 0;

main();