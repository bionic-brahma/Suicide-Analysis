import statsmodels.api as sm
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import plotly.express as px

df_cont = pd.read_csv("assets/data/countryContinent.csv", encoding="ISO-8859-1")
url = 'assets/data/suicide_moredata.csv'
url2 = 'assets/data/suicide_master.csv'
first_data = pd.read_csv(url2)
second_data = pd.read_csv(url)

first_data.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population','suicidesper100k', 'country-year', 'yearlyHDI',
    'GDPpyear', 'GDPpcapita', 'generation']
second_data.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population','suicidesper100k', 'country-year', 'yearlyHDI',
    'GDPpyear', 'GDPpcapita', 'generation', 'suicide%', 'Internetusers', 'Expenses', 'employeecompensation','Unemployment', 'Physiciansp1000', 'Legalrights', 'Laborforcetotal','Lifeexpectancy', 'Mobilesubscriptionsp100','Refugees', 'Selfemployed', 'electricityacess', 'secondarycompletion']

second_data.rename( {'GDPpyear':'yearly_gdp' } , axis=1 , inplace = True)
second_data.rename( {'GDPpcapita':'gdp_per_capita' } , axis=1 , inplace = True)
second_data.rename( {'yearlyHDI':'yearly_hdi' } , axis=1 , inplace = True)
second_data.rename( {'suicidesper100k':'sucid_in_hundredk' } , axis=1 , inplace = True)
second_data.rename( {'suicides_no':'suicides' } , axis=1 , inplace = True)

second_data.columns = map(str.lower, second_data.columns)
# remove special character
second_data.columns = second_data.columns.str.replace(' ', '')

first_data.rename( {'GDPpyear':'yearly_gdp' } , axis=1 , inplace = True)
first_data.rename( {'GDPpcapita':'gdp_per_capita' } , axis=1 , inplace = True)
first_data.rename( {'yearlyHDI':'yearly_hdi' } , axis=1 , inplace = True)
first_data.rename( {'suicidesper100k':'sucid_in_hundredk' } , axis=1 , inplace = True)
first_data.rename( {'suicides_no':'suicides' } , axis=1 , inplace = True)

first_data.columns = map(str.lower, first_data.columns)
# remove special character
first_data.columns = first_data.columns.str.replace(' ', '')


second_data = pd.merge(second_data, first_data, on =['country', 'year', 'sex', 'age', 'suicides', 'population',
       'sucid_in_hundredk', 'country-year', 'yearly_hdi', 'yearly_gdp',
      'gdp_per_capita', 'generation'] , how = 'left')

second_data = second_data.merge(df_cont[['country', 'continent', 'code_3']])

second_data.rename( {'code_3':'country_code' } , axis=1 , inplace = True)
second_data.rename( {'physiciansp1000':'physician_price' } , axis=1 , inplace = True)
second_data.rename( {'mobilesubscriptionsp100':'mobilesubscriptions' } , axis=1 , inplace = True)
countries_2 = second_data['country'].unique()

#good sample of the different regions.

countrynames = ['Argentina','Armenia','Australia',    'Austria',
    'Belgium',    'Brazil',    'Bulgaria',    'Canada',    'Chile',    'Colombia',    'Croatia',    'Cuba',    'Czech Republic',    'Denmark',
    'Finland',    'France',    'Germany',    'Greece',    'Hungary',    'Iceland',   'Ireland', 'Israel','Italy','Japan','Mexico', 'Netherlands','New Zealand','Norway','Poland', 'Portugal','Romania','Russian Federation','South Africa', 'Spain','Sweden', 'Switzerland','Thailand', 'Turkmenistan','Ukraine','United Kingdom', 'United States']

# countrynames

df1 = second_data.copy()
final = df1.iloc[np.where(df1.country == countrynames[0])]
for i, x in enumerate(countrynames[1:]):
    final = final.append(df1.iloc[np.where(df1.country == x)])
    
final = final[final.year >= 1985]
final = final[final.year <= 2016]

final['country'] = final['country'].astype('category')
final['continent'] = final['continent'].astype('category')
final['sex'] = final['sex'].astype('category')
final['generation'] = final['generation'].astype('category')
final['age'] = final['age'].astype('category')

