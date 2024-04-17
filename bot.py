import time 
import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame
df = pd.read_csv('DAAPL.csv')
dfx = df.head(1)  # Selecting the earliest row

def sidex(df):
    if df.iloc[-1]['Close'] >= df.iloc[-2]['Open']:
        return "Sell"
    elif df.iloc[-1]['Close'] <= df.iloc[-2]['Open']:
        return "Buy"

def signalx(df):
    if df.iloc[-1]['Close'] >= df.iloc[-2]['Open']:
        df['signal'] = 1
        return "Sell"
    elif df.iloc[-1]['Close'] <= df.iloc[-2]['Open']:
        df['signal'] = 2
        return "Buy"

def order(side, signal,df):
    print(f"{side}")
    print(f"{signal}")
    print(f"Close:{df.iloc[-1]['Close']} ::: Open:{df.iloc[-2]['Open']}")

def render(dfx):
    fig, ax = plt.subplots(figsize=(15, 8))  # Set the figsize parameter to adjust the size of the plot
    ax.plot(dfx.index, dfx['Close'], label='Close')
    ax.set_xlabel('Index')
    ax.set_ylabel('Close Price')
    ax.set_title('Real-time Plot')

    # Plot markers for buy and sell signals
    buy_signals = dfx[dfx['signal'] == 2]
    sell_signals = dfx[dfx['signal'] == 1]
    ax.scatter(buy_signals.index, buy_signals['Close'], color='green', marker='^', label='Buy Signal')
    ax.scatter(sell_signals.index, sell_signals['Close'], color='red', marker='v', label='Sell Signal')

    ax.legend()
    plt.show(block=False)  # Display the plot without blocking
    plt.pause(2)           # Pause for 2 seconds
    plt.close()
    time.sleep(2)           # Close the plot window

def kline(index):
    # Sample implementation of kline returning consecutive rows
    new_data = df.iloc[index]  # Get the row corresponding to the current index
    return pd.DataFrame([new_data])  # Convert the row to a DataFrame

for i in range(len(df)):
    new_df = kline(i)    
    dfx = pd.concat([dfx, new_df])
    side = sidex(dfx)
    signal = signalx(dfx)
    order(side, signal,df=dfx)
    render(dfx)

