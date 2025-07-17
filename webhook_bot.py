from flask import Flask, request
import alpaca_trade_api as tradeapi

app = Flask(__name__)

# ✅ Alpaca API keys (LIVE endpoint)
API_KEY = 'AKSGMAWK87QZ8DMH8CY6'
API_SECRET = 'pOVvJg5mlmYfHhSIa5hymn4jjNdC5C5cyOXDiYiB'
BASE_URL = 'https://api.alpaca.markets'

# Initialize Alpaca API client
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get('ticker')
    action = data.get('action')

    if action == 'buy':
        try:
            # Get current price for setting bracket levels
            quote = api.get_last_quote(symbol)
            last_price = (quote.askprice + quote.bidprice) / 2

            take_profit_price = round(last_price * 1.08, 2)  # 8% take profit
            stop_loss_price = round(last_price * 0.95, 2)    # 5% stop loss

            api.submit_order(
                symbol=symbol,
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc',
                order_class='bracket',
                take_profit={'limit_price': take_profit_price},
                stop_loss={'stop_price': stop_loss_price}
            )
            return f"Bracket order placed for {symbol}", 200
        except Exception as e:
            return str(e), 500

    return "Invalid action", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
