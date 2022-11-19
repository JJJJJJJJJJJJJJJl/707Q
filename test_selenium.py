from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#import numpy as np
import time;

BASE_URL = "https://www.leafly.com/";

def main():
    driver = webdriver.Safari();
    url = BASE_URL+"strains?itm_source=blast&itm_medium=sp-hero&itm_campaign=trf-all-strain-marquee-usa-all&page=1";
    driver.get(url);
    #element = driver.find_element(By.CSS_SELECTOR, ".button.button--primary.text-sm");
    #data-testid="age-gate-yes-button"
    try:
        im21but = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, './/button[@data-testid="age-gate-yes-button"]')));
        im21but.click();
    except Exception as e:
        print(e);
    #strains = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jsx-72b23e4c6be41632.col")));
    #strains_name =  WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@itemprop="name"]')));
    #class="p-md"
    clean_strains_link = [];
    try:
        strains_link =  WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/a[@class="p-md"]')));
        for a in strains_link:
            clean_strains_link.append(a.get_attribute('href'))
    except Exception as e:
        print(e);
    for a in clean_strains_link:
        print(a);
    print(driver.current_url);
    for j in range(0, 18):
        print(driver.page_source[0]);
        print("strain: " + str(j));
        try:
            driver.get(clean_strains_link[j]);
        except Exception as e:
            print(e);
        print("CURRENT URL: " + driver.current_url);
        # I am not sure why but this line enables imgs variable access...i dont fckin know why man wtf
        print(driver.page_source[0]);
        imgs = [];
        clean_strain_imgs_link = [];
        try:
            imgs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, './/img[@data-testid="image-single-image"]')));
            for img in imgs:
                print(driver.page_source[0]);
                try:
                    clean_strain_imgs_link.append(img.get_attribute('srcset'));
                except Exception as e:
                    print(e);
        except Exception as e:
            print(e);
            
        for i in range(0, len(clean_strain_imgs_link)):
            print("image: " + str(i));
            srcset = clean_strain_imgs_link[i];
            link = srcset.split("x,");
            res_change_split = link[1].split("w=50");
            final_link = res_change_split[0] + "w=500" + res_change_split[1];
            print(final_link);
    """ print(driver.current_url);
    strains[0].click();
    driver.switch_to.window(driver.window_handles[0]); """
    #itemprop="name"
    """ print(strains[0].text);
    strains[0].click(); """
    """ strain_pics = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, f'.//img[@alt="Picture of {strains_name[0].text}"]')))
    print(len(strain_pics))
    print(strain_pics[0].get_attribute('srcset')); """
    #print(strains_pic[0].get_attribute('srcset'));
    #print(strains_pic[1].get_attribute('srcset'));

    #print(strains[0].find_element(By.XPATH, './/span[@itemprop="name"]').text);
    #media="(min-width: 1025px)"
    #print(strain_0.find_element(By.XPATH, './/span[@media="(min-width: 1025px)"]'));


    """ time.sleep(3);
    button_21_yes = driver.find_elements(By.CLASS_NAME, "button button--primary text-sm");
    time.sleep(3);
    button_21_yes.click(); """
    #time.sleep(60);
    """ driver = webdriver.Safari();
    data = np.zeros((1, MAX_SIZE));
    page_number = INITIAL_PAGE;
    while 1:
        print("Page: ", page_number);
        url = "https://csgoempire.com/history?seed=" + str(page_number);
        driver.get(url);
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "grid")))
        grid = driver.find_elements(By.CLASS_NAME, "grid");
        #page_number > 2500 condition because some pages
        #in between (eg.: page 200 is empty for some reason)
        #are empty so this makes sure it doesnt break on those
        if len(grid[0].text) == 0 and page_number > 2500:
            break;
        if len(grid[0].text) > 0:
            rounds = digest(grid[0].text);
            rounds = process(rounds);
            data = np.append(data, rounds, axis=0);
        page_number += 1;
    data = np.delete(data, 0, axis=0);
    np.save("data", data);
    driver.close(); """

main();