import datetime
from django.shortcuts import render, redirect
import requests
import yfinance as yf
import pandas as pd
import numpy as np
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import date
from joblib import load
from prophet import Prophet
from prophet.plot import plot_plotly
import matplotlib.pyplot as plt
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
from django.db import connection
from django.core.mail import EmailMessage, send_mail
import smtplib  # Optional for logging errors
# from stockpredictionai.tasks import send_weekly
from stockpredictionai.celery import app
import mysql.connector
import openai
from .chatgpt_service import get_chat_response
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Set your OpenAI API key
openai.api_key = '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'



db_host = "localhost"
db_user = "root"
db_password = "root"
db_name = "stockpredictionai"


def signout(request):
    logout(request)
    return redirect('/')
def sendDataBasedOnCategory(data_list):
    for user in data_list:
        try:
            print("in try block")
            
            mydb = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            if user[0] == "Basic":
                query = "SELECT symbol_name, trend FROM prediction WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK) ORDER BY RAND() LIMIT 1;"
                mycursor2 = mydb.cursor()

                mycursor2.execute(query)

                myresult = mycursor2.fetchone()
                print(myresult)
                subject = 'Your Weekly Newsletter - Stockpredictionai'
                body = """**Investment Insights:**"""+myresult[0]+" -- "+myresult[1]+""""
    """
                from_email = 'omnathgupta11@gmail.com'
                to_email = user[1]

                message = EmailMessage(subject, body, from_email, [to_email])
                message.content_subtype = "html"
                
                # Optional: Add attachments (replace with your actual logic)
                # attachment_file = open("path/to/attachment.pdf", "rb")
                # email.attach(filename="attachment.pdf", content=attachment_file.read())

                message.send()

                print("Email sent successfully!")
            
            elif user[0] == "Pro":
                query = "SELECT symbol_name, trend FROM prediction WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK) ORDER BY RAND() LIMIT 2;"
                mycursor3 = mydb.cursor()

                mycursor3.execute(query)


                rows = mycursor3.fetchall()
                print(rows)

                subject = 'Your Weekly Newsletter - Stockpredictionai'
                body = """**Investment Insights:**"""+rows[0][0]+" -- "+rows[0][1]+"...\n" +rows[1][0]+" -- "+rows[1][1]+ """
    """
                from_email = 'omnathgupta11@gmail.com'
                to_email = user[1]

                message = EmailMessage(subject, body, from_email, [to_email])
                message.content_subtype = "html"
                
                # Optional: Add attachments (replace with your actual logic)
                # attachment_file = open("path/to/attachment.pdf", "rb")
                # email.attach(filename="attachment.pdf", content=attachment_file.read())

                message.send()
                
                print("Email sent successfully!")
            
                
            else:
                query = "SELECT symbol_name, trend FROM prediction WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK) ORDER BY RAND() LIMIT 5;"
                mycursor2 = mydb.cursor()

                mycursor2.execute(query)

                rows = mycursor2.fetchall()
                print(rows)

                subject = 'Your Weekly Newsletter - Stockpredictionai'
                body = """**Investment Insights:**"""+rows[0][0]+" -- "+rows[0][1]+"...\n" +rows[1][0]+" -- "+rows[1][1]+"...\n" +rows[2][0]+" -- "+rows[2][1]+"...\n" +rows[3][0]+" -- "+rows[3][1]+"...\n" +rows[4][0]+" -- "+rows[4][1]+ """
    """
                from_email = 'omnathgupta11@gmail.com'
                to_email = user[1]

                message = EmailMessage(subject, body, from_email, [to_email])
                message.content_subtype = "html"
                
                # Optional: Add attachments (replace with your actual logic)
                # attachment_file = open("Capture2.png", "rb")
                # message.attach(filename="Capture2.png", content=attachment_file.read())

                message.send()
                
                print("Email sent successfully!")



        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")


