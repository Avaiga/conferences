import datetime as dt
import pandas as pd


def clean_data(initial_dataset: pd.DataFrame):
    print("     Cleaning data")
    initial_dataset['Date'] = pd.to_datetime(initial_dataset['Date'])
    cleaned_dataset = initial_dataset
    return cleaned_dataset


def predict(cleaned_dataset: pd.DataFrame, day: dt.datetime):
    print("     Predicting")
    train_dataset = cleaned_dataset[cleaned_dataset['Date'] < day]
    predictions = train_dataset['Value'][-30:].reset_index(drop=True)
    return predictions


def evaluate(predictions, cleaned_dataset, day):
    print("     Evaluating")
    expected = cleaned_dataset.loc[cleaned_dataset['Date'] >= day, 'Value'][:30].reset_index(drop=True)
    mae = ((predictions - expected) ** 2).mean()
    return mae
