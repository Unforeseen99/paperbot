import os
import time
import random
from fastapi import FastAPI
from threading import Thread

app = FastAPI()

# SETTINGS
BALANCE = float(os.getenv("PAPER_START_BALANCE", "100000"))
MAX_ALLOC = float(os.getenv("MAX_ALLOC_PCT", "0.30"))
PER_TRADE = float(os.getenv("PER_TRADE_PCT", "0.01"))
TRAIL = float(os.getenv("TRAILING_STOP_PCT", "0.005"))

positions = {}
pnl = 0

symbols = os.getenv(
    "SYMBOLS",
    "BTC,ETH,SOL,XRP,ADA"
).split(",")


def fake_price():
    return random.uniform(50, 50000)


def trader():
    global pnl, BALANCE

    while True:

        # randomly open trade
        if random.random() > 0.7 and len(positions) < 5:

            sym = random.choice(symbols)

            if sym not in positions:

                size = BALANCE * PER_TRADE
                entry = fake_price()

                positions[sym] = {
                    "entry": entry,
                    "size": size,
                    "trail": entry * (1 - TRAIL),
                }

                print(f"OPEN {sym} @ {entry}")

        # manage trades
        for sym in list(positions.keys()):

            price = fake_price()

            if price < positions[sym]["trail"]:

                profit = (price - positions[sym]["entry"]) * (
                    positions[sym]["size"] / positions[sym]["entry"]
                )

                pnl += profit
                BALANCE += profit

                print(f"CLOSE {sym} PNL {profit}")

                del positions[sym]

            else:

                new_trail = price * (1 - TRAIL)

                if new_trail > positions[sym]["trail"]:
                    positions[sym]["trail"] = new_trail

        time.sleep(5)


Thread(target=trader, daemon=True).start()


@app.get("/")
def dashboard():
    return {
        "balance": BALANCE,
        "pnl": pnl,
        "positions": positions,
    }


@app.get("/positions")
def get_positions():
    return positions


@app.get("/pnl")
def get_pnl():
    return {
        "balance": BALANCE,
        "pnl": pnl,
    }
