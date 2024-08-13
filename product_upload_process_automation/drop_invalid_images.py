import pandas as pd, pprint, shutil, os, requests


txt_filename = 'invalids\invalid_images_2.txt'
foldername = 'unsorted2'

# open and read invalid images txt file into a list
with open(file=txt_filename, mode='r') as txt_file:
    invalid_images_list = txt_file.read().splitlines()

csv_filename = invalid_images_list[0].strip().split(' ')[-1]
filepath = f'{foldername}\{csv_filename}'
csv_df = pd.read_csv(filepath_or_buffer=filepath, encoding='ISO-8859-1')

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
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

invalid_image_counter = 0

for invalid_image in invalid_images_list:

    image_link = invalid_image.strip().split(' ')[1]
    csv_filename = invalid_image.strip().split(' ')[-1]

    # open each link in the browser
    if verify_image_link(url=image_link): pass
    else:
        # if not valid, get the row of the invalid image link and delete
        # segregate image_link column and loop through the links in the column
        image_links = csv_df['IMAGE_LINK']
        
        for index, link in image_links.items():
            if link == image_link:
                csv_df.drop(index, inplace=True)

        # reset dataframe index labelling
        csv_df.reset_index(drop=True, inplace=True)

        print(f'\ndropped {image_link}\n')

        invalid_image_counter += 1

# after verification, convert df back to csv and save in a separate folder
csv_df.to_csv(path_or_buf=f'filtered_unsorted\{csv_filename}', index=False)

os.remove(path=filepath)

shutil.move(src=f'filtered_unsorted\{csv_filename}', dst=filepath)

print(f'{invalid_image_counter} images were invalid.\n')