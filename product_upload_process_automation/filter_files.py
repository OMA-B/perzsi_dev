import pandas as pd, time, os


for filename in os.listdir(path='unsorted'):
    # create dataframe from csv
    print(f'\n\ncurrent file: {filename}')
    csv_df = pd.read_csv(filepath_or_buffer=f'unsorted\{filename}')

    # first check for products that are not in stock, to be deleted
    print(f"there are {len(csv_df['AVAILABILITY'])} items before filter...")
    for index, item in csv_df['AVAILABILITY'].items():
        if item not in ('in stock', 'in_stock'):
            csv_df.drop(index, inplace=True)
        
    # reset dataframe index labelling
    csv_df.reset_index(drop=True, inplace=True)
    print(f"there are now {len(csv_df['AVAILABILITY'])} items after filter.")

    # after verification, convert df back to csv and save in a separate folder
    csv_df.to_csv(path_or_buf=f'filtered_unsorted\{filename}', index=False)

    os.remove(path=f'unsorted\{filename}')