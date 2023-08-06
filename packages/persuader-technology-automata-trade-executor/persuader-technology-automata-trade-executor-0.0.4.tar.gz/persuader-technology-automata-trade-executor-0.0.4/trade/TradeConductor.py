import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.trade.InstrumentTrade import InstrumentTrade, Status

from trade.executor.TradeExecutor import TradeExecutor
from trade.serialize.trade_deserializer import deserialize_trade
from trade.serialize.trade_serializer import serialize_trade


class TradeConductor:

    def __init__(self, options, trade_executor: TradeExecutor):
        self.options = options
        self.cache = RedisCacheHolder()
        self.trade_executor = trade_executor

    def build_trade_key(self):
        return self.options['TRADE_KEY']

    def store_trade_to_execute(self, trade: InstrumentTrade):
        trade_key = self.build_trade_key()
        trade_to_store = serialize_trade(trade)
        self.cache.store(trade_key, trade_to_store)

    def fetch_trade_to_execute(self) -> InstrumentTrade:
        trade_key = self.build_trade_key()
        raw_trade = self.cache.fetch(trade_key, as_type=dict)
        return deserialize_trade(raw_trade)

    def perform_trade(self):
        trade = self.fetch_trade_to_execute()
        if trade.status == Status.NEW:
            updated_trade = self.trade_executor.trade(trade)
            self.store_trade_to_execute(updated_trade)
        else:
            logging.warning(f'Trade is not new, so will not trade -> {trade}')
