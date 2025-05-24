import pandas as pd



def process_excel_file_for_analysis(filename, sheet_1_name, sheet_2_name):
    # read in the excel file
    company_sheet = pd.read_excel(io=filename, sheet_name=sheet_2_name)
    platform_sheet = pd.read_excel(io=filename, sheet_name=sheet_1_name)

    # results lists
    matching_orders_transactions = []
    amz_missing_orders = []
    platform_missing_orders = []

    # go over the company records and look for a match in the platform records
    for c_index, c_record in company_sheet.iloc[1:, :].iterrows():
        if c_record['Sales Record'] in platform_sheet['Order ID'].values and c_record['Sale Price'] != 0:
            row_in_platform = platform_sheet.loc[platform_sheet['Order ID'] == c_record['Sales Record']]
            matching_orders_transactions.append({
                'Amz Order Number': c_record['Sales Record'],
                'Amz Date': c_record['Date'],
                'Amz Sale Price': c_record['Sale Price'],
                'Amz Cost': c_record['Cost'],
                'Amz Selling Fee': c_record['Selling Fee'],
                'Amz Profit': c_record['Profit'],
                'Platform Date': row_in_platform['Date'].values[0],
                'Platform Transaction type': row_in_platform['Transaction type'].values[0],
                'Platform Order ID': row_in_platform['Order ID'].values[0],
                'Total product charges': row_in_platform['Total product charges'].values[0],
                'Total promotional rebates': row_in_platform['Total promotional rebates'].values[0],
                'Amazon fees': row_in_platform['Amazon fees'].values[0],
                'Total (USD)': row_in_platform['Total (USD)'].values[0],
            })
        else: # and if there's no match or the sale price is not 0
            amz_missing_orders.append({
                'Amz Order Number': c_record['Sales Record'],
                'Amz Date': c_record['Date'],
                'Amz Sale Price': c_record['Sale Price'],
                'Amz Cost': c_record['Cost'],
                'Amz Selling Fee': c_record['Selling Fee'],
                'Amz Profit': c_record['Profit'],
                'Platform Date': '',
                'Platform Transaction type': '',
                'Platform Order ID': '',
                'Total product charges': '',
                'Total promotional rebates': '',
                'Amazon fees': '',
                'Total (USD)': '',
            })

    # go over platform records and check for which ain't in company records
    for p_index, p_record in platform_sheet.iterrows():
        if p_record['Order ID'] not in company_sheet['Sales Record'].values:
            platform_missing_orders.append({
                'Amz Order Number': '',
                'Amz Date': '',
                'Amz Sale Price': '',
                'Amz Cost': '',
                'Amz Selling Fee': '',
                'Amz Profit': '',
                'Platform Date': p_record['Date'],
                'Platform Transaction type': p_record['Transaction type'],
                'Platform Order ID': p_record['Order ID'],
                'Total product charges': p_record['Total product charges'],
                'Total promotional rebates': p_record['Total promotional rebates'],
                'Amazon fees': p_record['Amazon fees'],
                'Total (USD)': p_record['Total (USD)'],
            })


    # create dataframes
    matching_orders_transactions_df = pd.DataFrame(data=matching_orders_transactions)
    amz_missing_orders_df = pd.DataFrame(data=amz_missing_orders)
    platform_missing_orders_df = pd.DataFrame(data=platform_missing_orders)

    # create final results excel file
    with pd.ExcelWriter(path=f'output/analyzed_excel_result.xlsx') as writer:
        platform_sheet.to_excel(excel_writer=writer, sheet_name=sheet_1_name, index=False)
        company_sheet.to_excel(excel_writer=writer, sheet_name=sheet_2_name, index=False)
        matching_orders_transactions_df.to_excel(excel_writer=writer, sheet_name='Matching_Orders_Transactions', index=False)
        amz_missing_orders_df.to_excel(excel_writer=writer, sheet_name='AMZ_Missing_Orders', index=False)
        platform_missing_orders_df.to_excel(excel_writer=writer, sheet_name='Platform_Missing_Orders', index=False)

    
    return 'completed'





process_excel_file_for_analysis('Balance Sheet.xlsx', 'Transactions for time period 4_', 'AMZ Transaction')