final.drop('yearly_hdi', axis=1, inplace=True)
final.drop('secondarycompletion', axis=1, inplace=True)
final.drop('legalrights', axis=1, inplace=True)

final.internetusers=final.internetusers.fillna(final.internetusers	. min())
final.employeecompensation=final.employeecompensation.fillna(final.employeecompensation.mean())
final.electricityacess=final.electricityacess.fillna(final.electricityacess.mean())
final.refugees=final.refugees.fillna(final.refugees.mean())
final.expenses=final.expenses.fillna(final.expenses.mean())
final.physician_price=final.physician_price.fillna(final.physician_price.mean())

final['internetusers'] = final['internetusers'].replace(r'^\s*$', np.nan, regex=True)
final['unemployment'] = final['unemployment'].replace(r'^\s*$', np.nan, regex=True)
final['physician_price'] = final['physician_price'].replace(r'^\s*$', np.nan, regex=True)
final['internetusers'] = final['internetusers'].replace(r'^\s*$', np.nan, regex=True)
final['laborforcetotal'] = final['laborforcetotal'].replace(r'^\s*$', np.nan, regex=True)
final['selfemployed'] = final['selfemployed'].replace(r'^\s*$', np.nan, regex=True)
final['electricityacess'] = final['electricityacess'].replace(r'^\s*$', np.nan, regex=True)
final['lifeexpectancy'] = final['lifeexpectancy'].replace(r'^\s*$', np.nan, regex=True)
final['mobilesubscription'] = final['mobilesubscriptions'].replace(r'^\s*$', np.nan, regex=True)
final['refugees'] = final['refugees'].replace(r'^\s*$', np.nan, regex=True)
final['expenses'] = final['expenses'].replace(r'^\s*$', np.nan, regex=True)
final['employeecompensation'] = final['employeecompensation'].replace(r'^\s*$', np.nan, regex=True)
final['physician_price'] = final['physician_price'].replace(r'^\s*$', np.nan, regex=True)


final.loc[ final['internetusers'] == 0 | np.isnan(final['internetusers']), 'internetusers' ] = final['internetusers'].mean()
final.loc[ final['unemployment'] == 0 | np.isnan(final['unemployment']), 'unemployment' ] = final['unemployment'].mean()
final.loc[ final['physician_price'] == 0 | np.isnan(final['physician_price']), 'physician_price' ] = final['physician_price'].min()
final.loc[ final['laborforcetotal'] == 0 | np.isnan(final['laborforcetotal']), 'laborforcetotal' ] = final['laborforcetotal'].mean()
final.loc[ final['selfemployed'] == 0 | np.isnan(final['selfemployed']), 'selfemployed' ] = final['selfemployed'].mean()
final.loc[ final['electricityacess'] == 0 | np.isnan(final['electricityacess']), 'electricityacess' ] = final['electricityacess'].mean()
final.loc[ final['lifeexpectancy'] == 0 | np.isnan(final['lifeexpectancy']), 'lifeexpectancy' ] = final['lifeexpectancy'].mean()
final.loc[ final['mobilesubscriptions'] == 0 | np.isnan(final['mobilesubscriptions']), 'mobilesubscriptions' ] = final['mobilesubscriptions'].mean()
final.loc[ final['refugees'] == 0 | np.isnan(final['refugees']), 'refugees' ] = final['refugees'].mean()
final.loc[ final['expenses'] == 0 | np.isnan(final['expenses']), 'expenses' ] = final['expenses'].mean()
final.loc[ final['employeecompensation'] == 0 | np.isnan(final['employeecompensation']), 'employeecompensation' ] = final['employeecompensation'].mean()
final.loc[ final['physician_price'] == 0 | np.isnan(final['physician_price']), 'physician_price' ] = final['physician_price'].mean()

final.loc[:, 'expenses':'refugees'] = final.loc[:, 'expenses':'refugees'].fillna(final['employeecompensation'].mean()) 



final.to_csv('assets/processed_data/output.csv',mode = 'w', index=False)
print("File saved successfully!!!")
# outputting data to run models in live server
