from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

""" 
    Grab images:
        - data-testid="image-picture-image" -> selected strain picture (on strain page).
        - data-testid="image-single-image" -> if strain contains multiple images, then
            this captures those smaller displayed images.

 """

driver = webdriver.Safari();

def format_strain_name(raw_name):
    return raw_name.lower().replace(" ","_");

def format_strain_active_ingredient(raw_active_ingredient):
    """
        Examples:
            "THC 20%" to (THC, 20)
            "CBD 0%" to (CBD, 0)
    """
    if raw_active_ingredient[0] == 'L':
        raw_active_ingredient = raw_active_ingredient.split("...")[1];
    mid_process_text = raw_active_ingredient.split(" ");
    active_ingredient_name = mid_process_text[0];
    active_ingredient_value = int(mid_process_text[1].split("%")[0]);
    return (active_ingredient_name, active_ingredient_value);

def srcset_to_250link(srcset, replace_width):
    link = srcset.split("x,");
    res_change_split = link[1].split("w="+str(replace_width));
    return res_change_split[0][1:] + "w=250" + res_change_split[1].split(" ")[0];

def file_to_list_link():
    file = open('strains_link.txt', 'r');
    links = file.readlines();
    file.close();
    return links;

def main():
    # TODO: looop through file_to_list_link()

    driver.get(file_to_list_link()[0]);
    print("URL: " + driver.current_url);
    """
        I really not a fan of stalling the program but a 1s sleep time seems
        to ensure everything goes as expected (page loads -> scrape operations).
        But, because there are only 6192 pages to scrape, this sets an acceptable
        minimum of 6192 seconds (1h:43m) for the execution time. It is acceptable
        since this only needs to be run a single time.
    """
    time.sleep(1);

    # Name
    try:
        #name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/h1[@itemprop="name"]')));
        name = WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.XPATH, './/h1[@itemprop="name"]').get_attribute("innerHTML"));
        try:
            print(format_strain_name(name));
        except Exception as e:
            print(e);
            print("Error when formatting strain name.");
    except Exception as e:
        print(e);
        print("Couldn't find name.");

    # Type - Indica, Hybrid, Sativa.
    # class="inline-block text-xs px-sm py-xs rounded font-bold text-default bg-leafly-white"
    try:
        type = WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.XPATH, './/span[@class="inline-block text-xs px-sm py-xs rounded font-bold text-default bg-leafly-white"]').get_attribute("innerHTML"));
        type = type.lower();
        print(type);
    except Exception as e:
        print(e);
        print("Couldn't find type.");

    # Active ingredients - THC, CBD, CBG,...
    try:
        active_ingredients = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@class="text-xs rounded flex items-center mr-xl"]')));
        try:
            print(format_strain_active_ingredient(active_ingredients[0].text));
            print(format_strain_active_ingredient(active_ingredients[1].text));
        except Exception as e:
            print(e);
            print("Error when formatting strain active ingredients.");
    except Exception as e:
        print(e);
        print("Couldn't find THC/CBD/CBG/...")
    
    # Terpene
    try:
        terpene = WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.XPATH, './/span[@class="ml-sm"]').get_attribute("innerHTML"));
        terpene = terpene.lower();
        print(terpene);
    except Exception as e:
        print(e);

    # Small/To-select strain images URL's
    try:
        small_images = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, './/img[@data-testid="image-single-image"]')));
        for img in small_images:
            try:
                print(srcset_to_250link(img.get_attribute("srcset"), 50));
            except Exception as e:
                small_images = None;
                print(e);
                print("Error when transforming smaller pictures link.");
    except Exception as e:
        small_images = None;
        print(e);
        print("Couldn't find small images.");

    if small_images == None:
        # Big/Inital presented strain picture
        try:
            global big_image;
            big_image = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, './/img[@data-testid="image-picture-image"]')));
            try:
                print(srcset_to_250link(big_image.get_attribute("srcset"), 295));
            except Exception as e:
                print(e);
                print("Error when transforming big picture link.");
        except Exception as e:
            print(e);
            print("Couldn't find larger initial picture.");

    # Effects & Flavors
    try:
        effects_and_flavors = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/p[@data-testid="item-name"]')));
        # Positive effects
        for effect in effects_and_flavors[:3]:
            print(effect.get_attribute("innerHTML"));
        # Negative effects
        for effect in effects_and_flavors[3:6]:
            print(effect.get_attribute("innerHTML"));
        # Flavors
        for flavor in effects_and_flavors[6:9]:
            print(flavor.get_attribute("innerHTML"));
    except Exception as e:
        print(e);

    """
        TODO: Having all the gathered data, instantiate Strain object and append it to .csv file.
        Also, log exceptions/errors along with it's leafly page number.
    """


main();