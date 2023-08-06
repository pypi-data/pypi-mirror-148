from core.oracle.Prediction import Prediction
from exchange.rate.ExchangeRateHolder import ExchangeRateHolder


class Oracle:

    def set_exchange_rates(self, exchange_rates: ExchangeRateHolder):
        pass

    def predict(self, instrument) -> Prediction:
        pass
