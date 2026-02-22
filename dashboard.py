from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

balance = 100000
positions = []
pnl = 0

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return f"""
    <html>
    <head>
        <title>Paperbot Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="background:black;color:lime;font-family:Arial;text-align:center;">
        <h1>Paper Trading Bot</h1>
        <h2>Balance: ${balance}</h2>
        <h2>PNL: ${pnl}</h2>
        <h3>Open Positions: {len(positions)}</h3>
    </body>
    </html>
    """
