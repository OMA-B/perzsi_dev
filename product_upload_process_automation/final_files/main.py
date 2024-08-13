import mysql.connector, os, pprint, json
from dotenv import load_dotenv
from process_csv import sort_data_from_csv

load_dotenv()


perzsi_cred = {
    'username': 'p_migration',
    'password': os.getenv('PASSWORD'),
    'host': 'db-mysql-nyc1-22348-do-user-10649077-0.b.db.ondigitalocean.com',
    'port' : 25060,
    'database': 'authserver'
}

perzsi_db = mysql.connector.connect(**perzsi_cred)


cursor = perzsi_db.cursor()


def show_tables_in_db():
    cursor.execute('SHOW TABLES')

    for table in cursor:
        print(table)

    cursor.close()
    perzsi_db.close()

# show_tables_in_db()

def query_all_from_db(table):
    # cursor.execute(f'DESCRIBE {table};')
    cursor.execute(f'SELECT * FROM {table}')
    # cursor.execute(f"SELECT * FROM {table} WHERE idacct = 484101;")

    # print(cursor.fetchone())
    for row in cursor.fetchall():
        pprint.pprint(row)

    cursor.close()
    perzsi_db.close()

# query_all_from_db(table='api_product')
# query_all_from_db(table='tbsptwoo')

def alter_table(table):
    # cursor.execute(f'ALTER TABLE {table} MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY')
    # cursor.execute(f'ALTER TABLE {table} MODIFY COLUMN id INT AUTO_INCREMENT, ADD PRIMARY KEY (id)')
    cursor.execute(f'ALTER TABLE {table} DROP PRIMARY KEY, MODIFY COLUMN id INT AUTO_INCREMENT, ADD PRIMARY KEY (id)')
    # cursor.execute(f'ALTER TABLE {table} MODIFY COLUMN id INT NULL')

    perzsi_db.commit()

    print('done!')

    cursor.close()
    perzsi_db.close()

# alter_table(table='api_product')

def delete_record_from_table(table):
    # delete all records from table
    # query = f'DELETE FROM {table}'
    # cursor.execute(query)

    # delete specific record from table
    # query = f'DELETE FROM {table} WHERE store_id = %s'
    # store_id = ('6ea9ab1baa0efb9e19094440c317e21b',)
    # cursor.execute(query, store_id)

    # query = f'DELETE FROM {table} WHERE idstore = %s'
    # idstore = ('29',)
    # cursor.execute(query, idstore)

    # delete specific records from table
    with open(file='done_stores_1.json', mode='r') as j_file:
        done_stores = json.load(fp=j_file)

    done_stores_list = []
    for store_list in [list(store.keys()) for store in done_stores]:
        done_stores_list.extend(store_list)

    store_ids = [done_store[done_stores_list[index]].split(' - ')[1] for index, done_store in enumerate(done_stores)]
    store_ids = tuple([done_store[done_stores_list[index]].split(' - ')[1] for index, done_store in enumerate(done_stores) if done_store[done_stores_list[index]].split(' - ')[1] not in store_ids[:index]])
    idstores = [done_store[done_stores_list[index]].split(' - ')[0] for index, done_store in enumerate(done_stores)]
    idstores = tuple([done_store[done_stores_list[index]].split(' - ')[0] for index, done_store in enumerate(done_stores) if done_store[done_stores_list[index]].split(' - ')[0] not in idstores[:index]])
    # print(store_ids)
    # print(idstores)
    # placeholders = ', '.join(['%s'] * len(store_ids))
    # query = f'DELETE FROM {table} WHERE store_id IN ({placeholders})'
    # cursor.execute(query, store_ids)

    placeholders = ', '.join(['%s'] * len(idstores))
    query = f'DELETE FROM {table} WHERE idstore IN ({placeholders})'
    cursor.execute(query, idstores)

    perzsi_db.commit()

    print(cursor.rowcount, f'records successfully deleted from {table}')

    cursor.close()
    perzsi_db.close()


# delete_record_from_table(table='api_product')
# delete_record_from_table(table='tbsptwoo')


def insert_data_into_db(table, upload_csv):

    if table == 'api_product':
        insert_query = f'INSERT INTO {table} (id, title, url, click_count, status, created_at, update_at, active, store_id, image_url, currency_symbol, count_ids, discount_price, main_price, description, UPC, MPN, GTIN) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    elif table == 'tbsptwoo':
        insert_query = f'INSERT INTO {table} (idacct, ProdID, idstore, P_ProdID, idctg_father, idctg, Platform, insertdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    
    elif table == 'api_banners':
        insert_query = f'INSERT INTO {table} (banner_type, image, active, animated, url, created_at, update_at, text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

    elif table == 'api_ads':
        insert_query = f'INSERT INTO {table} (adtype, adtypename, campaign_id, campgn_type, campgn_typename, adname, adtitle, addesc, adlandingurl, aditemurl, cat_idctgfatherid, cat_fathername, adbgttype, adbgtname, ad_bgtamt, bidtype, bidname, bidamount, ad_startdate, ad_enddate, ad_status, ad_apprstatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    elif table == 'api_product_review':
        insert_query = f'INSERT INTO {table} (reviewId, P_ProdId, iduse, rating, created_at, updated_at, review_title, review_body, helpful_count, review_images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    values = sort_data_from_csv(table=table, upload_csv=upload_csv)

    cursor.executemany(insert_query, values)

    perzsi_db.commit()

    print(cursor.rowcount, f'records successfully inserted to {table}!')

    cursor.close()
    perzsi_db.close()


# insert_data_into_db(table='api_product', upload_csv='Product_Upload_1.csv')
insert_data_into_db(table='tbsptwoo', upload_csv='Product_Category_Upload_1.csv')

# insert_data_into_db(table='api_banners', upload_csv='banners_data.csv')

# insert_data_into_db(table='api_ads', upload_csv='img_n_prod_ads_francis_test.csv')

# insert_data_into_db(table='api_product_review', upload_csv='new_review_upload.csv')




# def update_value_in_a_column(table, column, old_value, new_value):
#     cursor.execute(f"UPDATE {table} SET {column} = '{new_value}' WHERE {column} = {old_value};")

#     print('Updated!')

#     cursor.close()
#     perzsi_db.close()

# update_value_in_a_column(table='api_product', column='status', old_value='Penguinchillers', new_value='STAGING')