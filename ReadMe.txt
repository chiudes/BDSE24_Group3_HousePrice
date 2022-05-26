There are data and codes for analyze house price of Taipei City and New Taipei City.

# original data
"0_taipei.csv" is the original data from website which is too big to push on github.
After using "purge_data.py", there will be a purged data called "1_taipei_purged.csv" which will be used for mechine learing.

# data for join
"pop.csv" is the population data of Taipei.
"AllFinancialCols.csv" is the financial data of Taiwan.
Both will be join for mechine learning.

# mechine learning code
"LinearRegression.ipynb" use LinearRegression for mechine learning. 
"xgb.ipynb" use xgboost for mechine learning.
"tp_xgb.ipynb" split "1_taipei_purged.csv" into Taipei City and New Taipei City then use xgboost for mechine learning.
"make_web.ipynb" make a csv file with our prediction called "web_with_pred.csv".
"check_diff.ipynb" make a csv file with 2021 real price and 2021 prediction for comparison.
