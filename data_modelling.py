import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from pandas import read_csv
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import datetime
from prophet import Prophet
from sklearn.metrics import mean_squared_error
import dateutil.parser # for handling the conversion of datetime formats
from datetime import timedelta # for operating the datetime objects
from statsmodels.tsa. statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse
from tqdm import tqdm
from os import system, name
import warnings
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

ERRORS = pd.DataFrame(columns = ["country", "AR", "sarimax", "fbprophet"])
nearestn=NearestNeighbors(n_neighbors=2)

warnings.filterwarnings('ignore')

url = 'assets/processed_data/output.csv'
df = pd.read_csv(url, parse_dates=True, infer_datetime_format=True)



# Add a attribute name to add it in the prediction/forecasting
columns = ['sucid_in_hundredk']


# This function will generate a dataframe out of a time series list



def outlier(final):

    outlier_threshold = 0.85

    for_DBSCAN = final.copy()

    #getting numerical columns
    num_df = for_DBSCAN._get_numeric_data()
    num_df = num_df.drop(["year"], axis = 1)
    X = StandardScaler().fit_transform(num_df)


    # outlier removal function
    print("nunber of records: ",len(X))
    temp = X.copy()
    nbrs=nearestn.fit(temp)
    distances,indices=nbrs.kneighbors(temp)
    distances=np.sort(distances,axis=0)
    distances=distances[:,1]

    db = DBSCAN(eps=outlier_threshold, min_samples=3)

    db.fit(temp)

    for_DBSCAN["clusters"]=db.labels_
    outliers_indexes=for_DBSCAN.loc[for_DBSCAN.clusters==-1].index
    outlier_df = for_DBSCAN.loc[for_DBSCAN.clusters==-1]
    print("Total ",len(outliers_indexes)," are outliers")

    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)

    for_DBSCAN=for_DBSCAN.drop(outliers_indexes,axis=0)
    for_DBSCAN=for_DBSCAN.drop("clusters",axis=1)

    print("Before removing outliers, total number of records: ", len(final))
    final=final.drop(outliers_indexes,axis=0)
    
    print("After removing outliers, total number of records: ", len(final))
    print("#"*40)

    return final, outlier_df

df, outlier_df = outlier(df)
df.index = df.year
df = df.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True, ignore_index=False, key=None)

outlier_df.to_csv('assets/processed_data/outliers.csv')

countries=df['country'].unique()

def time_to_df(list1, number_of_attributes = 3):
    df = pd.DataFrame(columns=range(number_of_attributes))
    
    for i in range(len(list1)-number_of_attributes+1):
        record = []
        for j in range(i,i+number_of_attributes):
            record.append(list1[j])
        df.loc[len(df.index)] = record
        
        
    return df


# This function trains the model using the input data(dataframe)
def train_and_forecast(list1, number_of_forecast = 5, npast_year =0, number_of_attributes = 3):

    input1 = time_to_df(list1, number_of_attributes)
    # We take last column of the features as target and rest are taken as attributes
    featureMat = input1.iloc[:, : len(input1.columns) - 1]
    label = input1[input1.columns[-1]]
    train_features, test_features, train_res, test_res= train_test_split(featureMat,label,test_size=0.4)
    
    # Here we are using linear regression model
    #model = linear_model.LinearRegression()
    model = linear_model.ElasticNet(alpha = 0.7)
    model.fit(train_features, train_res)
    test_result = model.predict(test_features)
    # Checking for the score
    error = sqrt((1/len(test_res)*np.sum(test_result - test_res))*
        np.sum(test_result - test_res))
    error = int(100*error)/100
    forecasted_values = []
    if(npast_year != 0):
        list_for_forcasting = list1[:-npast_year]
    else:
        list_for_forcasting = list1
    for i in range(number_of_forecast+npast_year):
        
        features_for_forecast = list_for_forcasting[-number_of_attributes+1:]
        forecasted_value = model.predict([features_for_forecast])[0]
        forecasted_values.append(forecasted_value)
        list_for_forcasting.append(forecasted_value)
        
    return forecasted_values, error

    
