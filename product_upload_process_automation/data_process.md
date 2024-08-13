# Perzsi stores data preprocessing for DB Upload

1. unzip_to_csv_file -- extract the downloaded zipped files and convert them to csv files automatically
2. filter files -- to remove out of stock data
3. verify images -- to remove products without image display
4. extract_level_two -- to add new category levels to the products_cat_levels.csv file, so to be able to sort new added data
5. store info -- add image verified stores to store info file if not done already
6. sort product data -- to assign products their category levels
7. filter and rearrange products by levels -- to reorganize category levels of products if there are more than 2 categories
8. merge data -- to combine all sorted and rearranged products data, to be ready for DB upload. 