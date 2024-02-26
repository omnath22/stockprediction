from django.shortcuts import render, redirect
import requests
import yfinance as yf
import pandas as pd
import numpy as np
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import date
from joblib import load
from prophet import Prophet
from prophet.plot import plot_plotly
import matplotlib.pyplot as plt
import json

def signout(request):
    logout(request)
    return redirect('/')

forecast = pd.DataFrame()
# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def home(request):
    
    # user = User.objects.get(username='omnath2')
    # hashed_login_password = make_password('root')
    # if user.password == hashed_login_password:
    #     print("Passwords match!")
    # else:
    #     print("Passwords don't match.")

    # print(user.password)  # This will print the hashed password
    url = ('https://newsapi.org/v2/top-headlines?'
    'country=in&'
    'category=business&'
    'apiKey=7919e2baf4204e35ad417533b496a930')
    response = requests.get(url)
    
    if request.method:
            if request.GET.get('confirmpassword'):
                print("signup")
                # form = UserCreationForm(request.GET)
                # print(form)
                email = request.GET.get('email')
                password = request.GET.get('password')
                confirmpassword = request.GET.get('confirmpassword')
                # print(email)
                print(password)
                print(confirmpassword)
                if is_ajax(request=request):
                    print("inside signupajax")
                
                    user =User.objects.create_user(username=email,password=password)
                    user.save()
                    if user is not None:
                        login(request,user)
                        return JsonResponse({"message":"yes"})
                        
                    else:
                        return JsonResponse({"message": "no"})

            else:
                email = request.GET.get('email')
                password = request.GET.get('password')
                print(email)
                if is_ajax(request=request):
                    print("inside ajax")
                    user =authenticate(request,username=email,password=password)
                    print(user)
                    if user is not None:
                        login(request,user)
                        return JsonResponse({"message":"yes"})
                        
                    else:
                        return JsonResponse({"message": "no"})

              




            # print("login") 
    

    # print(response.json())
    return render(request, 'index.html',{'response':response.json()})




