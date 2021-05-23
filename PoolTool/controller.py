from PoolTool.view import PoolTool
from PoolTool.model import Model
from pubsub import pub


class Controller:
    def __init__(self):
        # initiate model and view so that controller can talk
        self.model = Model()
        self.view = PoolTool()
        # subscribe and respond to actions
        pub.subscribe(self.pool_change, 'pool_change')
        pub.subscribe(self.update_pool_change, 'update_pool_change')
        pub.subscribe(self.update_pool_price, 'update_pool_price')
        pub.subscribe(self.update_pool_estimate, 'update_pool_estimate')
        pub.subscribe(self.get_pools, 'get_pools')
        pub.subscribe(self.return_pool_list, 'return_pool_list')
        pub.subscribe(self.swap_assets, 'swap_assets')
        pub.subscribe(self.deposit_assets, 'deposit_assets')
        pub.subscribe(self.withdraw_assets, 'withdraw_assets')
        pub.subscribe(self.interaction_return, 'interaction_return')
        pub.subscribe(self.set_denomination, 'set_denomination')
        pub.subscribe(self.price_swap, 'price_swap')
        pub.subscribe(self.refresh_history_panel, 'refresh_history_panel')
        pub.subscribe(self.refresh_stats_panel, 'refresh_stats_panel')

    def pool_change(self, data):
        self.model.pool_change(data)

    def update_pool_change(self, data):
        self.view.update_pool_change(data)

    def update_pool_price(self, data):
        self.model.update_pool_price(data)

    def update_pool_estimate(self, data):
        self.view.update_pool_estimate(data)

    def get_pools(self, data):
        self.model.get_pools(data)

    def return_pool_list(self, data):
        self.view.return_pool_list(data)

    def swap_assets(self, data):
        self.model.swap_assets(data)

    def deposit_assets(self, data):
        self.model.deposit_assets(data)

    def withdraw_assets(self, data):
        self.model.withdraw_assets(data)

    def interaction_return(self, data):
        self.view.interaction_return(data)

    def set_denomination(self, data):
        self.model.set_denomination(data)

    def price_swap(self):
        self.model.price_swap()

    def refresh_history_panel(self, data):
        self.view.generate_history_panel(data)

    def refresh_stats_panel(self, data):
        self.view.generate_stats_panel(data)


def main():
    c = Controller()
    c.view.run()
