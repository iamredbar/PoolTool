# by Christopher Sanborn
import tkinter as tk
from tkinter import ttk
import math
import numpy as numpy
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bitshares import BitShares
from bitshares.amount import Amount
from bitshares.asset import Asset


matplotlib.use("TkAgg")

class DepthData():

    def __init__(self):
        self.dirty=True

    def update_blockchain_data(self, blockchain_data):
        self.dirty = True
        self.pool = blockchain_data['pool']
        self.amount_x = self.pool.amount_x()
        self.amount_y = self.pool.amount_y()
        self.bids = self.pool.market_bids()
        self.asks = self.pool.market_asks()

    def get_pool_price(self):
        return self.pool.price()

    def get_pool_buys(self, p_min, p_max):
        p_pool = self.get_pool_price()
        p_min = p_min if p_min > 0 else (p_max-p_min)/1e6
        p_max = min(p_max, p_pool)
        prices = numpy.linspace(p_min,p_max,100) if p_min<p_max else []
        depth = [self.amount_y*(math.sqrt(p_pool/p) - 1) for p in prices]
        return {
            'x':prices,
            'y':depth
        }

    def get_pool_sells(self, p_min, p_max):
        p_pool = self.get_pool_price()
        p_min = max(p_min, p_pool)
        prices = numpy.linspace(p_min,p_max,100) if p_min<p_max else []
        depth = [self.amount_y*(1-math.sqrt(p_pool/p)) for p in prices]
        return {
            'x':prices,
            'y':depth
        }

    def get_book_buys(self, p_min, p_max):
        x = []
        y = []
        cum = 0
        for pr in self.bids:
            price = pr.price
            if price >= p_min:
                previous = cum
                cum  = cum + pr['quote']['amount']
                x.extend([price, price])
                y.extend([previous, cum])
        if cum > 0:
            x.append(p_min)
            y.append(cum)
        return {
            'x':x,
            'y':y
        }

    def get_book_sells(self, p_min, p_max):
        x = []
        y = []
        cum = 0
        for pr in self.asks:
            price = pr.price
            if price <= p_max:
                previous = cum
                cum  = cum + pr['quote']['amount']
                x.extend([price, price])
                y.extend([previous, cum])
        if cum > 0:
            x.append(p_max)
            y.append(cum)
        return {
            'x':x,
            'y':y
        }


class DepthChart(tk.Frame):

    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.data = DepthData()
        self.fig = None
        self.canvas = None

    def update_blockchain_data(self, blockchain_data):
        self.data.update_blockchain_data(blockchain_data)
        pool_price = self.data.get_pool_price()
        prices = []
        prices.extend([pr.price for pr in blockchain_data['market_orderbook']['asks']])
        self.pricewindow = [pool_price*(1/2),
                            pool_price*(3/2)]
        self.draw()

    def draw(self):

        pool_sell_curve = self.data.get_pool_sells(*self.pricewindow)
        pool_buy_curve = self.data.get_pool_buys(*self.pricewindow)
        book_sell_curve = self.data.get_book_sells(*self.pricewindow)
        book_buy_curve = self.data.get_book_buys(*self.pricewindow)

        if self.fig is None:
            self.fig = Figure(figsize=(7,4.5))
        self.fig.clf()
        self.fig.patch.set_facecolor("burlywood")
        a = self.fig.gca()
        a.set_facecolor("ghostwhite")

        attr = {
            "book": {
                "buy": {
                    "line": {
                        "color": "darkgreen",
                    },
                    "area": {
                        "color": "darkgreen",
                        "alpha": 0.25,
                    },
                },
                "sell": {
                    "line": {
                        "color": "darkred",
                    },
                    "area": {
                        "color": "darkred",
                        "alpha": 0.25,
                    },
                },
            },
            "pool": {
                "buy": {
                    "line": {
                        "color": "green",
                    },
                    "area": {
                        "color": "green",
                        "alpha": 0.25,
                    },
                },
                "sell": {
                    "line": {
                        "color": "red",
                    },
                    "area": {
                        "color": "red",
                        "alpha": 0.25,
                    },
                },
            },
        }

        a.plot(pool_sell_curve['x'], pool_sell_curve['y'], **attr['pool']['sell']['line'])
        a.plot(pool_buy_curve['x'], pool_buy_curve['y'], **attr['pool']['buy']['line'])
        a.fill_between(pool_sell_curve['x'], pool_sell_curve['y'], **attr['pool']['sell']['area'])
        a.fill_between(pool_buy_curve['x'], pool_buy_curve['y'], **attr['pool']['buy']['area'])

        a.plot(book_sell_curve['x'], book_sell_curve['y'], **attr['book']['sell']['line'])
        a.plot(book_buy_curve['x'], book_buy_curve['y'], **attr['book']['buy']['line'])
        a.fill_between(book_sell_curve['x'], book_sell_curve['y'], **attr['book']['sell']['area'])
        a.fill_between(book_buy_curve['x'], book_buy_curve['y'], **attr['book']['buy']['area'])

        a.set_xlim(self.pricewindow)
        a.set_ylim(bottom=0)
        a.ticklabel_format(style='plain')

        a.set_title(self.data.pool.market().get_string(separator=":"), loc="left")
        a.set_ylabel("Depth (%s)"%(self.data.pool.asset_y()['symbol']))
        a.set_xlabel("Price (%s/%s)"%(self.data.pool.asset_x()['symbol'],
                                      self.data.pool.asset_y()['symbol']))

        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, self)
            self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas.draw()
