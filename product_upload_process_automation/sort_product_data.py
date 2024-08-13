import pandas as pd, os


# open products cat level file
products_cat_levels = pd.read_csv(filepath_or_buffer='products_cat_levels.csv')

# open store data
folder = 'image_verified'

for filename in os.listdir(path=folder):

    store_product_data = pd.read_csv(filepath_or_buffer=f'{folder}\{filename}')

    print(f'\ncurrent file: {filename}')

    # loop through and split items into list
    for index, row in store_product_data.iterrows():
        # segregate the product level column
        cat = row['GOOGLE_PRODUCT_CATEGORY_NAME'] if row['GOOGLE_PRODUCT_CATEGORY_NAME'] is not None else row['PRODUCT_TYPE']
        if str(cat) != '':
            level_list = str(cat).split('>')
            # then get level one
            level_one = level_list[0].strip()
            # check if list len is greater than 1, then get level two
            level_two = level_list[1].strip() if len(level_list) > 1 else ''
            # if list len is greater than 2, get level three
            level_three = level_list[2].strip() if len(level_list) > 2 else ''
            # loop through products_cat_levels and check if categories match and assign apposite cat levels
            for cat_index, cat_row in products_cat_levels.iterrows():
                if level_one is not None and level_one == cat_row['level_one']: store_product_data.at[index, 'UNIT_PRICING_MEASURE'] = cat_row['IDCTG_1']
                if level_two is not None:
                    # check if product belongs to fashion, to be able discern if kids or adult male or female
                    if level_one in ('Apparel & Accessories', 'Luggage & Bags') and level_two == cat_row['level_two']:
                        if row['AGE_GROUP'] != 'adult': store_product_data.at[index, 'UNIT_PRICING_BASE_MEASURE'] = cat_row['IDCTG_2_kids']
                        else: store_product_data.at[index, 'UNIT_PRICING_BASE_MEASURE'] = cat_row['IDCTG_2_adult_female'] if row['GENDER'] == 'female' else cat_row['IDCTG_2_adult_male']
                    elif level_two == cat_row['level_two']:
                        if cat_row['level_two'] in ('Pet Supplies', 'Toys'):
                            if level_three == cat_row['level_three']: store_product_data.at[index, 'UNIT_PRICING_BASE_MEASURE'] = cat_row['IDCTG_2']
                        else: store_product_data.at[index, 'UNIT_PRICING_BASE_MEASURE'] = cat_row['IDCTG_2']
                if level_three is not None:
                    # check if product belongs to fashion, to be able discern if kids or adult male or female
                    if level_one in ('Apparel & Accessories', 'Luggage & Bags') and level_three == cat_row['level_three']:
                        if row['AGE_GROUP'] != 'adult':
                            if pd.isna(cat_row['IDCTG_3_kids']) or str(cat_row['IDCTG_3_kids']).strip() == '': pass
                            else: store_product_data.at[index, 'INSTALLMENT'] = cat_row['IDCTG_3_kids']
                        else: 
                            if pd.isna(cat_row['IDCTG_3_adult_female']) or str(cat_row['IDCTG_3_adult_female']).strip() == '' and pd.isna(cat_row['IDCTG_3_adult_male']) or str(cat_row['IDCTG_3_adult_male']).strip() == '': pass
                            else: store_product_data.at[index, 'INSTALLMENT'] = cat_row['IDCTG_3_adult_female'] if row['GENDER'] == 'female' else cat_row['IDCTG_3_adult_male']
                    elif level_three == cat_row['level_three']:
                        if pd.isna(cat_row['IDCTG_3']) or str(cat_row['IDCTG_3']).strip() == '': pass
                        else: store_product_data.at[index, 'INSTALLMENT'] = cat_row['IDCTG_3']

            # remove USD from prices
            if str(row['PRICE']).strip() != '': store_product_data.at[index, 'PRICE'] = round(float(str(row['PRICE']).replace('USD', '').strip()), 2)
            if str(row['SALE_PRICE']).strip() != '': store_product_data.at[index, 'SALE_PRICE'] = round(float(str(row['SALE_PRICE']).replace('USD', '').strip()), 2)
        else:
            # if category not provided
            store_product_data.drop(index, inplace=True)

        # reset dataframe index labelling
        store_product_data.reset_index(drop=True, inplace=True)


    # save sorted data
    store_product_data.to_csv(path_or_buf=f'sorted_products_data\{filename}', index=False)

    # delete file from old folder
    os.remove(path=f'{folder}\{filename}')