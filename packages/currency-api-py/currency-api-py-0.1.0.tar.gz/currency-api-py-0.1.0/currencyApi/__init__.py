from __future__ import annotations

"""
MIT License

Copyright (c) 2022 Marseel-E

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
STRUCTURE -> BASE_URL + @apiVersion + /date + /endpoint (.json|.min.json)
DATE      -> = LATEST | YYYY-MM-DD (MIN -> 2020-11-22)
ENDPOINTS -> /currencies (lists all the available currencies)
			-> /currencies/{currencyCode} (get currency list with 'currencyCode' as base currency)
			-> /currencies/{currencyCode1}/{currencyCode2} (get the currency value for 'currencyCode1'
			to 'currencyCode2')
"""

__all__ = ['CurrencyApi']
__title__ = 'currency-api-py'
__author__ = 'Marseel Eeso'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present Marseel Eeso'
__version__ = '0.1.0'
__path__ = __import__('pkgutil').extend_path(__path__, __name__)


import aiohttp

from typing import Optional, Dict, Union


BASE_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/"


class CurrencyApi:
	def __init__(self) -> None:
		self.session: Optional[aiohttp.ClientSession] = None

	async def __aenter__(self) -> "CurrencyApi":
		self.session = aiohttp.ClientSession()
		return self

	async def close_session(self) -> None:
		if self.session is not None:
			await self.session.close()

	async def __aexit__(self, *args) -> None:
		await self.close_session()

	async def _request(self, endpoint: str, date: Optional[str] = "latest") -> dict:
		if self.session is None:
			self.session = aiohttp.ClientSession()

		async with self.session.get(BASE_URL + date + "/" + endpoint + ".min.json") as response:
			if response.status != 200:
				raise Exception("Something wen't wrong. Make sure the currency code is correct, and the date isn't older than 2020-11-22")

			return await response.json()



	async def get_currencies(self, date: Optional[str] = "latest") -> {'code': 'name'}:
		return await self._request(endpoint="currencies", date=date)


	async def get_values_based_on(self, currency_code: str, date: Optional[str] = "latest") -> Dict[str, Union[str, Dict[str, int]]]:
		return (await self._request(endpoint=f"currencies/{currency_code}", date=date))[currency_code]

	async def convert(self, currency_from: str, currency_to: str, date: Optional[str] = "latest") -> int:
		return (await self._request(endpoint=f"currencies/{currency_from}/{currency_to}", date=date))[currency_to]