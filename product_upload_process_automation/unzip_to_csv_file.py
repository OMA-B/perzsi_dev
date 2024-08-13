import zipfile
import os

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

for filename in os.listdir(path='unzipped'):
    zip_path = f'unzipped\{filename}'
    extract_to = 'unsorted'

    # Ensure the extraction directory exists
    os.makedirs(extract_to, exist_ok=True)

    extract_zip(zip_path, extract_to)

    print(f'Extracted {zip_path} to {extract_to}')


for filename in os.listdir(path='unsorted'):
    os.rename(src=f'unsorted\{filename}', dst=f'unsorted\{filename.split(".")[0]}.csv')