def send_email(user_list):
    for user in user_list:
        try:
            print("in try block")
            
            mydb = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            query = "SELECT symbol_name, trend FROM prediction WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK) ORDER BY RAND() LIMIT 1;"
            mycursor2 = mydb.cursor()

            mycursor2.execute(query)

            myresult = mycursor2.fetchone()
            print(myresult)
            subject = 'Your Weekly Newsletter - Stockpredictionai'
            body = """**Investment Insights:**"""+myresult[0]+" -- "+myresult[1]+""""
"""
            from_email = 'omnathgupta11@gmail.com'
            to_email = user[1]

            message = EmailMessage(subject, body, from_email, [to_email])
            message.content_subtype = "html"
            
            # Optional: Add attachments (replace with your actual logic)
            # attachment_file = open("path/to/attachment.pdf", "rb")
            # email.attach(filename="attachment.pdf", content=attachment_file.read())

            message.send()
            mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
              # Create a cursor object
            mycursor = mydb.cursor()
            
            my_date = date.today()
            # Update query with placeholders for security
            sql = "UPDATE newsletter SET date = %s"
            formatted_date_str = my_date.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
            val = (formatted_date_str,)  # Replace with actual values

            # Execute the update query
            mycursor.execute(sql, val)

            # Commit the changes
            mydb.commit()


            print("Email sent successfully!")
            

        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")

forecast = pd.DataFrame()
# Create your views here.
# def send_mail_to_all(request):
#     send_weekly.delay()
#     return HttpResponse('Sent')

# now = date.today()
# print(now)
# cursor1 = connection.cursor()
# cursor1.execute("SELECT date FROM newsletter where email='og501110@gmail.com'")
# data_from_newsletter_table = cursor1.fetchone()
# formated_date = data_from_newsletter_table[0].strftime("%Y-%m-%d")
# print(formated_date)
# # print(data_from_newsletter_table)
# if formated_date != now and now.weekday() ==6:
#     print("sunday")
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM newsletter")
#     data_from_database = cursor.fetchall()    
#     send_email(data_from_database)
#     print(data_from_database)


cursor1 = connection.cursor()
cursor1.execute("SELECT date FROM newsletter where email='og501110@gmail.com'")
data_from_newsletter_table = cursor1.fetchone()
# formated_date = data_from_newsletter_table[0].strftime("%Y-%m-%d")
# print(formated_date)
if data_from_newsletter_table is not None:
    formated_date = data_from_newsletter_table[0].strftime("%Y-%m-%d")

    # Check if subscribed on Sunday but not today's Sunday
    if formated_date != datetime.date.today().strftime("%Y-%m-%d") and datetime.date.today().weekday() ==6:
        # Simulate sending data (replace with your actual logic)
        print("yes inside if of sending data")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM newsletter")
        data_from_database = cursor.fetchall()
        print(data_from_database)
        send_email(data_from_database)
        cursor2 = connection.cursor()
        cursor2.execute("SELECT plan,email FROM auth_user")
        data_from_database_user_table = cursor2.fetchall()
        print(data_from_database_user_table)
        sendDataBasedOnCategory(data_from_database_user_table)
    else:
        print("inside else")

def subscribe(request):
    email_to_add = request.GET['joinusinput']
    print(email_to_add)
    print("inside subscribe to add email into newsletter")
    try:
        sql = """
        INSERT INTO newsletter (email,date)
        VALUES (%s,%s)
        """
        cursor = connection.cursor()
        cursor.execute(sql, (email_to_add, datetime.date.today().strftime("%Y-%m-%d")))
        connection.commit()
        return render(request,'subscribe.html',{'response':"yes"})
        # print(request.user)
    except Exception:
        print(Exception)
        return render(request,'subscribe.html',{'response':"no"})
    



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def request_with_retry(url):
    session = requests.Session()

    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')
    except requests.exceptions.Timeout as time_err:
        print(f'Timeout error occurred: {time_err}')
    except requests.exceptions.RequestException as err:
        print(f'An error occurred: {err}')

    return response
def home(request):
    authen = 0
    if request.user.is_authenticated:
        authen = 1
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
    response = request_with_retry(url)
