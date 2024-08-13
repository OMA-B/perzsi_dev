import pandas as pd, os, shutil, json


# open store info file
store_info = pd.read_csv(filepath_or_buffer='store_info.csv', encoding='ISO-8859-1')

# lists to store merged product upload and product category upload
product_upload = []
product_cat_upload = []
done_stores = []

id_value = 1080175
idacct = 1564274
auto_prod_id = 2205587

# open store files to extract needed data
folder = 'sorted_products_data'
for filename in os.listdir(path=folder):
    # filename = '1_800_FLORALS-1_800_FLORALS_Products-shopping.csv'
    print(f'current file: {filename}')
    store_product_data = pd.read_csv(filepath_or_buffer=f'{folder}\{filename}', encoding='ISO-8859-1')

    # loop through store info and check for current store, to fetch the relevant data
    for index, row in store_info.iterrows():
        if str(row['Filename']) in filename:
            store_id = row['ID']
            store_num = row['Store_Num']

            # loop through and get needed columns of data into list
            for index, row in store_product_data.iterrows():

                prod_id = f'Xuu524ab1dd{str(id_value).zfill(7)}'
                # for product upload
                product_upload.append({
                    'ID': prod_id,
                    'Title': row['TITLE'],
                    'Url': row['LINK'],
                    'click_count': 200,
                    'status': 'STAGING',
                    'created_at': '2024-04-20',
                    'update_at': '2024-04-20',
                    'active': 1,
                    'store_id': store_id,
                    'image_url': row['IMAGE_LINK'],
                    'currency_symbol': '$',
                    'count_ids': '',
                    'discount_price': row['SALE_PRICE'],
                    'main_price': row['PRICE'],
                    'description': str(row['DESCRIPTION'])[:250] if '<' not in str(row['DESCRIPTION']) or '>' not in str(row['DESCRIPTION']) or '脗' not in str(row['DESCRIPTION']) or '聮' not in str(row['DESCRIPTION']) or '脙' not in str(row['DESCRIPTION']) or '垄' not in str(row['DESCRIPTION']) or '聙' not in str(row['DESCRIPTION']) or '聶' not in str(row['DESCRIPTION']) else row['TITLE'],
                    'UPC': '',
                    'MPN': row['MPN'],
                    'GTIN': row['GTIN'],
                })
                # for product category upload
                product_cat_upload.append({
                    'idacct': idacct,
                    'ProdID': auto_prod_id,
                    'idstore': store_num,
                    'P_ProdID': prod_id,
                    'idctg_father': row['UNIT_PRICING_MEASURE'],
                    'idctg': row['UNIT_PRICING_BASE_MEASURE'],
                    'Platform': 'Perzsi_Upload',
                    'insertdate': '2024-04-20',
                })

                id_value += 1
                idacct += 1
                auto_prod_id += 1
            
            # move file to separate folder when done with
            shutil.move(src=f'{folder}\{filename}', dst=f'done\{filename}')
            done_stores.append({filename: f'{store_num} - {store_id}'})

product_upload_df = pd.DataFrame(data=product_upload)
product_cat_upload_df = pd.DataFrame(data=product_cat_upload)

product_upload_df.to_csv(path_or_buf='final_files\Product_Upload_1.csv', index=False)
product_cat_upload_df.to_csv(path_or_buf='final_files\Product_Category_Upload_1.csv', index=False)

with open(file='final_files\done_stores_1.json', mode='w') as file:
    json.dump(obj=done_stores, fp=file)