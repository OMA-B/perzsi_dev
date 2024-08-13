import pandas as pd, os


def remove_uncategorized_products(filename: str):
    # read csv file
    products_data = pd.read_csv(filepath_or_buffer=filename, encoding='ISO-8859-1')

    print(f'current file: {filename}')

    for index, row in products_data.iterrows():
        # check if level one category is empty, then delete row
        for num in [0,1,2,3,4,5,6,7,8,9]:
            if str(num) in str(row['UNIT_PRICING_MEASURE']): break
        else: products_data.drop(index, inplace=True)
    # reset index labelling
    products_data.reset_index(drop=True, inplace=True)

    return (products_data, filename)


def rearrange_level_two_and_three(dataframe_n_filename):
    dataframe = dataframe_n_filename[0]
    filename = dataframe_n_filename[1]
    # if there is level 3, replace level 1 with 2 and level 2 with 3
    dataframe['INSTALLMENT'] = dataframe['INSTALLMENT'].astype(object)
    for index, row in dataframe.iterrows():
        for num in [0,1,2,3,4,5,6,7,8,9]:
            if str(num) in str(row['INSTALLMENT']):
                dataframe.at[index, 'UNIT_PRICING_MEASURE'] = row['UNIT_PRICING_BASE_MEASURE']
                dataframe.at[index, 'UNIT_PRICING_BASE_MEASURE'] = row['INSTALLMENT']
                dataframe.at[index, 'INSTALLMENT'] = ''
                break

    # save cleaned data back to file
    dataframe.to_csv(path_or_buf=filename, index=False)


folder = 'sorted_products_data'
for filename in os.listdir(path=folder):
    rearrange_level_two_and_three(dataframe_n_filename=remove_uncategorized_products(filename=f'{folder}\{filename}'))