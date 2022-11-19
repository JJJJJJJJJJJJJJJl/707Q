from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from strain import Strain, Type, Effect, Terpene, Flavor, Enum
import pandas as pd
import csv

FILENAME = "jjjjjjdataset.csv";
MAX_LINK = 6192;

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
    """ if i ever come back to this, start from 2056 (last checkpointon strains_list)
        reason i stopped was because less known strains have literaly no data, 
        just default images (bad!) and nothing else (some effects and flavors, but
        are they even trustworthy?? prob not) so yea, at the moment i'm writting this
        the dataset has currently data over 2057 strains which is pretty good for what
        im looking for to do with it.
    """ 
    for page in range(2056, MAX_LINK):
        while True:
            try:
                driver.get(file_to_list_link()[page]);
                break;
            except Exception as e:
                print(e);
        print("URL: " + driver.current_url);
        """
            I'm really not a fan of stalling the program but a 1s sleep time seems
            to ensure everything goes as expected (page loads -> scrape operations).
            But, because there are only 6192 pages to scrape, this sets an acceptable
            minimum of 6192 seconds (1h:43m) for the execution time. It is acceptable
            since this only needs to be run a single time.
        """
        time.sleep(1);

        # Name
        try:
            global name; name = "";
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
        try:
            global type; type = Type.nan;
            type_element = WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.XPATH, './/span[@class="inline-block text-xs px-sm py-xs rounded font-bold text-default bg-leafly-white"]').get_attribute("innerHTML"));
            type = Type[type_element.lower()];
            print(type);
        except Exception as e:
            print(e);
            print("Couldn't find type.");

        # Active ingredients - THC, CBD, CBG,...
        try:
            global thc, cbd, cbg; thc = -1; cbd = -1; cbg = -1;
            active_ingredients = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@class="text-xs rounded flex items-center mr-xl"]')));
            try:
                first_active = format_strain_active_ingredient(active_ingredients[0].text);
                second_active = format_strain_active_ingredient(active_ingredients[1].text);
                if first_active[0] == "THC":
                    thc = first_active[1];
                elif first_active[0] == "CBD":
                    cbd = first_active[1];
                else: cbg = first_active[1];
                if second_active[0] == "THC":
                    thc = second_active[1];
                elif second_active[0] == "CBD":
                    cbd = second_active[1];
                else: cbg = second_active[1];
            except Exception as e:
                print(e);
                print("Error when formatting strain active ingredients.");
        except Exception as e:
            print(e);
            print("Couldn't find THC/CBD/CBG/...")
        
        # Terpene
        try:
            global terpene; terpene = Terpene.nan;
            terpene_element = WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.XPATH, './/span[@class="ml-sm"]').get_attribute("innerHTML"));
            terpene = Terpene[terpene_element.lower()].name;
            print(terpene);
        except Exception as e:
            print(e);

        # Small/To-select strain images URL's
        try:
            global small_images; small_images = [];
            small_images_elements = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, './/img[@data-testid="image-single-image"]')));
            for img in small_images_elements:
                try:
                    print(srcset_to_250link(img.get_attribute("srcset"), 50));
                    small_images.append(srcset_to_250link(img.get_attribute("srcset"), 50));
                except Exception as e:
                    print(e);
                    print("Error when transforming smaller pictures link.");
        except Exception as e:
            print(e);
            print("Couldn't find small images.");

        # Big/Inital presented strain picture (only if small images don't exist)
        global big_image; big_image = [];
        if len(small_images) == 0:
            try:
                big_image_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, './/img[@data-testid="image-picture-image"]')));
                try:
                    print(srcset_to_250link(big_image_element.get_attribute("srcset"), 295));
                    big_image.append(srcset_to_250link(big_image_element.get_attribute("srcset"), 295));
                except Exception as e:
                    print(e);
                    print("Error when transforming big picture link.");
            except Exception as e:
                print(e);
                print("Couldn't find larger initial picture.");

        # Effects & Flavors
        try:
            global effects; effects = [];
            global flavors; flavors = [];
            effects_and_flavors = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/p[@data-testid="item-name"]')));
            for ef in effects_and_flavors:
                added = False
                processed = ef.get_attribute("innerHTML").lower().replace(" ","_").replace("/","_");
                for effect in Effect:
                    if effect.name == processed:
                        effects.append(Effect[processed].name);
                        added = True
                        break;
                if added == False:
                    flavors.append(Flavor[processed].name);
        except Exception as e:
            print(e);

        """
            TODO: Having all the gathered data, instantiate Strain object and append it to .csv file.
            Also, log exceptions/errors along with it's leafly page number.
        """
        dp = Strain(name=name, images=small_images+big_image, 
                        type=type, main_effect=effects[0] if len(effects) > 0 else [],
                        effects=effects, thc=thc, 
                        cbd=cbd, cbg=cbg, main_terpene=terpene, 
                        main_flavor=flavors[0] if len(flavors) > 0 else [], flavors=flavors);

        try:
            with open(FILENAME, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([dp.name, dp.images, dp.type.name,
                                dp.main_effect, dp.effects, dp.thc,
                                dp.cbd, dp.cbg, dp.main_terpene, 
                                dp.main_flavor, dp.flavors])
        except BaseException as e:
            print('BaseException:', FILENAME)
        

main();