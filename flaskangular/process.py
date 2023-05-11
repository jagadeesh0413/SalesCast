import base64
import datetime
import io
import os
import pandas as pd
# for SARIMA
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

def preprocess_data(dataframe):
    # Handle missing values in the "Total" column
    dataframe['Total'] = dataframe['Total'].fillna(dataframe['Total'].mean())

     # Change index date format to DD-MM-YYYY
    dataframe.index = pd.to_datetime(dataframe.index, format='%d-%m-%Y')

    return dataframe
 

def buildModel():
    # Fit the seasonal ARIMA model
    model = sm.tsa.statespace.SARIMAX(df, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    res1 = model.fit()
    print('build - done')
    return res1


def predict(start, end):
    pred1 = res.predict(start=start, end=end)
    print('prediction - done')
    return pred1


def plotGraph(predicted):
    plt.clf()
    plt.plot(df['Total'], label='Actual', color='blue')
    plt.plot(predicted, label='Predicted', color='red') 
    # plt.plot(df['Total'], label='Actual')
    # plt.plot(predicted, label='Predicted') 
    plt.xlabel('Year')
    plt.ylabel('Sales')
    plt.title('Actual vs. Predicted Sales Data')
    plt.legend()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64


def main(periodicity, num, dataframe):
    global df, pred, res, initial, final
    # Reading the dataset
    df = dataframe
    print(df.head())

    res = buildModel()

    if(periodicity=='month'):
  

     initial = df.index[len(df) - 1]
     final = initial + pd.Timedelta(days=31 * int(num))
     pred = predict(initial, final)

    else:
     if(periodicity=='day'): 
      # resample to daily frequency
      df = df.resample('D').sum()
     if(periodicity=='week'):
       # resample to Weekly frequency
      df = df.resample('W').sum()

    initial = df.index[len(df)-1]  #last value in the dataset
    if(periodicity=='day'): final = initial + pd.Timedelta(days = int(num))
    if(periodicity=='week'): final = initial + pd.Timedelta(weeks = int(num))

    forecast_daily = res.predict(start=initial, end=final)
    pred = forecast_daily
    forecast_daily = pd.DataFrame(forecast_daily)






    path = "result/result.csv"
    res = pd.concat([df["Total"], pred])
    directory = os.path.dirname(path)

    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    res.to_csv(path,header=False)
    # Plotting the graph
    return plotGraph(pred), os.path.basename(path)


# returns the data points for the graph
def datapts():
    # values of x axis
    dates = res["Date"].values
    labels = []
    for x in dates:
        labels.append(str(x).split("T")[0])

    # Values of y -axis
    sales = pred.tolist()
    response = {
        "labels": labels,
        "sales": sales
    }
    return response


if __name__ == "__main__":
    main(1, num=36)