def AR_forecast(series, nforecast_year = 10, npast_year =0, p = 3):

    number_of_forecast = nforecast_year
    
    # Generate predictions
    forecasts, error = train_and_forecast(series.to_list(), number_of_forecast, npast_year, p+1)
    forecasts_ser = pd.Series(forecasts, copy=False)
    to_plot=forecasted_series_to_df(series, forecasts_ser, npast_year, str(series.name), "Date")

    return to_plot, series, error

# function to check if the year is leap year or not
def is_leap_year(year):

    if (year%4) == 0:
        if (year%100) == 0:
            if (year%400) == 0:
                return True
            else:
                return False
        else:
             return True
    else:
        return False

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def forecasted_series_to_df(series, forecasted_series_, npast_year, name_of_forecasted_column, name_of_datetime_index_column):
  forecasted_series = forecasted_series_.copy()
  y = 0
  index_for_forcaste = []
  index_for_forcaste.append(series.index[-npast_year-1])
  for i in range(len(forecasted_series)-1):
    y = y+1
    date_temp = index_for_forcaste[-1]
    if(is_leap_year(date_temp.year)):
      date_temp = date_temp + timedelta(days = 366)
    else:
      date_temp = date_temp + timedelta(days = 365)
    index_for_forcaste.append(date_temp)

 
  forecasted_series.index = pd.to_datetime(index_for_forcaste)

  forecasted_series = pd.DataFrame({name_of_datetime_index_column:forecasted_series.index, name_of_forecasted_column:forecasted_series.values})
  forecasted_series.index = forecasted_series[name_of_datetime_index_column]
  forecasted_series = forecasted_series.drop(name_of_datetime_index_column, axis = 1)

  return forecasted_series



for i in tqdm (range (len(countries)), desc="Generating data files.."):
    country = countries[i]
    #print("Creating a time series for country ",country," with parameter ", columns)
    country_df = df[(df.country == country)]
    country_with_columns = pd.DataFrame(country_df, columns=columns)
    # adding all deaths together and group by year
    country_with_columns = country_with_columns.groupby(['year'])[columns].transform('sum')
    #country_with_columns = pd.Series.to_frame(country_with_columns)
    country_with_columns['year'] = list(country_with_columns.index)
    country_with_columns = country_with_columns.drop_duplicates()
    country_with_columns = country_with_columns.drop(labels='year', axis=1)

    country_with_columns.to_csv('assets/processed_data/country_wise/data/'+str(country)+'.csv')

print("All files are written in the directory.")
print("\n"*5)


# evaluate an SARIMA model for a given order (p,d,q)
def evaluate_sarima_model(X, sarima_order):

    # prepare training dataset
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]

    # make predictions
    predictions = list()

    for t in range(len(test)):
        model = SARIMAX(history, order=sarima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])

    # calculate out of sample error
    rmse = sqrt(mean_squared_error(test, predictions))

    return rmse