def details(request):
    # print(request.GET)
    if not request.user.is_authenticated:
        messages.success(request,'You must Log In')
        return redirect('/')
    else:
            
        tk = (request.GET['tickername'])
        tkres = tk  + ".BO"
        # url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=ioc&apikey=SF2KJLRRW7BRU3YD'
        # r = requests.get(url)
        # data = r.json()

        # print(data)

        ticker = yf.Ticker(tkres)
        data = ticker.history(interval="1wk", period="5y")
        short_ema = data["Close"].ewm(span=12, min_periods=12).mean()
        long_ema = data["Close"].ewm(span=26, min_periods=26).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=9, min_periods=9).mean()

        data["MACD"] = macd
        data["Signal"] = signal
        # print(data['MACD'].iloc[-1])
        # print(data['Signal'].iloc[-1])
        momPoint = ""
        if data['MACD'].iloc[-1] > data['Signal'].iloc[-1]:
            # print('Bullish')
            momPoint = "High Momentum"
        else:
            # print("Bearish")
            momPoint = "Low Momentum"


        print(ticker.info)
        tickername = ticker.info['symbol']
        tickercurrentprice = ticker.info['currentPrice']
        tickerchangefrompreviousclosepercentage = round((((ticker.info['currentPrice'] - ticker.info['previousClose'])/ticker.info['previousClose'] )* 100), 2)
        tickerchangefrompreviousclosewithoutround = ticker.info['currentPrice'] - ticker.info['previousClose']
        tickerchangefrompreviousclose = round(tickerchangefrompreviousclosewithoutround, 2)
        tickervolume = ticker.info['volume']
        if tickervolume // 1000000 >0:
            tickervolume=round(tickervolume/1000000,2)
            tickervolume = str(tickervolume) + "M"
        elif tickervolume // 1000 >0:
            tickervolume =round(tickervolume/1000,2)
            tickervolume = str(tickervolume) + "K"
        print(tickervolume)
        # print(tickerchangefrompreviousclosepercentage)
        # print(tickername.actions)
    
        if tickerchangefrompreviousclose>0:
            tickerchangefrompreviousclose = str(tickerchangefrompreviousclose)
            tickerchangefrompreviousclose = '+' + tickerchangefrompreviousclose
        else:
            tickerchangefrompreviousclose = str(tickerchangefrompreviousclose)
            tickerchangefrompreviousclose = '-' + tickerchangefrompreviousclose
        # print(tickerchangefrompreviousclose)

        
        if tickerchangefrompreviousclosepercentage>0:
            tickerchangefrompreviousclosepercentage = str(tickerchangefrompreviousclosepercentage)
            tickerchangefrompreviousclosepercentage = '+' + tickerchangefrompreviousclosepercentage
        else:
            tickerchangefrompreviousclosepercentage = str(tickerchangefrompreviousclosepercentage)
            tickerchangefrompreviousclosepercentage = '-' + tickerchangefrompreviousclosepercentage
    
        # roe = round(data['QuaterlyEarningsGrowthYOY'] *100, 2)
        # earningsgrowth = round(data['QuaterlyRevenueGrowthYOY']*100, 2)
        # print(roe)
        # print(earningsgrowth)
            

        finPoint = ""
        valPoint = ""
        # print(earningsgrowth)

        key_to_check = "returnOnEquity"  # Replace with the key you want to check
        key_to_check_earningsgrowth = "earningsGrowth"
        flag = -2
        
        if key_to_check in ticker.info:
            flag=0
        elif key_to_check_earningsgrowth in ticker.info:
            flag=1
        elif key_to_check not in ticker.info and key_to_check_earningsgrowth not in ticker.info:
            flag=-2
        elif key_to_check in ticker.info and key_to_check_earningsgrowth in ticker.info:
            flag=2
        if flag==1 and ticker.info['earningsGrowth']<1:
            earningsgrowth = round(ticker.info['earningsGrowth'] *100, 2)
        elif flag==1:
            earningsgrowth = round(ticker.info['earningsGrowth'], 2)
        if flag==2:
            print("The API response contains the key:", key_to_check)
            # Access the value associated with the key:
            roe = round(ticker.info[key_to_check] *100, 2)
            print("Value:", roe)
            
            if earningsgrowth > 10 and roe > 10:
                finPoint = "Strong Financial"
            elif earningsgrowth >5 and roe >5:
                finPoint = "Good Financial"
            else:
                finPoint = "Weak Financial"
        elif flag==1:
            print("The API response does not contain the key:", key_to_check)
            if earningsgrowth > 10:
                finPoint = "Strong Financial"
            elif earningsgrowth >5:
                finPoint = "Good Financial"
            else:
                finPoint = "Weak Financial"
        else:
            finPoint = "NA"



        pe = ticker.info['currentPrice'] / (ticker.info['revenuePerShare'] * ticker.info['operatingMargins'])
        if pe >= 30:
            valPoint = "High Valuation"
        elif pe>5 and pe<30:
            valPoint = "Medium Valuation"
        else:
            valPoint = "Low Valuation"
        START = "2015-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")
        period =  2*365
        def load_data(ticker):
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data
        data = load_data(tkres)
        c_data = data
        print(data)
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        print(forecast)
        df_train = df_train.rename(columns={"Date": "Date", "Close": "Price"})
        # fig = m.plot(forecast)

        # Customize the plot (optional
        # Show the plot
        # plt.show()

        # data_to_send = forecast.to_json(orient='records')
        print(forecast['yhat'].iloc[-1])
        last_record = forecast['yhat'].iloc[-1]
        sugg = ""
        if last_record <= (tickercurrentprice + tickercurrentprice * 0.2):
            sugg = "DONT BUY"
        else:
            sugg = "GOOD TO BUY"
        stock_data = {
            'timestamps': [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in forecast['ds'].tolist()],
            'price': c_data['Close'].tolist(),
        }
        data_to_send = {
            'timestamps': [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in forecast['ds'].tolist()],
            'yhats': forecast['yhat'].tolist(),
            'yhat_lowers': forecast['yhat_lower'].tolist(),
            'yhat_uppers': forecast['yhat_upper'].tolist(),
        }
        data_to_send = json.dumps(data_to_send)
        stock_data_to_send = json.dumps(stock_data)
        
        
  
        
        return render(request, 'details.html',{'ticker':tk,'tickername': ticker.info['longName'],'tickercurrentprice':tickercurrentprice,'tickerchangefrompreviousclose':tickerchangefrompreviousclose,'tickerchangefrompreviousclosepercentage':tickerchangefrompreviousclosepercentage,'tickervolume':tickervolume,'finPoint':finPoint,'valPoint':valPoint,'momPoint':momPoint,'data':data_to_send,'sugg':sugg,'stockdata':stock_data_to_send})

