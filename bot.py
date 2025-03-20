import telebot
import requests

# 🔑 Your Telegram Bot Token & Finnhub API Key
BOT_TOKEN = "7713614539:AAHZOk9iMpW0yVihGi6mXmyadSCMjHLbZJ0"
bot = telebot.TeleBot(BOT_TOKEN)
FINNHUB_API_KEY = "cvdlsl9r01qm9khlpis0cvdlsl9r01qm9khlpisg"

bot = telebot.TeleBot(BOT_TOKEN)

# 📌 Command: /trade (Trading Features Menu)
@bot.message_handler(commands=['trade'])
def trade_menu(message):
    bot.send_message(message.chat.id, "📊 *Trading Features:*\n"
                                      "1️⃣ /price [symbol] - Live asset price\n"
                                      "2️⃣ /predict [symbol] - Market direction\n"
                                      "3️⃣ /sentiment [symbol] - Market sentiment\n\n"
                                      "💡 Example: /price AAPL (Apple stock)\n"
                                      "💡 Example: /predict BTC (Bitcoin)", parse_mode="Markdown")

# 📈 Command: /price [symbol] - Get Live Price
@bot.message_handler(commands=['price'])
def get_price(message):
    try:
        symbol = message.text.split()[1].upper()
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url).json()
        if 'c' in response:
            bot.send_message(message.chat.id, f"💰 *{symbol} Price:* ${response['c']}", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "❌ Invalid Symbol! Example: /price AAPL")
    except:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid symbol! Example: /price TSLA")

# 🔮 Command: /predict [symbol] - Market Up/Down Prediction
@bot.message_handler(commands=['predict'])
def predict_market(message):
    try:
        symbol = message.text.split()[1].upper()
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url).json()
        
        if 'c' in response:
            current_price = response['c']
            prev_close = response['pc']
            if current_price > prev_close:
                trend = "📈 *UP (Bullish)*"
            else:
                trend = "📉 *DOWN (Bearish)*"
            bot.send_message(message.chat.id, f"🔮 *Prediction for {symbol}:*\n{trend}", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "❌ Invalid Symbol! Example: /predict BTC")
    except:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid symbol! Example: /predict BTC")

# 📊 Command: /sentiment [symbol] - Market Sentiment Analysis
@bot.message_handler(commands=['sentiment'])
def market_sentiment(message):
    try:
        symbol = message.text.split()[1].upper()
        url = f"https://finnhub.io/api/v1/news-sentiment?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url).json()

        if 'sentimentScore' in response:
            sentiment_score = response['sentimentScore']
            if sentiment_score > 0:
                sentiment = "🟢 Positive Sentiment"
            elif sentiment_score < 0:
                sentiment = "🔴 Negative Sentiment"
            else:
                sentiment = "🟡 Neutral Sentiment"
            
            bot.send_message(message.chat.id, f"📊 *Market Sentiment for {symbol}:*\n{sentiment}", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "❌ Invalid Symbol! Example: /sentiment TSLA")
    except:
        bot.send_message(message.chat.id, "⚠️ Please enter a valid symbol! Example: /sentiment BTC")

# 🚀 Start Bot
bot.polling()
