# by Christopher Sanborn
import math
import numpy
from bitshares import BitShares
from bitshares.amount import Amount
from bitshares.asset import Asset
from bitshares.market import Market
from bitshares.price import Order

from bitshares.instance import BlockchainInstance

@BlockchainInstance.inject
class Pool(dict):

    def __init__(self, *args, invert=False, **kwargs):
        self.invert = invert
        pool = kwargs.pop("pool", None)
        if pool is None and len(args) == 1:
            pool = args[0]
        pool_id = self.blockchain._find_liquidity_pool(pool)
        pool_obj = self.blockchain.rpc.get_object(pool_id)
        data = {
            "id": pool_id,
            "object": pool_obj, # raw object here
            # interpretted fields t.b.d. here by _populate method
        }
        dict.__init__(self, data)
        self._populate()

    def __str__(self):
        return "<pool %s:%s (%s)> balances %s, %s"%(
            self["asset_b"]["symbol"],
            self["asset_a"]["symbol"],
            self["id"],
            self["amount_a"],
            self["amount_b"],
        )

    def _populate(self):
        self.update({
            "asset_a": Asset(self["object"]["asset_a"]),
            "asset_b": Asset(self["object"]["asset_b"]),
            "share_asset": Asset(self["object"]["share_asset"]),
            "taker_fee": int(self["object"]["taker_fee_percent"]) / 10000,
        })
        share_ddo = self.blockchain.rpc.get_object(self["share_asset"]["dynamic_asset_data_id"])
        self.update({
            "amount_a": Amount(int(self["object"]["balance_a"])/10**self["asset_a"].precision, self["asset_a"]),
            "amount_b": Amount(int(self["object"]["balance_b"])/10**self["asset_b"].precision, self["asset_b"]),
        })

    def price(self):
        """ Return nominal price to buy asset_b paying asset_a, unless
            invert then flip.  Return type: float (not a Price object).

        """
        return (
            self['amount_a']['amount'] / self['amount_b']['amount']
            if not self.invert else
            self['amount_b']['amount'] / self['amount_a']['amount']
        )

    def asset_x(self):
        return (self['asset_a'] if not self.invert else self['asset_b'])

    def asset_y(self):
        return (self['asset_b'] if not self.invert else self['asset_a'])

    def amount_x(self):
        return (
            self['amount_a']['amount'] if not self.invert
            else self['amount_b']['amount']
        )

    def amount_y(self):
        return (
            self['amount_b']['amount'] if not self.invert
            else self['amount_a']['amount']
        )

    def market(self):
        return Market(**(
            {"base":self['asset_a'],"quote":self['asset_b']} if not self.invert
            else {"base":self['asset_b'],"quote":self['asset_a']}
        ))

    def market_asks(self):
        limits = self.market().get_limit_orders(300)
        asks = []
        for lim in limits:
            if lim['for_sale']['asset'] == self.asset_y():
                order = Order(
                    1.0/lim['price'],
                    quote = lim['for_sale'],
                    base =  Amount(lim['for_sale']['amount']/lim['price'], self.asset_x())
                )
                asks.append(order)
        return sorted(asks, key = lambda k: k['price'])

    def market_bids(self):
        limits = self.market().get_limit_orders(300)
        bids = []
        for lim in limits:
            if lim['for_sale']['asset'] == self.asset_x():
                order = Order(
                    1.0/lim['price'],
                    base = lim['for_sale'],
                    quote =  Amount(lim['for_sale']['amount']/lim['price'], self.asset_y())
                )
                bids.append(order)
        return sorted(bids, key = lambda k: k['price'], reverse=True)
