from taipy.gui import Gui, Markdown, notify
from taipy import Config, Scope
import taipy as tp

import time

import datetime as dt

from pmdarima import auto_arima

from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np

from pandas.core.common import SettingWithCopyWarning
import warnings

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

path_to_data = "data/covid-19-all.csv"

Config.configure_job_executions(mode="standalone", nb_of_workers=2)

def add_features(data):
    dates = pd.to_datetime(data["Date"])
    data["Months"] = dates.dt.month
    data["Days"] = dates.dt.isocalendar().day
    data["Week"] = dates.dt.isocalendar().week
    data["Day of week"] = dates.dt.dayofweek
    return data

def create_train_data(final_data, date):
    bool_index = pd.to_datetime(final_data['Date']) <= date
    train_data = final_data[bool_index]
    return train_data

def preprocess(initial_data, country, date):
    data = initial_data.groupby(["Country/Region",'Date'])\
                       .sum()\
                       .dropna()\
                       .reset_index()

    final_data = data.loc[data['Country/Region']==country].reset_index(drop=True)
    final_data = final_data[['Date','Deaths']]
    final_data = add_features(final_data)
    
    train_data = create_train_data(final_data, date)
    return final_data, train_data


def train_arima(train_data):
    model = auto_arima(train_data['Deaths'],
                       start_p=1, start_q=1,
                       max_p=5, max_q=5,
                       start_P=0, seasonal=False,
                       d=1, D=1, trace=True,
                       error_action='ignore',  
                       suppress_warnings=True)
    model.fit(train_data['Deaths'])
    return model


def forecast(model):
    predictions = model.predict(n_periods=60)
    return predictions


def result(final_data, predictions, date):
    dates = pd.to_datetime([date + dt.timedelta(days=i)
                            for i in range(len(predictions))])
    final_data['Date'] = pd.to_datetime(final_data['Date'])
    predictions = pd.concat([pd.Series(dates, name="Date"),
                             pd.Series(predictions, name="Predictions")], axis=1)
    return final_data.merge(predictions, on="Date", how="outer")


initial_data_cfg = Config.configure_data_node(id="initial_data",
                                              storage_type="csv",
                                              path=path_to_data,
                                              cacheable=True,
                                              validity_period=dt.timedelta(days=5),
                                              scope=Scope.GLOBAL)

country_cfg = Config.configure_data_node(id="country", default_data="India",
                                         cacheable=True, validity_period=dt.timedelta(days=5))


date_cfg = Config.configure_data_node(id="date", default_data=dt.datetime(2020,10,10),
                                         cacheable=True, validity_period=dt.timedelta(days=5))

final_data_cfg =  Config.configure_data_node(id="final_data",
                                                  cacheable=True, validity_period=dt.timedelta(days=5))


train_data_cfg =  Config.configure_data_node(id="train_data", cacheable=True, validity_period=dt.timedelta(days=5))


task_preprocess_cfg = Config.configure_task(id="task_preprocess_data",
                                           function=preprocess,
                                           input=[initial_data_cfg, country_cfg, date_cfg],
                                           output=[final_data_cfg,train_data_cfg])

model_cfg = Config.configure_data_node(id="model", cacheable=True, validity_period=dt.timedelta(days=5), scope=Scope.PIPELINE)

task_train_cfg = Config.configure_task(id="task_train",
                                      function=train_arima,
                                      input=train_data_cfg,
                                      output=model_cfg)

predictions_cfg = Config.configure_data_node(id="predictions", scope=Scope.PIPELINE)

task_forecast_cfg = Config.configure_task(id="task_forecast",
                                      function=forecast,
                                      input=model_cfg,
                                      output=predictions_cfg)

result_cfg = Config.configure_data_node(id="result", scope=Scope.PIPELINE)

task_result_cfg = Config.configure_task(id="task_result",
                                      function=result,
                                      input=[final_data_cfg, predictions_cfg, date_cfg],
                                      output=result_cfg)

pipeline_preprocessing_cfg = Config.configure_pipeline(id="pipeline_preprocessing",
                                                       task_configs=[task_preprocess_cfg])

pipeline_arima_cfg = Config.configure_pipeline(id="ARIMA",
                                               task_configs=[task_train_cfg, task_forecast_cfg, task_result_cfg])

def train_linear_regression(train_data):    
    y = train_data['Deaths']
    X = train_data.drop(['Deaths','Date'], axis=1)
    
    model = LinearRegression()
    model.fit(X,y)
    return model

def forecast_linear_regression(model, date):
    dates = pd.to_datetime([date + dt.timedelta(days=i)
                            for i in range(60)])
    X = add_features(pd.DataFrame({"Date":dates}))
    X.drop('Date', axis=1, inplace=True)
    predictions = model.predict(X)
    return predictions


task_train_cfg = Config.configure_task(id="task_train",
                                      function=train_linear_regression,
                                      input=train_data_cfg,
                                      output=model_cfg)

task_forecast_cfg = Config.configure_task(id="task_forecast",
                                      function=forecast_linear_regression,
                                      input=[model_cfg, date_cfg],
                                      output=predictions_cfg)

pipeline_random_forest_cfg = Config.configure_pipeline(id="LinearRegression",
                                               task_configs=[task_train_cfg, task_forecast_cfg, task_result_cfg])

scenario_cfg = Config.configure_scenario(id='scenario', pipeline_configs=[pipeline_preprocessing_cfg,
                                                                          pipeline_arima_cfg,
                                                                          pipeline_random_forest_cfg])
if __name__=='__main__':
    scenario = tp.create_scenario(scenario_cfg, name='First Scenario')
    tp.submit(scenario)
    while not scenario.result.is_ready_for_reading:
        time.sleep(1)