# evaluate combinations of p, d and q values for an SARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
    
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None

    for p in p_values:

        for d in d_values:

            for q in q_values:

                order = (p,d,q)
                try:
                    rmse = evaluate_sarima_model(dataset, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                    #print('SARIMA%s RMSE=%.3f' % (order,rmse))
                except:
                    continue

        #print('Best SARIMA%s RMSE=%.3f' % (best_cfg, best_score))

    #print('Best SARIMA%s RMSE=%.3f' % (best_cfg, best_score))
    return best_cfg, best_score, rmse


def forecast(country,npast_year = 0, nforecast_year = 5):

    series = read_csv('assets/processed_data/country_wise/data/'+str(country)+'.csv', header=0, index_col=0, parse_dates=True)
    first_time = True
    for parameter_to_forecast in series.columns:
        if parameter_to_forecast == 'year':
            pass
        else:
            # evaluate parameters
            p_values = [0, 1, 2, 4, 6]
            d_values = range(0, 3)
            q_values = range(0, 3)
            
            tdf = series[parameter_to_forecast].copy()
            tdf.index = series.index
            tdf = tdf.squeeze()
           
            # selecting best model using grid search
            best_cfg, best_score, error_sarimax = evaluate_models(tdf.values, p_values, d_values, q_values)
            # Instantiate the model
           
            model = SARIMAX(series[parameter_to_forecast], order=best_cfg)

            # Fit the model
            results = model.fit()

            # Generate predictions
            forecasts = results.get_prediction(start=len(series)-npast_year,end = len(series)+nforecast_year-1)
            forecasted_1, actual, error_AR = AR_forecast(series[parameter_to_forecast], 
                nforecast_year = nforecast_year,npast_year = npast_year, p = 5)
            forcasted_final = [actual.to_list()[-1]]
            forcasted_final.extend(forecasted_1[parameter_to_forecast].to_list())

            data_fbp = series.copy()
            data_fbp["year"] = data_fbp.index
            data_fbp.columns = ['y','ds']
            data_fbp['ds'] = pd.to_datetime(data_fbp['ds'])
            train = data_fbp.iloc[:len(data_fbp)-int(len(data_fbp)*0.25)]
            test = data_fbp.iloc[len(data_fbp)-int(len(data_fbp)*0.25)+1:]
            m = Prophet(interval_width = 0.80)
            m.fit(data_fbp)
            future = m.make_future_dataframe(periods=15, freq = "Y", include_history = "False") 
            forecast = m.predict(future)
            res = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            forcecast_fbf = [actual.to_list()[-1]]
            temp_ls = forecast['yhat'].to_list()[len(data_fbp):]
            
            forcecast_fbf.extend(temp_ls)
            forcecast_fbf = pd.Series(forcecast_fbf, copy=False)
            to_plot_fbf=forecasted_series_to_df(series[parameter_to_forecast], forcecast_fbf, npast_year, str(parameter_to_forecast), "year")

            # Model evaluation for prophet
            predictions = forecast.iloc[-len(test):]['yhat']
            #print("Root Mean Squared Error between actual and  predicted values: ",rmse(predictions,test['y']), "--> ",int(rmse(predictions,test['y'])*10000/test['y'].mean())/100," %")
            error_fbprophet = rmse(predictions,test['y'])
            mean_forecast_sarima = forecasts.predicted_mean

            forcasted_final_sarima = [actual.to_list()[-1]]
            forcasted_final_sarima.extend(mean_forecast_sarima.to_list())
            forcasted_final_sarima = pd.Series(forcasted_final_sarima, copy=False)
            
            print("Forecasting for country: ", country)

            to_plot=forecasted_series_to_df(series[parameter_to_forecast], forcasted_final_sarima, npast_year, str(parameter_to_forecast), "year")
            to_plot[parameter_to_forecast+"_sarimax"] = to_plot[parameter_to_forecast]
            to_plot[parameter_to_forecast+"_AR"] = forcasted_final
            to_plot=to_plot.drop([parameter_to_forecast], axis = 1)
            to_plot[parameter_to_forecast+"_fbprophet"] = to_plot_fbf[parameter_to_forecast]

            to_plot[parameter_to_forecast+"_sarimax"] = to_plot[parameter_to_forecast+"_sarimax"].apply(lambda x: int(x*100)/100)
            to_plot[parameter_to_forecast+"_AR"] = to_plot[parameter_to_forecast+"_AR"].apply(lambda x: int(x*100)/100)
            to_plot[parameter_to_forecast+"_fbprophet"] = to_plot[parameter_to_forecast+"_fbprophet"].apply(lambda x: int(x*100)/100)

            if first_time:
                first_time = False
                temp = to_plot.copy()
            else:
                temp=pd.merge(to_plot, temp, on = "year", how = 'right') 

            ERRORS.loc[len(ERRORS)] = [country, error_AR,error_sarimax, error_fbprophet]
                    


    # writting forecastes to the hard-disk
    temp.to_csv('assets/processed_data/country_wise/forecasted/'+str(country)+'.csv')

    return temp, series
clear()
for i in tqdm (range (len(countries)), desc="Generating forecasted data files.."):
    country = countries[i]
    to_plot, series = forecast(country = country, npast_year = 0, nforecast_year = 15)
    ERRORS.to_csv('assets/processed_data/error.csv')
    print("Error file written successfully.")
    clear()
clear()
print("Forecasted files are ready to serve the dash boarded.")
print("Error file written successfully.")