from view import View
from model import Model
import tkinter as tk
from pubsub import pub

class Controller:
    def __init__(self, window):
        #variables
        self.window = window
        self.model = Model()
        self.view = View(self.window)
        self.view.setup(self.model.settings)

        pub.subscribe(self.pool_change_requested, 'pool_change_requested')
        pub.subscribe(self.update_prices, 'update_prices')
        pub.subscribe(self.take_offer, 'take_offer')
        pub.subscribe(self.quit_program_requested, 'quit_program_requested')

        pub.subscribe(self.update_gui, 'update_gui')
        pub.subscribe(self.update_trading_prices, 'update_trading_prices')
        pub.subscribe(self.print_transaction, 'print_transaction')

    def print_transaction(self, data):
        self.view.print_transaction(data)

    def update_trading_prices(self, data):
        self.view.update_trading_prices(data)


    def update_gui(self, data):
        self.view.update_gui(data)

    def update_prices(self, data):
        self.model.update_prices(data)

    def pool_change_requested(self, data):
        self.model.pool_change(data)


    def take_offer(self, data):
        self.model.take_offer(data)

    def quit_program_requested(self):
        self.model.quit_program()

if __name__ == '__main__':
    window = tk.Tk()
    window.title('PoolTool')
    window.resizable(False, False)
    window.columnconfigure([1,2], weight=1)

    app = Controller(window)
    window.mainloop()
