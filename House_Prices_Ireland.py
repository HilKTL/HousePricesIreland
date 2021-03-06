import pickle
# load : get the data from file
data = pickle.load(open("C:\\Users\\serta\\Desktop\\Property_Price_Register_Ireland-28-05-2021.pkl", "rb"))
import pandas as pd
data = pd.DataFrame(data)
print(data.columns)
print(data.info)
print(data.dtypes)
print(data.drop_duplicates)
#Percentage of null values of columns
def null_data_percentage(data) :
    results = []
    features = list(data.columns)
    #print(features)
    for feature in features:
        percentage = len(data[data[feature].isnull()]) / len(data)
        result = print('percentage of null data in',feature,'column is', percentage)
        results.append(result)
    return results
null_data_percentage(data = data)
data.drop(columns='POSTAL_CODE',axis = 1,inplace = True)
data['PROPERTY_SIZE_DESC'].fillna('No information',inplace = True)
print(data['PROPERTY_SIZE_DESC'].head())
print(data["PROPERTY_DESC"].iloc[0:30])
data["PROPERTY_DESC"] = ['New' if x == 'New Dwelling house /Apartment' else 'Second_hand' for x in data["PROPERTY_DESC"]]
print(data["PROPERTY_DESC"])
#getting index of new properties
lst_index_new = data[data["PROPERTY_DESC"] == 'New'].index
print(data.iloc[lst_index_new,5])
#getting index of vat excluded properties
lst_index_vax = data[data["IF_VAT_EXCLUDED"] == 0].index
# defining a function for finding new properties whose prices are vax excluded
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
intersection_lst = intersection(lst_index_vax, lst_index_new)
print(data.iloc[intersection_lst,3])
#adding vat on sale prices of new properties
data.iloc[intersection_lst,3] = data.iloc[intersection_lst,3]*113.5/100
print(data.iloc[intersection_lst,3])
data.drop('IF_VAT_EXCLUDED',axis = 1,inplace = True)
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (12, 8),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
"""First 50 Dublin counties where houses were sold under 250000 euros in 2021"""
dublin_data = data[data["COUNTY"] == "Dublin"]
house_prices_under_250000 = dublin_data[dublin_data['SALE_PRICE'] < 250000.000].index
year_of_2021 = dublin_data[dublin_data['SALE_DATE'].dt.year > 2020].index
intersection_lst = intersection(house_prices_under_250000, year_of_2021)
address = data.iloc[intersection_lst,1].str.split(',')
print(address.iloc[3][1:3])
address = [x[1:3] for x in address]
print(address.sort)
print(address)
address_data = pd.DataFrame(address)
address_data.columns = ['Town','County']
address_data['Town'].value_counts()[0:50].plot(kind = 'bar')
plt.title('Houses sold in Dublin under 250000 euros')
"""2021 Average House Prices of Each Counties"""
data.head()
sales_of_2021 = data[data['SALE_DATE'].dt.year == 2021]
sales_of_2021.drop(columns ='IF_MARKET_PRICE',axis = 1,inplace = True)
sales_of_2021.groupby('COUNTY').describe()
avg_2021 = sales_of_2021.groupby('COUNTY').mean().sort_values(by = 'SALE_PRICE')
import numpy as np
avg_2021.plot(kind = 'barh',xticks = np.arange(100000,600000,50000))
plt.title('2021 Average sale prices of counties')
print(data['SALE_DATE'].nsmallest(1),data['SALE_DATE'].nlargest(1))
"""Increase rate in house prices between 2010 and 2021 among cities in Ireland"""
sales_of_2010 = data[data['SALE_DATE'].dt.year == 2010]
sales_of_2010.drop(columns ='IF_MARKET_PRICE',axis = 1,inplace = True)
sales_of_2010.head()
avg_2010 = sales_of_2010.groupby('COUNTY').mean().sort_values(by = 'SALE_PRICE')
price_change_ratio_of_counties = (avg_2021-avg_2010)/avg_2010*100
price_change_ratio_of_counties.columns = ['Price_change_ratio_from_2010_to_2021']
price_change_ratio_of_counties = price_change_ratio_of_counties.sort_values(by ='Price_change_ratio_from_2010_to_2021' )
price_change_ratio_of_counties.plot(kind = 'bar',yticks = np.arange(-5,65,5))
plt.title('Average price change ratio of properties from 2010 to 2021')

"""PRICE CHANGES FROM YEAR TO YEAR FOR EACH COUNTRY"""
data['SALE_DATE'] = data['SALE_DATE'].dt.year
def price_changes(df,county):
    dfs = df[df['COUNTY'] == county]
    sale_price = dfs.groupby('SALE_DATE').mean()
    sale_price = sale_price['SALE_PRICE']
    print(sale_price)
    title = 'Avg. Property Price changes of',county.upper(),'between 2010 t0 2021'
    sale_price.plot(kind = 'line',figsize = (5,5) ,xticks = np.arange(2010,2022,1))
    plt.xticks(rotation = 50)
    plt.title(title)
    plt.show()
county_list = data['COUNTY'].unique()
print(county_list)
for county in county_list:
    fig, ax = plt.subplots()
    price_changes(df = data,county = county)

"""Average and maximum price and number of houses sold in different neighborhoods of a county in 2021"""
data['ADDRESS'] = [x.split(',')  for x in data['ADDRESS']]
data['Town'] = [x[1].upper().strip() for x in data['ADDRESS']]
print(data['Town'])
data['STREET'] = [x[0].upper().strip() for x in data['ADDRESS']]
print(data['STREET'])
#defining a function for getting avg.,max price and number of house sold in 2021
def median_price_address_county(df,county,address):
    data = df[(df['COUNTY'] == county) & (df['SALE_DATE'] == 2021)]
    data_median = round(data.groupby(by = 'Town')['SALE_PRICE'].median())
    data_max = data.groupby(by = 'Town')['SALE_PRICE'].max()
    data_count = data.groupby(by = 'Town')['SALE_PRICE'].count()
    x = print('Average Price is : ',data_median[address],'\nMax Price is :',data_max[address],'\nNumber of house sold is : ',data_count[address])
    return x

"""Average and maximum price and number of houses sold in Ballinagh neighborhoud in Cavan"""
median_price_address_county(df = data,county = 'Cavan',address = 'BALLINAGH')

"""Average and maximum price and number of houses sold in Portlaoise neighborhoud in Laois"""
median_price_address_county(df = data,county = 'Laois',address = 'PORTLAOISE')

"""Average and maximum price and number of houses sold in Ballsbridge neighborhoud in Dublin"""
median_price_address_county(df = data,county = 'Dublin',address = 'BALLSBRIDGE')




