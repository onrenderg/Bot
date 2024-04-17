# import pandas as pd
# import matplotlib.pyplot as plt
# import time
# from flask import Flask, jsonify, render_template, session

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# # Sample DataFrame
# df = pd.read_csv('RHEL.csv')
# dfx = df.head(1)  # Selecting the earliest row
# current_index = 0

# def sidex(df):
#     if df.iloc[-1]['Close'] >= df.iloc[-2]['Open']:
#         return "Sell"
#     elif df.iloc[-1]['Close'] <= df.iloc[-2]['Open']:
#         return "Buy"

# def signalx(df):
#     if df.iloc[-1]['Close'] >= df.iloc[-2]['Open']:
#         df['signal'] = 1
#         return "Sell"
#     elif df.iloc[-1]['Close'] <= df.iloc[-2]['Open']:
#         df['signal'] = 2
#         return "Buy"

# def order(side, signal, df):
#     print(f"{side}")
#     print(f"{signal}")
#     print(f"Close:{df.iloc[-1]['Close']} ::: Open:{df.iloc[-2]['Open']}")



# def kline(index):
#     if index < len(df):
#         new_data = df.iloc[index]
#         return pd.DataFrame([new_data])
#     else:
#         return None


# @app.route('/stream')
# def update_klines():
#     global current_index
#     try:
#         # Get the next row from the data stream
#         if current_index >= len(df):
#             return jsonify({'message': 'Data stream ended'}), 200
        
#         new_df = kline(current_index)
#         current_index += 1

#         side = sidex(new_df)
#         signal = signalx(new_df)
#         order(side, signal, df=new_df)

#         session['current_index'] = current_index  # Update session with current index

#         return jsonify(new_df.to_dict(orient='records')), 200
#     except Exception as e:
#         return str(e), 500

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)



# # The provided code appears to be functioning correctly in terms of streaming data row by row 
# # and incrementing the index. However, the error message "Data stream ended" indicates that 
# # you've reached the end of your CSV file ('RHEL.csv') during the data streaming process.
# # Here's a breakdown of what's happening and how to address the "Data stream ended" message:
# # Code Analysis:
# # Data Initialization:
# # You load the 'RHEL.csv' file into a Pandas DataFrame (df).
# # dfx is initialized with the first row of the DataFrame.
# # current_index starts at 0.
# # Streaming Route (/stream):
# # The update_klines function fetches a new row from the DataFrame using the kline function and 
# # increments the current_index.
# # It processes signals using sidex and signalx and prints order information.
# # The current index is stored in the Flask session.
# # The fetched row is returned as a JSON response.
# # Error Handling:
# # If an IndexError occurs (meaning you've tried to access a row beyond the DataFrame's end), the 
# # function returns the "Data stream ended" message.
# # Reasons for "Data stream ended" Error:
# # File Size: The 'RHEL.csv' file might be smaller than you expect, and you've reached the end of 
# # the data quickly.
# # Index Issue: There could be an issue with how the current_index is being incremented or managed, 
# # causing it to reach the end of the DataFrame prematurely.


import pandas as pd
from flask import Flask, jsonify,render_template
import time

app = Flask(__name__)




# df = pd.read_csv('RHEL.csv')
# # df['Date'] = pd.to_datetime(df['Date'], utc=True)  # Specify UTC as the timezone
# df = df.drop('adj close', axis=1)
# current_index = 0
# Sample DataFrame
df = pd.read_csv('RHEL.csv')
df['Date'] = pd.to_datetime(df['Date'], utc=True)  # Specify UTC as the timezone
df['time'] = df['Date'].astype(int) // 10**9 
df.rename(columns={'Date': 'Time'}, inplace=True)
df.columns = df.columns.str.lower()
df = df.drop('adj close', axis=1)
current_index = 0

@app.route('/stream')
def update_klines():
    global current_index
    if current_index >= len(df):
        return jsonify({'message': 'Data stream ended'}), 200

    # Get the next row from the data stream
    new_data = df.iloc[current_index]
    current_index += 1

    return jsonify(new_data.to_dict()), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