# Call the send_email function

    
    if request.method == 'GET':
            if request.GET.get('confirmpassword'):
                print("signup")
                # form = UserCreationForm(request.GET)
                # print(form)
                email = request.GET.get('email')
                emailfromsignup = request.GET.get('emailfromsignup')
                password = request.GET.get('password')
                confirmpassword = request.GET.get('confirmpassword')
                # print(email)
                print(password)
                print(confirmpassword)
                print(emailfromsignup)
                if is_ajax(request=request):
                    print("inside signupajax")
                    #check for user already present
                    sql = f"SELECT * FROM auth_user WHERE username='{email}'"
                    cursor3 = connection.cursor()
                    cursor3.execute(sql)
                    myresult = cursor3.fetchone()
                    if myresult:
                        #meaning user is present
                        return JsonResponse({"status":"no","message":"User already present","authen":authen})
                    else:
                        user =User.objects.create_user(username=email,password=password)
                        user.save()
                        print(user.__dict__)
                        if user is not None:
                            login(request,user)
                            authen = 1
                            #updating the columns
                            sql = "UPDATE auth_user SET email = %s, totalPrediction = %s,date = %s,plan = %s WHERE username = %s"
                            formatted_date_str = date.today().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
                            val = (emailfromsignup,0,formatted_date_str,"Basic",email)  # Replace with actual values
                            mycursor = connection.cursor()
                            # Execute the update query
                            mycursor.execute(sql, val)

                            connection.commit()
                            print("successfully updated")
                            
                            return JsonResponse({"status":"yes","authen":authen})
                            
                        else:
                            return JsonResponse({"status": "no","message":"Error in signup","authen":authen})

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
                        authen = 1
                        #check if user is logged in for first time in a day if yes then make totalPrediction =0
                        try:
                            sql = "SELECT date FROM auth_user WHERE username=%s"
                            val = (email,)
                            mycursor = connection.cursor()
                            mycursor.execute(sql, val)
                            myresult = mycursor.fetchone()
                            print(myresult[0])
                            if myresult[0] != date.today():
                                
                                sql = "UPDATE auth_user SET totalPrediction = %s,date = %s WHERE username = %s"
                                formatted_date_str = date.today().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
                                val = (0,formatted_date_str,email)  # Replace with actual values
                                mycursor = connection.cursor()
                                # Execute the update query
                                mycursor.execute(sql, val)

                                connection.commit()
                                print("successfully updated")
                            else:
                                #Dont update totalPrediciton
                                #or dont do anything cause system has previosly updated both fields
                                pass
                        except Exception as e:
                            print(e)
                        try:
                            sql = "SELECT plan FROM auth_user WHERE username=%s"
                            cursor3 = connection.cursor()
                            cursor3.execute(sql,(request.user,))
                            myres = cursor3.fetchone()
                            print(myres[0])
                        except Exception as e:
                            print(e)
                        return JsonResponse({"message":"yes","authen":authen,"planselected":myres[0]})
                        
                    else:
                        return JsonResponse({"message": "no","authen":authen})

              




            # print("login")
    #it should run only when user is log in
    if request.user.is_authenticated:
        try:
            sql = "SELECT plan FROM auth_user WHERE username=%s"
            cursor3 = connection.cursor()
            cursor3.execute(sql,(request.user,))
            myres = cursor3.fetchone()
            print(myres[0])
        except Exception as e:
            print(e)
    else:
        myres = ("select")
    
    return render(request, 'index.html',{'response':response.json(),"authen":authen,"planselected":myres[0]})

def disclaimer(request):
    authen = 0
    isStockUnderWatch = 0
    if request.user.is_authenticated:
        authen = 1
    # print(authen)
        try:
            sql = "SELECT plan FROM auth_user WHERE username=%s"
            cursor3 = connection.cursor()
            cursor3.execute(sql,(request.user,))
            myres = cursor3.fetchone()
            print(myres[0])
        except Exception as e:
            print(e)
    else:
        myres = ("select")
    
    
    return render(request,'disclaimer.html',{"authen":authen,"planselected":myres[0]})


