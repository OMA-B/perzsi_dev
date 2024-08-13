import pandas as pd, time, os, threading
from selenium import webdriver
from selenium.webdriver.common.by import By


def verify_image_process(folder):
    
    driver = webdriver.Chrome()
    driver.get(url='https://google.com')

    for filename in os.listdir(path=folder):
        # create dataframe from csv
        print(f'\n\ncurrent file: {filename}')
        csv_df = pd.read_csv(filepath_or_buffer=f'{folder}\{filename}')

        print(f"there are {len(csv_df['AVAILABILITY'])} items in file...")

        # segregate image_link column and loop through the links in the column
        image_links = csv_df['IMAGE_LINK']
        if filename == 'GameFly_Online_Video_Game_Rentals-Rentals_Catalog-shopping.csv':
            image_links = image_links[1990:]
        elif filename == 'Sobelia-Product_feed_US_Google_Shopping-shopping.csv':
            image_links = image_links[160:]
        elif filename == 'Aosom_com-Aosom_US_Product_Feed-shopping.csv':
            image_links = image_links[2500:]
        elif filename == 'LightsOnline_com-LightsOnline_Feed-shopping.csv':
            image_links = image_links[2380:]
        
        for index, link in image_links.items():
            # open each link in the browser
            driver.get(url=link)
            time.sleep(2)
            # confirm if image is displayed by checking if the image link is valid
            try:
                driver.find_element(By.TAG_NAME, 'img').is_displayed() 
                if driver.find_element(By.TAG_NAME, 'img').get_attribute('src') == link: 
                    if index % 10 == 0: print(f"{index} of {len(csv_df['AVAILABILITY'])} - {filename}")
            except:
                # if not valid, get the row of the invalid image link and delete
                csv_df.drop(index, inplace=True)
                print(f'image {link} is invalid. {index} - {filename}')

        # reset dataframe index labelling
        csv_df.reset_index(drop=True, inplace=True)

        # after verification, convert df back to csv and save in a separate folder
        csv_df.to_csv(path_or_buf=f'image_verified\{filename}', index=False)

        os.remove(path=f'{folder}\{filename}')


# create Thread objects
thread1 = threading.Thread(target=verify_image_process, args=('unsorted',))
thread2 = threading.Thread(target=verify_image_process, args=('unsorted2',))
thread3 = threading.Thread(target=verify_image_process, args=('unsorted3',))
thread4 = threading.Thread(target=verify_image_process, args=('unsorted4',))

# start Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# join Threads
thread1.join()
thread2.join()
thread3.join()
thread4.join()

print('Done verifying...\nAll Threads executed!')