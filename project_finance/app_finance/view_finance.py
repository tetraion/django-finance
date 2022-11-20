import pandas as pd
import numpy as np
import talib as ta
from pandas_datareader import data
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')

import base64
from io import BytesIO

import mplfinance as mpf

# 線形回帰モデル
from sklearn.linear_model import LinearRegression
# 時系列分割
from sklearn.model_selection import TimeSeriesSplit
# 予測精度検証
from sklearn.metrics import mean_squared_error as mse

def Output_Graph():
	buffer = BytesIO()                   #バイナリI/O(画像や音声データを取り扱う際に利用)
	plt.savefig(buffer, format="png")    #png形式の画像データを取り扱う
	buffer.seek(0)                       #ストリーム先頭のoffset byteに変更
	img   = buffer.getvalue()            #バッファの全内容を含むbytes
	graph = base64.b64encode(img)        #画像ファイルをbase64でエンコード
	graph = graph.decode("utf-8")        #デコードして文字列から画像に変換
	buffer.close()
	return graph

def Plot_Graph(search, start, end):
    # end = datetime.datetime.today()
    # start = (pd.Period(end, 'D') - 365).start_time
    

    df = data.DataReader(search, 'yahoo', start, end)
    # df = data.DataReader(search,'stooq',start=start,end=end)

    date = df.index
    close = df['Adj Close']

    span01=5
    span02=25
    span03=50

    #移動平均
    df['sma01']=close.rolling(window=span01).mean()
    df['sma02']=close.rolling(window=span02).mean()
    df['sma03']=close.rolling(window=span03).mean()
    #MACD
    df['macd'], df['macdsignal'], df['macdhint'] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    #RSI
    df['RSI'] = ta.RSI(close, timeperiod=span02)
    #ボリンジャーバンド
    df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevup=2, nbdevdn=2, matype=0)

    plt.switch_backend("AGG")        #スクリプトを出力させない
    plt.figure(figsize=(15,15))
    plt.subplot(5,1,1)

    plt.title('moving average')
    plt.plot(date,close,label='Close',color='#99b898')
    plt.plot(date,df['sma01'],label='5-day',color='#e84a5f')
    plt.plot(date,df['sma02'],label='25-day',color='#ff847c')
    plt.plot(date,df['sma03'],label='50-day',color='#feceab')
    plt.legend()

    plt.subplot(5,1,2)
    plt.title('volume')
    plt.bar(date,df['Volume'],label='Volume',color='grey')
    plt.legend()

    plt.subplot(5,1,3)
    plt.title('MACD')
    plt.fill_between(date, df['macdhint'], color='grey', alpha=0.5, label='MACD_hint')
    plt.hlines(0,start,end,"gray",linestyle='dashed')
    plt.legend()

    plt.subplot(5,1,4)
    plt.title('RSI')
    plt.plot(date, df['RSI'], label='RSI',color="gray")
    plt.hlines([30,50,70],start,end,"gray",linestyle='dashed')
    plt.legend()

    plt.subplot(5,1,5)
    plt.title('bollinger band')
    plt.plot(date,close,label='Close',color='#99b898')
    plt.fill_between(date, df['upper'], df['lower'], color='grey', alpha=0.3)
    plt.legend()

    graph = Output_Graph()           #グラフプロット
    return graph

def candle(search, start, end):
    df = data.DataReader(search, 'yahoo', start, end)
    # df = data.DataReader(search,'stooq',start=start,end=end)

    close = df['Adj Close']

    span01=5
    span02=25
    span03=50




    #ボリンジャーバンド
    df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevup=2, nbdevdn=2, matype=0)
    tcdf = df[['upper','middle','lower']]

    df_candle = df[['High','Low','Open','Close','Volume']]

    plt.switch_backend("AGG") 

    apd = mpf.make_addplot(tcdf)

    mpf.plot(df_candle,addplot=apd,type='candle',style='yahoo', figsize=(15,7))

    graph = Output_Graph()           #グラフプロット
    return graph

def zyukaiki(search, start, end):
    df = data.DataReader(search, 'yahoo', start, end)
    df['weekday'] = df.index.weekday
    data_technical = df.copy()
    data_technical['Body'] = data_technical['Open'] - data_technical['Close']

    data_technical['Close_diff'] = data_technical['Close'].diff(1)

    data_technical['Close_next'] = data_technical['Close'].shift(-1)
    data_technical = data_technical.dropna(how='any')
    data_technical = data_technical[data_technical['weekday']== 3]
    data_technical = data_technical[['High', 'Low', 'Open', 'Close', 'Body', 'Close_diff', 'Close_next']]

    days = end - start
    test2 = start + days*3/4

    train = data_technical[: start + days*3/4]
    test = data_technical[test2 :]
    X_train = train.drop(columns=['Close_next']) #学習用説明変数
    y_train = train['Close_next'] #学習用目的変数

    X_test = test.drop(columns=['Close_next']) #test用説明変数
    y_test = test['Close_next'] #test用目的変数

    # 実際のデータで実行
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    score = np.sqrt(mse(y_test, y_pred))
    # print(f'RMSE: {score}')
    # 実際のデータと予測データをデータフレームにまとめる
    df_result = test[['Close_next']]
    df_result['Close_pred'] = y_pred

    # 実際のデータと予測データの比較グラフを作成
    plt.switch_backend("AGG")        #スクリプトを出力させない
    plt.figure(figsize=(10,6))
    plt.plot(df_result[['Close_next', 'Close_pred']])
    plt.plot(df_result['Close_next'], label='Close_next', color='orange')
    plt.plot(df_result['Close_pred'], label='Close_pred', color='blue')
    plt.xlabel('Date')
    plt.ylabel('JPY')
    plt.legend()

    graph = Output_Graph()           #グラフプロット
    return graph,score

    