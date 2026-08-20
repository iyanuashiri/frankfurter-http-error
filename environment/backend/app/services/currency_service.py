from frankfurter.rest_adapter import RestAdapter


frankfurter = RestAdapter()


class Currency:
    def __init__(self):
        self.client = frankfurter

    async def get_currencies(self):
        return await self.client.get_currencies()

    async def convert(self, base_currency: str, target_currency: str):
        return await self.client.get_currency_rates(base_currency=base_currency, 
                                                    target_currency=target_currency)

    async def historical(self, date: str, base_currency: str, target_currency: str):
        return await self.client.get_historical_currency_rates(
            date=date, base_currency=base_currency, target_currency=target_currency)