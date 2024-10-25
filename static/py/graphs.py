import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def generate_stock_data(start_date, days, initial_price):
    date_range = pd.date_range(start=start_date, periods=days)
    prices = [initial_price]
    for _ in range(1, days):
        change = np.random.normal(0, 2)
        new_price = max(prices[-1] + change, 0.01)
        prices.append(new_price)
    volume = np.random.randint(100000, 1000000, size=days)
    df = pd.DataFrame({
        'Date': date_range,
        'Open': prices,
        'High': [p * (1 + abs(np.random.normal(0, 0.02))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.02))) for p in prices],
        'Close': [p * (1 + np.random.normal(0, 0.01)) for p in prices],
        'Volume': volume
    })  
    return df

start_date = datetime(2023, 1, 1)
days = 252
initial_price = 100
df = generate_stock_data(start_date, days, initial_price)
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()
df['Daily_Return'] = df['Close'].pct_change()
df['Volatility'] = df['Daily_Return'].rolling(window=20).std() * np.sqrt(252)

def plot_stock_data(df, title):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(title, fontsize=16)
    ax1.plot(df['Date'], df['Close'], label='Close Price')
    ax1.plot(df['Date'], df['MA20'], label='20-day MA')
    ax1.plot(df['Date'], df['MA50'], label='50-day MA')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax2.bar(df['Date'], df['Volume'], label='Volume', alpha=0.5)
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Date')
    ax2.legend()
    plt.tight_layout()
    plt.show()

plot_stock_data(df, 'Stock Price Analysis')
print(df.describe())
latest_price = df['Close'].iloc[-1]
highest_price = df['High'].max()
lowest_price = df['Low'].min()
avg_volume = df['Volume'].mean()
volatility = df['Volatility'].iloc[-1]

print(f"\nLatest Price: ${latest_price:.2f}")
print(f"52-Week High: ${highest_price:.2f}")
print(f"52-Week Low: ${lowest_price:.2f}")
print(f"Average Daily Volume: {avg_volume:.0f}")
print(f"Current Volatility: {volatility:.2%}")

significant_moves = df[abs(df['Daily_Return']) > 0.05]
print("\nSignificant Price Moves (>5%):")
for _, row in significant_moves.iterrows():
    print(f"Date: {row['Date'].date()}, Return: {row['Daily_Return']:.2%}")