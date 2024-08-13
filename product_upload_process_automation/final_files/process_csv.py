import pandas as pd, pprint


def sort_data_from_csv(table, upload_csv):

    if table == 'api_product':
        perzsi_data_df = pd.read_csv(f'{upload_csv}')

        data = {
            'id':  perzsi_data_df['ID'].to_list()[870000:],
            'title': perzsi_data_df['Title'].to_list()[870000:],
            'url': perzsi_data_df['Url'].to_list()[870000:],
            'click_count': perzsi_data_df['click_count'].to_list()[870000:],
            'status': perzsi_data_df['status'].to_list()[870000:],
            'created_at': perzsi_data_df['created_at'].to_list()[870000:],
            'update_at': perzsi_data_df['update_at'].to_list()[870000:],
            'active': perzsi_data_df['active'].to_list()[870000:],
            'store_id': perzsi_data_df['store_id'].to_list()[870000:],
            'image_url': perzsi_data_df['image_url'].to_list()[870000:],
            'currency_symbol': perzsi_data_df['currency_symbol'].to_list()[870000:],
            'count_ids': perzsi_data_df['count_ids'].to_list()[870000:],
            'discount_price': perzsi_data_df['discount_price'].to_list()[870000:],
            'main_price': perzsi_data_df['main_price'].to_list()[870000:],
            'description': perzsi_data_df['description'].to_list()[870000:],
            'UPC': perzsi_data_df['UPC'].to_list()[870000:],
            'MPN': perzsi_data_df['MPN'].to_list()[870000:],
            'GTIN': perzsi_data_df['GTIN'].to_list()[870000:],
        }
    elif table == 'tbsptwoo':
        perzsi_data_df = pd.read_csv(f'{upload_csv}')

        data = {
            'idacct':  perzsi_data_df['idacct'].to_list()[800000:],
            'ProdID': perzsi_data_df['ProdID'].to_list()[800000:],
            'idstore': perzsi_data_df['idstore'].to_list()[800000:],
            'P_ProdID': perzsi_data_df['P_ProdID'].to_list()[800000:],
            'idctg_father': perzsi_data_df['idctg_father'].to_list()[800000:],
            'idctg': perzsi_data_df['idctg'].to_list()[800000:],
            'Platform': perzsi_data_df['Platform'].to_list()[800000:],
            'insertdate': perzsi_data_df['insertdate'].to_list()[800000:],
        }
    elif table == 'api_banners':
        perzsi_data_df = pd.read_csv(f'{upload_csv}')

        data = {
            'banner_type':  perzsi_data_df['banner_type'].to_list(),
            'image': perzsi_data_df['image'].to_list(),
            'active': perzsi_data_df['active'].to_list(),
            'animated': perzsi_data_df['animated'].to_list(),
            'url': perzsi_data_df['url'].to_list(),
            'created_at': perzsi_data_df['created_at'].to_list(),
            'updated_at': perzsi_data_df['updated_at'].to_list(),
            'text': perzsi_data_df['text'].to_list(),
        }
    elif table == 'api_ads':
        perzsi_data_df = pd.read_csv(f'{upload_csv}')

        data = {
            # 'id': perzsi_data_df['id'].to_list(),
            # 'adid': perzsi_data_df['adid'].to_list(),
            'adtype': perzsi_data_df['adtype'].to_list(),
            'adtypename': perzsi_data_df['adtypename'].to_list(),
            'campaign_id': perzsi_data_df['campaign_id'].to_list(),
            'campgn_type': perzsi_data_df['campgn_type'].to_list(),
            'campgn_typename': perzsi_data_df['campgn_typename'].to_list(),
            'adname': perzsi_data_df['adname'].to_list(),
            'adtitle': perzsi_data_df['adtitle'].to_list(),
            'addesc': perzsi_data_df['addesc'].to_list(),
            'adlandingurl': perzsi_data_df['adlandingurl'].to_list(),
            'aditemurl': perzsi_data_df['aditemurl'].to_list(),
            'cat_idctgfatherid': perzsi_data_df['cat_idctgfatherid'].to_list(),
            'cat_fathername': perzsi_data_df['cat_fathername'].to_list(),
            'adbgttype': perzsi_data_df['adbgttype'].to_list(),
            'adbgtname': perzsi_data_df['adbgtname'].to_list(),
            'ad_bgtamt': perzsi_data_df['ad_bgtamt'].to_list(),
            'bidtype': perzsi_data_df['bidtype'].to_list(),
            'bidname': perzsi_data_df['bidname'].to_list(),
            'bidamount': perzsi_data_df['bidamount'].to_list(),
            'ad_startdate': perzsi_data_df['ad_startdate'].to_list(),
            'ad_enddate': perzsi_data_df['ad_enddate'].to_list(),
            'ad_status': perzsi_data_df['ad_status'].to_list(),
            'ad_apprstatus': perzsi_data_df['ad_apprstatus'].to_list(),
        }
    elif table == 'api_product_review':
        perzsi_data_df = pd.read_csv(f'{upload_csv}')

        data = {
            'reviewId': perzsi_data_df['reviewId'].to_list(),
            'P_ProdId': perzsi_data_df['P_ProdId'].to_list(),
            'iduse': perzsi_data_df['iduse'].to_list(),
            'rating': perzsi_data_df['rating'].to_list(),
            'created_at': perzsi_data_df['created_at'].to_list(),
            'updated_at': perzsi_data_df['updated_at'].to_list(),
            'review_title': perzsi_data_df['review_title'].to_list(),
            'review_body': perzsi_data_df['review_body'].to_list(),
            'helpful_count': perzsi_data_df['helpful_count'].to_list(),
            'review_images': perzsi_data_df['review_images'].to_list(),
        }

    data_df = pd.DataFrame(data)

    data_df.fillna(value='[]', inplace=True) if table == 'api_product_review' else data_df.fillna(value=0.0, inplace=True)

    insert_row_values = [tuple(row) for row in data_df.itertuples(index=False)]

    return insert_row_values

    # print(data_df)


def convert_excel_to_csv():
    excel_file = pd.read_excel('new_review_upload.xlsx')

    excel_file.to_csv('new_review_upload.csv')




if __name__ == '__main__':
    # sort_data_from_csv(table='api_product')
    convert_excel_to_csv()