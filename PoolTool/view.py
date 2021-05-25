import platform
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from pubsub import pub

Window.size = (400, 650)

# Fix bug where Windows does not see OpenGL 2.0
if platform.system() == 'Windows':
    from kivy import Config
    import os
    Config.set('graphics', 'multisamples', '0')
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

class CustomToolbar(ThemableBehavior, RectangularElevationBehavior, MDBoxLayout):
    pass


class CustomListItem(MDGridLayout):
    asset_a = StringProperty()
    icon = StringProperty()
    asset_b = StringProperty()
    price = StringProperty()
    price_color = ColorProperty()


class LoadingPoolsPopup(Popup):
    pass


class InteractPopup(Popup):
    titletext = StringProperty()
    bodytext = StringProperty()
    confirmbutton = StringProperty()
    data = None


class ReturnPopup(Popup):
    titletext = StringProperty()
    bodytext = StringProperty()


class SettingsPopup(Popup):
    account = StringProperty()
    key = StringProperty()
    node = StringProperty()
    denomination = StringProperty()


class LoadingPoolInfo(Popup):
    bodytext = StringProperty()


class PoolTool(MDApp):
    """

    """

    def __init__(self, **kwargs):
        self.icon = 'PoolTool/assets/icon.jpg'
        super().__init__(**kwargs)
        self.view_pools = []
        self.screen = Builder.load_file('PoolTool/layout.kv')
        self.pool_dropdown = []
        self.interact_popup = None
        self.interact_data = None
        self.settings_popup = None
        self.loading_pools_popup = None
        self.loading_pool_info = None
        self.account = ''
        self.key = ''
        self.node = 'wss://api.iamredbar.com/ws'  # default in settings
        self.denomination = 'BitUSD'  # default in settings
        self.screen.pool_select_spinner.text = 'Select Pool Here'
        self._init_gui()

    def _init_gui(self):
        self.screen.amount_text_field.text = ''
        self.screen.swap_asset_button.text = 'Asset A'
        self.screen.swap_estimate.text = 'Receive (estimate)'
        self.screen.other_asset.text = 'Asset B'
        self.screen.deposit_a_text_field.text = ''
        self.screen.deposit_asset_a.text = 'Asset A'
        self.screen.deposit_b_text_field.text = ''
        self.screen.deposit_asset_b.text = 'Asset B'
        self.screen.withdraw_text_field.text = ''
        self.screen.withdraw_share_asset_label.text = 'Share Asset'
        self.screen.pool_share_balance.text = '(Share Balance)'
        self.screen.pool_share_bal_label.text = 'Share Asset'

    def _clear_gui(self):
        self.screen.amount_text_field.text = ''
        self.screen.swap_asset_button.text = ''
        self.screen.swap_estimate.text = 'Receive (estimate)'
        self.screen.other_asset.text = ''
        self.screen.deposit_a_text_field.text = ''
        self.screen.deposit_asset_a.text = ''
        self.screen.deposit_b_text_field.text = ''
        self.screen.deposit_asset_b.text = ''
        self.screen.withdraw_text_field.text = ''
        self.screen.withdraw_share_asset_label.text = ''
        self.screen.pool_share_balance.text = ''
        self.screen.pool_share_bal_label.text = ''
        self.screen.history_list.clear_widgets()

    def get_pools(self, caller):
        if not self.screen.pool_select_spinner.values or caller != 'spinner':
            if self.loading_pools_popup:
                self.loading_pools_popup = None
            if not self.loading_pools_popup:
                self.loading_pools_popup = LoadingPoolsPopup()
            self.loading_pools_popup.open()
            data = {
                'node': self.node,
                'denomination': self.denomination,
            }
            Clock.schedule_once(lambda dt: pub.sendMessage('get_pools', data=data), 0.2)

    def pool_change(self, new_pool):
        if new_pool != 'Select Pool Here':
            if self.loading_pool_info:
                self.loading_pool_info = None
            if not self.loading_pool_info:
                temp = f'loading\n{new_pool.split(" ")[0]}\ninfo...'
                self.loading_pool_info = LoadingPoolInfo(bodytext=temp)
            self.loading_pool_info.open()
            Clock.schedule_once(lambda dt: pub.sendMessage(topicName='pool_change', data=new_pool))

    def refresh_stats_panel(self, data):
        pass

    def return_pool_list(self, data):
        self._clear_popups()
        self.screen.pool_select_spinner.values = data

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'LightGreen'
        self.theme_cls.accent_palette = 'Red'
        self.use_kivy_settings = False
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        return self.screen

    """
    These are functions that are triggered by the GUI
    """
    def _open_settings(self):
        if self.settings_popup:
            self.settings_popup = None
        if not self.settings_popup:
            self.settings_popup = SettingsPopup(
                account=self.account,
                key=self.key,
                node=self.node,
                denomination=self.denomination,
            )
        self.settings_popup.open()

    def save_settings(self, account, key, node, denomination):
        self.account = account
        self.key = key
        self.node = node
        self.denomination = denomination
        pub.sendMessage('set_denomination', data=denomination)
        self._clear_popups()

    def _clear_popups(self):
        if self.settings_popup:
            self.settings_popup.dismiss(force=True)
            self.settings_popup = None
        if self.loading_pools_popup:
            self.loading_pools_popup.dismiss(force=True)
            self.loading_pools_popup = None
        if self.interact_popup:
            self.interact_popup.dismiss(force=True)
            self.interact_popup = None
            self.interact_data = None
        if self.loading_pool_info:
            self.loading_pool_info.dismiss(force=True)
            self.loading_pool_info = None

    def update_pool_change(self, data):
        self._clear_gui()
        self._clear_popups()
        self.screen.swap_card.disabled = False
        self.screen.deposit_card.disabled = False
        self.screen.withdraw_card.disabled = False
        self.screen.swap_asset_button.text = data['asset_a_symbol']
        self.screen.other_asset.text = data['asset_b_symbol']
        self.screen.deposit_asset_a.text = data['asset_a_symbol']
        self.screen.deposit_asset_b.text = data['asset_b_symbol']
        self.screen.pool_share_balance.text = data['share_asset_balance']
        self.screen.pool_share_bal_label.text = data['share_asset_symbol']
        self.screen.withdraw_share_asset_label.text = data['share_asset_symbol']
        self.screen.value_label.text = f'{data["value"]}'
        self.screen.swap_count.text = str(data['swap_count']) if data['swap_count'] < 100 else '100+'
        self.screen.swap_fee.text = data['swap_fee']
        self.screen.withdraw_fee.text = data['withdraw_fee']
        self.screen.poolshare_value.text = f'{data["poolshare_value"]}\nper share'
        self.screen.asset_a_balance.text = f'{data["asset_a_balance"]}\n{data["asset_a_symbol"]}'
        self.screen.asset_b_balance.text = f'{data["asset_b_balance"]}\n{data["asset_b_symbol"]}'
        self.generate_history_panel(data['history'])

    def generate_history_panel(self, history):
        # print(self.screen.history_list.children)
        # self.screen.history_list.clear_widgets()
        # try:
        #     for child in self.screen.history_list.children:
        #         print(child)
        #         self.screen.history_list.remove_widget(child)
        # except:
        #     print('no children')
        for op in history:
            self.screen.history_list.add_widget(
                CustomListItem(
                    asset_a=op['asset_a'],
                    icon=op['icon'],
                    price=op['price'],
                    price_color=op['price_color'],
                    asset_b=op['asset_b'],
                )
            )
        # print(self.screen.history_list.children)

    def generate_stats_panel(self, data):
        self.screen.value_label.text = f'{data["value"]}'
        self.screen.poolshare_value.text = f'{data["poolshare_value"]}\nper share'

    def _interchange_assets_swap(self):
        tmp_a = self.screen.swap_asset_button.text
        tmp_b = self.screen.other_asset.text
        self.screen.swap_asset_button.text = tmp_b
        self.screen.other_asset.text = tmp_a
        self.screen.amount_text_field.text = ''
        self.screen.swap_button.disabled = True
        self.screen.swap_estimate.text = 'Receive (estimate)'

    def update_pool_price(self, amount):
        send_data = {
            'amount': amount,
            'swap_asset': self.screen.swap_asset_button.text,
            'purchase_asset': self.screen.other_asset.text
        }
        pub.sendMessage('update_pool_price', data=send_data)

    def price_swap(self, sender):
        if sender == 'price_switch':
            pub.sendMessage('price_swap')

    def update_pool_estimate(self, amount):
        self.screen.swap_estimate.text = amount
        self.screen.swap_button.disabled = False

    def _swap_assets(self, data):
        pub.sendMessage('swap_assets', data=data)
        self._clear_popups()

    def _deposit_assets(self, data):
        pub.sendMessage('deposit_assets', data=data)
        self._clear_popups()

    def _withdraw_assets(self, data):
        pub.sendMessage('withdraw_assets', data=data)
        self._clear_popups()

    def interact(self, btn_text):
        if btn_text == 'SWAP':
            data = {
                'sell_asset': self.screen.swap_asset_button.text,
                'sell_amount': self.screen.amount_text_field.text,
                'receive_asset': self.screen.other_asset.text,
                'receive_approx_amount': self.screen.swap_estimate.text,
            }
            titletext = 'Verify Swap'
            bodytext = f'Swap\n{data["sell_amount"]} {data["sell_asset"]}\nfor approximately\n{data["receive_approx_amount"]} {data["receive_asset"]}?'
            confirmbutton = 'SWAP'
        elif btn_text == 'DEPOSIT':
            data = {
                'asset_a': self.screen.deposit_asset_a.text,
                'amount_a': self.screen.deposit_a_text_field.text,
                'asset_b': self.screen.deposit_asset_b.text,
                'amount_b': self.screen.deposit_b_text_field.text,
            }
            titletext = 'Verify Deposit'
            bodytext = f'Deposit:\n{data["amount_a"]} {data["asset_a"]}\n{data["amount_b"]} {data["asset_b"]}\nfor\n{self.screen.withdraw_share_asset_label.text}?'
            confirmbutton = 'DEPOSIT'
        elif btn_text == 'WITHDRAW':
            data = {
                'share_asset': self.screen.withdraw_share_asset_label.text,
                'amount': self.screen.withdraw_text_field.text,
                'asset_a': self.screen.deposit_asset_a.text,
                'asset_b': self.screen.deposit_asset_b.text,
            }
            titletext = 'Verify Withdraw'
            bodytext = f'Withdraw:\n{data["amount"]} {data["share_asset"]}\nfor\n{data["asset_a"]} and {data["asset_b"]}?'
            confirmbutton = 'WITHDRAW'
        else:
            data = {}
            titletext = ''
            bodytext = ''
            confirmbutton = ''
        self.interact_data = data
        if self.interact_popup:
            self.interact_popup = None
        if not self.interact_popup:
            self.interact_popup = InteractPopup(
                titletext=titletext,
                bodytext=bodytext,
                confirmbutton=confirmbutton,
            )
        self.interact_popup.open()

    def _confirm_interaction(self, interaction):
        # verify that account and key have been specified
        if self.account and self.key:
            self.interact_data['account'] = self.account
            self.interact_data['key'] = self.key
            if interaction == 'SWAP':
                self._swap_assets(self.interact_data)
            elif interaction == 'DEPOSIT':
                self._deposit_assets(self.interact_data)
            elif interaction == 'WITHDRAW':
                self._withdraw_assets(self.interact_data)
        else:  # they haven't entered an account or key
            self._clear_popups()
            popup = ReturnPopup(
                titletext='Invalid Account Settings',
                bodytext='Please check account\ninformation in\nthe settings',
            )
            popup.open()

    def interaction_return(self, data):
        if data['interaction_type'] == 'swap':
            titletext = 'Swap Complete'
            bodytext = f'Paid {data["paid"]}\nfor {data["received"]}\n(anticipated {data["anticipated"]})'
        elif data['interaction_type'] == 'deposit':
            titletext = 'Deposit Complete'
            bodytext = f'Deposited {data["paid_a"]}\nand {data["paid_b"]}\nfor {data["received"]}'
        elif data['interaction_type'] == 'withdraw':
            titletext = 'Withdraw Complete'
            bodytext = f'Exchanged {data["exchanged"]}\nfor {data["received_a"]}\nand {data["received_b"]}'
        else:
            titletext = 'Oops'
            bodytext = 'You shouldn\'t ever see this...'
        popup = ReturnPopup(
            titletext=titletext,
            bodytext=bodytext,
        )
        popup.open()
