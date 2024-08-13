import pandas as pd, os, pprint

# global variables
cat_levels = []
prod_cat_levels_df = pd.read_csv(filepath_or_buffer='products_cat_levels.csv')
level_two_checklist = prod_cat_levels_df['level_two'].to_list()
foldername = 'image_verified'

# list out the directory
for filename in os.listdir(foldername):
    # read the CSV file
    csv_df = pd.read_csv(filepath_or_buffer=f'{foldername}\{filename}')

    print(f'\ncurrent file: {filename}')
    # segregate the product level column
    google_prod_cat = csv_df['GOOGLE_PRODUCT_CATEGORY_NAME']
    prod_type = csv_df['PRODUCT_TYPE']
    # loop through and split items into list
    def segregate_categories(cat_column):
        for cat in cat_column:
            try:
                level_list = cat.split('>')
                # check if list len is greater than 1
                if len(level_list) > 1:
                    # then get level one and two
                    level_one = level_list[0].strip()
                    level_two = level_list[1].strip()
                # if list len is greater than 2, get level three
                level_three = level_list[2].strip() if len(level_list) > 2 else ''
                if level_two not in level_two_checklist or level_two in ('Pet Supplies', 'Toys'):
                    cat_levels.append((level_one, level_two, level_three))
                    level_two_checklist.append(level_two)
            except: continue

    if google_prod_cat[1] != '':
        segregate_categories(cat_column=google_prod_cat)
    elif prod_type[1] != '':
        segregate_categories(cat_column=prod_type)
# structure them together to make a dataframe
levels_frame = {
    'level_one': prod_cat_levels_df['level_one'].to_list() + [cat[0] for cat in cat_levels],
    'level_two': prod_cat_levels_df['level_two'].to_list() + [cat[1] for cat in cat_levels],
    'level_three': prod_cat_levels_df['level_three'].to_list() + [cat[2] for cat in cat_levels],
    'IDCTG_1': prod_cat_levels_df['IDCTG_1'].to_list() + ['' for cat in cat_levels],
    'IDCTG_2': prod_cat_levels_df['IDCTG_2'].to_list() + ['' for cat in cat_levels],
    'IDCTG_3': prod_cat_levels_df['IDCTG_3'].to_list() + ['' for cat in cat_levels],
    'IDCTG_2_kids': prod_cat_levels_df['IDCTG_2_kids'].to_list() + ['' for cat in cat_levels],
    'IDCTG_2_adult_male': prod_cat_levels_df['IDCTG_2_adult_male'].to_list() + ['' for cat in cat_levels],
    'IDCTG_2_adult_female': prod_cat_levels_df['IDCTG_2_adult_female'].to_list() + ['' for cat in cat_levels],
    'IDCTG_3_kids': prod_cat_levels_df['IDCTG_3_kids'].to_list() + ['' for cat in cat_levels],
    'IDCTG_3_adult_male': prod_cat_levels_df['IDCTG_3_adult_male'].to_list() + ['' for cat in cat_levels],
    'IDCTG_3_adult_female': prod_cat_levels_df['IDCTG_3_adult_female'].to_list() + ['' for cat in cat_levels],
}
new_csv_df = pd.DataFrame(data=levels_frame)
# save dataframe to CSV file
new_csv_df.to_csv(path_or_buf='products_cat_levels.csv', index=False)