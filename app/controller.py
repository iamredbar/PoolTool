from app.view import PoolTool
from app.model import Model
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

    def pool_change(self, data):
        self.model.pool_change(data)

    def update_pool_change(self, data):
        self.view.update_pool_change(data)

    def update_pool_price(self, data):
        self.model.update_pool_price(data)

    def update_pool_estimate(self, data):
        self.view.update_pool_estimate(data)

    def get_pools(self):
        self.model.get_pools()

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