def selectPlan(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status":"You must log in"})
    if request.method == 'GET':
           
            if request.GET.get('plan'):
                print("plan")
                # form = UserCreationForm(request.GET)
                # print(form)
                plan = request.GET.get('plan')
                print(plan)

                if is_ajax(request=request):
                    print("inside plan to be selected")
                    try:
                        sql = "UPDATE auth_user SET plan = %s WHERE username = %s"
                        val = (plan,request.user)  # Replace with actual values
                        mycursor = connection.cursor()
                        # Execute the update query
                        mycursor.execute(sql, val)
                        connection.commit()
                        print("successfully updated your plan")
                        return JsonResponse({"message": f"Plan Upgraded to {plan}","status":"ok"})
                        # print(request.user)
                    except Exception as e:
                        print(e)
                        




                    return JsonResponse({"message":"error"})


def details(request):
    # print(request.GET)
    if not request.user.is_authenticated:
        messages.success(request,'You must Log In')
        return redirect('/')
    
    if request.method == "GET":
            if request.GET.get('stock_symbol'):
                # return redirect('/')
                print("add")
                # form = UserCreationForm(request.GET)
                # print(form)
                stock_symbol = request.GET.get('stock_symbol')
                print(stock_symbol)
                if is_ajax(request=request):
                    print("inside signupajax to add symbol into watchlist")
                    sql = "SELECT * FROM watchlist WHERE username=%s AND stock_name=%s"
                    cursor3 = connection.cursor()
                    cursor3.execute(sql,(request.user,stock_symbol))
                    myresult = cursor3.fetchone()
                    if myresult:
                        # means stock is in watchlist just have to remove
                        try:
                            sql = "DELETE FROM watchlist WHERE username=%s AND stock_name=%s"
                            cursor4 = connection.cursor()
                            cursor4.execute(sql,(request.user,stock_symbol))
                            connection.commit()
                            return JsonResponse({"message":"Stock Deleted from watchlist"})
                        except Exception:
                            return JsonResponse({"message":"Error in removing from watchlist"})
                    else:
                        try:
                            sql = """
                            INSERT INTO watchlist (stock_name,username)
                            VALUES (%s,%s)
                            """
                            cursor = connection.cursor()
                            cursor.execute(sql, (stock_symbol, request.user))
                            connection.commit()
                            return JsonResponse({"message": "Stock Added to watchlist"})
                            # print(request.user)
                        except Exception:
                            print(Exception)
                            return JsonResponse({"message": "Error in Adding to watchlist"})
                        
                        
                        

            else:
                try:
                    sql = "SELECT totalPrediction,plan FROM auth_user WHERE username=%s"
                    val = (request.user,)
                    mycursor = connection.cursor()
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchone()
                    print(myresult)
                except Exception as e:
                    print(e)
                
                

                #check if user exceed their limit if yes then redirect with message
                #you have exceeded your limit upgrade
                if myresult[1] == "Basic":
                    myr = 4
                elif myresult[1] == "Pro":
                    myr = 19
                else:
                    myr = 49
                
                if myresult[0] > myr:
                    messages.success(request,'You Have exceeded your limit upgrade your plan')
                    return redirect('/')
                else:
                        
                    sql = "UPDATE auth_user SET totalPrediction = %s WHERE username = %s"
                    val = (myresult[0] +1,request.user)  # Replace with actual values
                    mycursor = connection.cursor()
                    # Execute the update query
                    mycursor.execute(sql, val)

                    connection.commit()
                    print(f"successfully updated {myresult[0]+1}")


                    isStockUnderWatch =  0
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
                    try:
                        sql = """
                        INSERT INTO prediction (symbol_name,date,trend)
                        VALUES (%s,%s,%s)
                        """
                        cursor = connection.cursor()
                        cursor.execute(sql, (ticker.info['longName'], datetime.date.today().strftime("%Y-%m-%d"), sugg))
                        connection.commit()
                        # print(request.user)
                    except Exception:
                        try:
                            sql = "UPDATE prediction SET date = %s,trend = %s WHERE symbol_name = %s"
                            formatted_date_str = date.today().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
                            val = (formatted_date_str,sugg,ticker.info['longName'])  # Replace with actual values
                            mycursor = connection.cursor()
                            # Execute the update query
                            mycursor.execute(sql, val)

                            connection.commit()
                            print("successfully updated")
                            # print(request.user)
                        except Exception:
                            print(Exception)

                    
                    # url = ('https://newsapi.org/v2/everything?'
                    # 'q=Apple&'
                    # 'from=2024-02-04&'
                    # 'sortBy=popularity&'
                    # 'pageSize: 5&'
                    # 'apiKey=7919e2baf4204e35ad417533b496a930')
                    # response = request_with_retry(url)
                    # # print(response.json())
                    
                    url = 'https://newsapi.org/v2/everything?'
                    # params = {
                    #     'q': ticker.info['industryKey'],
                    #     'from': '2024-02-14',
                    #     'sortBy': 'popularity',
                    #     'apiKey': '7919e2baf4204e35ad417533b496a930',  # Replace with your actual API key
                    #     'pageSize': 5  # Specify the number of articles to retrieve
                    # }
                    params = {
                        'q': tk,  # Company name to search for
                        'from': '2024-02-20',
                        'apiKey': '7919e2baf4204e35ad417533b496a930',   # Your News API key
                        'pageSize': 5

                    }
                    response = requests.get(url, params=params)
                #     articles = [
                #     "Apple stock price is expected to rise in the next quarter.",
                #     "The new iPhone release was met with disappointment by critics.",
                #     "The company is facing financial difficulties."
                # ]
                    data = response.json()
                    print(data)
                    articles_with_sentiment = []
                    for article in data['articles']:
                        title = article['title']
                        # sentiment = TextBlob(title).sentiment.polarity
                        # if sentiment >= 0:
                        #     sentiment = "Positive"
                        # else:
                        #     sentiment = "Negative"
                        # articles_with_sentiment.append({"title": title, "sentiment": sentiment})
                        analyzer = SentimentIntensityAnalyzer()
                        sentiment_scores = analyzer.polarity_scores(title)
                        sentiment = ""
                        # Classify sentiment as positive, negative, or neutral based on compound score
                        if sentiment_scores['compound'] >= 0.05:
                            sentiment = 'Positive'
                        elif sentiment_scores['compound'] <= -0.05:
                            sentiment = 'Negative'
                        else:
                            sentiment = 'Neutral'
                        articles_with_sentiment.append({"title": title, "sentiment": sentiment})
                    
                    sql = "SELECT * FROM watchlist WHERE username=%s AND stock_name=%s"
                    cursor3 = connection.cursor()
                    cursor3.execute(sql,(request.user,tk))
                    myresult = cursor3.fetchone()
                    if myresult:
                        # meaning stock is under watch
                        isStockUnderWatch = 1

                    if request.user.is_authenticated:
                            try:
                                sql = "SELECT plan FROM auth_user WHERE username=%s"
                                cursor3 = connection.cursor()
                                cursor3.execute(sql,(request.user,))
                                myres = cursor3.fetchone()
                                print(myres[0])
                            except Exception as e:
                                print(e)
                    else:
                        myres = ("select") 
    
                    return render(request, 'details.html',{'ticker':tk,'tickername': ticker.info['longName'],'tickercurrentprice':tickercurrentprice,'tickerchangefrompreviousclose':tickerchangefrompreviousclose,'tickerchangefrompreviousclosepercentage':tickerchangefrompreviousclosepercentage,'tickervolume':tickervolume,'finPoint':finPoint,'valPoint':valPoint,'momPoint':momPoint,'data':data_to_send,'sugg':sugg,'stockdata':stock_data_to_send,'response':articles_with_sentiment,'isStockUnderWatch':isStockUnderWatch,"planselected":myres[0]})

def watchlist(request):
    if not request.user.is_authenticated:
        messages.success(request,'You must Log In')
        return redirect('/')
    if request.method == 'GET':
            if request.GET.get('stock'):
                print("inside delete")
                # form = UserCreationForm(request.GET)
                # print(form)
                stock = request.GET.get('stock')
                
                print(stock)
                if is_ajax(request=request):
                    print("inside watchlistajax to delete symbol from watchlist")
                
                    try:
                        sql = "DELETE FROM watchlist WHERE username=%s AND stock_name=%s"
                        cursor4 = connection.cursor()
                        cursor4.execute(sql,(request.user,stock))
                        connection.commit()
                        return JsonResponse({"message":"yes"})
                    except Exception:
                        return JsonResponse({"message":"Error in removing from watchlist"})

                    
                
    
                    

    try:
        sql = "SELECT stock_name FROM watchlist WHERE username=%s"
        cursor = connection.cursor()
        cursor.execute(sql,(request.user,))
        myresult = cursor.fetchall()
        print(myresult)
    except Exception as e:
        print(e)
    data = {}
    if myresult:
        for i in myresult:
            tkres = i[0]  + ".BO"
            ticker = yf.Ticker(tkres)
            # print(ticker.info)
            # tickercurrentprice = ticker.info['currentPrice']
            # tickerchangefrompreviousclosepercentage = round((((ticker.info['currentPrice'] - ticker.info['previousClose'])/ticker.info['previousClose'] )* 100), 2)
            # tickerchangefrompreviousclosewithoutround = ticker.info['currentPrice'] - ticker.info['previousClose']
            # tickerchangefrompreviousclose = round(tickerchangefrompreviousclosewithoutround, 2)
            # if tickerchangefrompreviousclose>0:
            #     tickerchangefrompreviousclose = str(tickerchangefrompreviousclose)
            #     tickerchangefrompreviousclose = '+' + tickerchangefrompreviousclose
            # else:
            #     tickerchangefrompreviousclose = str(tickerchangefrompreviousclose)
            #     tickerchangefrompreviousclose =tickerchangefrompreviousclose
            # # print(tickerchangefrompreviousclose)

            
            # if tickerchangefrompreviousclosepercentage>0:
            #     tickerchangefrompreviousclosepercentage = str(tickerchangefrompreviousclosepercentage)
            #     tickerchangefrompreviousclosepercentage = '+' + tickerchangefrompreviousclosepercentage
            # else:
            #     tickerchangefrompreviousclosepercentage = str(tickerchangefrompreviousclosepercentage)
            #     tickerchangefrompreviousclosepercentage =tickerchangefrompreviousclosepercentage
            # print(tickerchangefrompreviousclose)
            # print(tickerchangefrompreviousclosepercentage)
            # longName = ticker.info['longName']
            data[i[0]] = {
                    'symbol':i[0],
                    'longName': ticker.info['longName'],
                    'currentPrice': "₹" +str(ticker.info['currentPrice']),
                    'previousClose': ticker.info['previousClose'],
                    'changeFromPreviousClose': round(ticker.info['currentPrice'] - ticker.info['previousClose'], 2),
                    'changeFromPreviousClosePercentage': round(((ticker.info['currentPrice'] - ticker.info['previousClose']) / ticker.info['previousClose']) * 100, 2),
                    'changeDisplay': "+" + str(round(ticker.info['currentPrice'] - ticker.info['previousClose'], 2)) if ticker.info['currentPrice'] > ticker.info['previousClose'] else str(round(ticker.info['currentPrice'] - ticker.info['previousClose'], 2))
                }
        print(data)

    data = json.dumps(data)

    if request.user.is_authenticated:
        try:
            sql = "SELECT plan FROM auth_user WHERE username=%s"
            cursor3 = connection.cursor()
            cursor3.execute(sql,(request.user,))
            myres = cursor3.fetchone()
            print(myres[0])
        except Exception as e:
            print(e)
    else:
        myres = ("select")

    return render(request,'watchlist.html',{'data':data,"planselected":myres[0]})
# def chatbot(request):
#     chatbot_response = None
#     if request.method == 'POST':
#         print("inside chatbot msg")
#         prompt = request.POST.get('prompt')
#         # return JsonResponse({'response': response})
#         return render(request, 'chatbot.html',{})

def chat_view(request):
    if request.method == 'GET':
        user_message = request.GET.get('message')
        print(user_message)
        chatbot_response = get_chat_response(user_message)
        return JsonResponse({'user_message': user_message, 'chatbot_response': chatbot_response})

