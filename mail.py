import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_KEY_NEWS = "NEW API"
STOCK_API_NEW = "STOCK API"

parameters_STOCK = {"function": "TIME_SERIES_DAILY", "symbol": STOCK_NAME, "apikey": STOCK_API_NEW}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# response_2 = requests.get(NEWS_ENDPOINT,params=parameters_NEWS)
# response_2.raise_for_status()

response_1 = requests.get(STOCK_ENDPOINT, params=parameters_STOCK)
response_1.raise_for_status()
data = response_1.json()["Time Series (Daily)"]
data_list = [value for (item, value) in data.items()]
# printing later data_list
yesterday_data = data_list[0]
yesterday_close_price = yesterday_data["4. close"]
print(yesterday_close_price)

day_before_yesterday_data = data_list[1]
# print(day_before_yesterday_data)
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_close_price) - float(day_before_yesterday_closing_price)
print(difference)
up_dowm = None

if difference > 0:
    up_dowm = "🔺"

else:
    up_dowm = "🔻"

diff_percent = difference / float(yesterday_close_price) * 100


if abs(diff_percent) > 1:
    params_new = {"apikey": API_KEY_NEWS, "qInTitle": COMPANY_NAME}
    new_response = requests.get(NEWS_ENDPOINT, params=params_new)
    new_response.raise_for_status()
    article = new_response.json()["articles"]
    three_articles = article[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_dowm} {diff_percent}\n Headline : {article['title']}.\n Brief {article['description']}" for article in
                          three_articles]

    account_sid = 'YOUR ID'
    auth_token = 'TWILIO TOKEN'
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(

            body=article,
            from_='Twilio Number',
            to='Your number'

        )
