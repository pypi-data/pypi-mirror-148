# currency-api-py
A python async wrapper for the currency-api API
# Installation
```cmd
py -m pip install -U currency-api-py

:: latest (unstable)
py -m pip install git+https://github.com/Marseel-E/currency-api-py
```
# Quickstart
```py
import asyncio

from currencyApi import CurrencyApi

async def main():
	async with CurrencyApi() as session:
		data = await session.convert("eur", "usd")
		print(data)

if __name__ = '__main__':
	asyncio.run(main())

# Output (2022-04-30)
>>> 1.054463
```