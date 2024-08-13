import pandas as pd, time, os, requests
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get(url='https://google.com')

def use_selenium(url):
    driver.get(url=url)
    time.sleep(0.5)
    # confirm if image is displayed by checking if the image url is valid
    driver.find_element(By.TAG_NAME, 'img').is_displayed() 
    if driver.find_element(By.TAG_NAME, 'img').get_attribute('src') == url: return True

def verify_image_link(url):
    """
    Verifies if an image URL is accessible.
    
    :param url: URL of the image.
    :return: True if the image is accessible, False otherwise.
    """
    try:
        response = requests.get(url, timeout=10)
        # Check if the response status code is 200 (OK) and the content type is an image
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            return True
        else:
            try: return use_selenium(url=url)
            except: return False
    # except requests.RequestException as e:
    except Exception as e:
        try: return use_selenium(url=url)
        except: return False


for filename in os.listdir(path='unsorted'):
    # create dataframe from csv
    print(f'\n\ncurrent file: {filename}')
    csv_df = pd.read_csv(filepath_or_buffer=f'unsorted\{filename}', encoding='ISO-8859-1')

    print(f"there are {len(csv_df['AVAILABILITY'])} items in file...")

    # segregate image_link column and loop through the links in the column
    image_links = csv_df['IMAGE_LINK']
    if filename == 'BOOKSAMILLION_COM-Books_A_Million_Product_Feed-shopping.csv':
        image_links = image_links[59960:]
    
    for index, link in image_links.items():
        # open each link in the browser
        try:
            if verify_image_link(url=link):
                if index % 10 == 0: print(f"{index} of {len(csv_df['AVAILABILITY'])} - {filename}")
            else:
                # if not valid, get the row of the invalid image link and delete
                csv_df.drop(index, inplace=True)
                try:
                    with open(file='invalids\invalid_images_1.txt', mode='+a') as txt_file:
                        txt_file.write(f'image {link} is invalid. {index} - {filename}\n')
                except: pass
                print(f'image {link} is invalid. {index} - {filename}')
        except: pass

    # reset dataframe index labelling
    csv_df.reset_index(drop=True, inplace=True)

    # after verification, convert df back to csv and save in a separate folder
    csv_df.to_csv(path_or_buf=f'image_verified\{filename}', index=False)

    os.remove(path=f'unsorted\{filename}')