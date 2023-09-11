import base64
import io
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
 # Fit SARIMA model
def buildModel():
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
    plt.plot(df['Total'], label='Actual')
    plt.plot(predicted, label='Predicted')
    plt.xlabel('Year')
    plt.ylabel('Sales')
    plt.title('Actual vs. Predicted Sales Data')
    plt.legend()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return  image_base64


def main(periodicity, num, dataframe):
    global df, pred, res, initial, final
    
    # Reading the dataset
    df = dataframe
    print(df.head())

    res = buildModel()
    initial = df.index[len(df) - 1]
    final = initial + pd.Timedelta(days=31 * int(num))
    pred = predict(initial, final)

    # Plotting the graph
    return plotGraph(pred)


# returning the data points for the graph
def datapts():

    # values of x axis
    dates = pred.index.values
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
    data = pd.read_csv("dataset.csv", index_col='Date', parse_dates=True)
    print(main(1, num=36, dataframe=data))

