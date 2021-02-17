from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from pubsub import pub

Window.size = (400, 650)


class CustomToolbar(ThemableBehavior, RectangularElevationBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CustomListItem(MDGridLayout):
    asset_a = StringProperty()
    icon = StringProperty()
    asset_b = StringProperty()


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


class PoolTool(MDApp):
    """

    """

    def __init__(self, **kwargs):
        # self.icon = 'assets/pool_tool.png'
        super().__init__(**kwargs)
        self.view_pools = []
        self.screen = Builder.load_file('app/layout.kv')
        self.pool_dropdown = []
        self.interact_popup = None
        self.interact_data = None
        self.settings_popup = None
        self.account = ''
        self.key = ''
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

    def get_pools(self):
        pub.sendMessage('get_pools')

    def return_pool_list(self, data):
        self.screen.pool_select_spinner.values = data

    def build(self):
        self.get_pools()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'LightGreen'
        self.theme_cls.accent_palette = 'Red'
        self.use_kivy_settings = False
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
            )
        self.settings_popup.open()

    def save_settings(self, account, key):
        self.account = account
        self.key = key
        self._clear_settings()

    def _clear_settings(self):
        if self.settings_popup:
            self.settings_popup.dismiss(force=True)
            self.settings_popup = None

    def pool_change(self, new_pool):
        pub.sendMessage('pool_change', data=new_pool)

    def update_pool_change(self, data):
        self._clear_gui()
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
        self.screen.value_label.text = f'${data["value"]:,.2f}'
        self.screen.swap_count.text = str(data['swap_count'])
        self.screen.swap_fee.text = data['swap_fee']
        self.screen.withdraw_fee.text = data['withdraw_fee']
        self.screen.poolshare_value.text = f'${data["poolshare_value"]:,.2f}\nper share'
        self.screen.asset_a_balance.text = f'{data["asset_a_balance"]}\n{data["asset_a_symbol"]}'
        self.screen.asset_b_balance.text = f'{data["asset_b_balance"]}\n{data["asset_b_symbol"]}'
        for op in data['history']:
            self.screen.history_list.add_widget(
                CustomListItem(
                    asset_a=op['asset_a'],
                    icon=op['icon'],
                    asset_b=op['asset_b']
                )
            )

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

    def update_pool_estimate(self, amount):
        self.screen.swap_estimate.text = amount
        self.screen.swap_button.disabled = False

    def _swap_assets(self, data):
        pub.sendMessage('swap_assets', data=data)
        self._clear_popup()

    def _deposit_assets(self, data):
        pub.sendMessage('deposit_assets', data=data)
        self._clear_popup()

    def _withdraw_assets(self, data):
        pub.sendMessage('withdraw_assets', data=data)
        self._clear_popup()

    def _clear_popup(self):
        if self.interact_popup:
            self.interact_popup.dismiss(force=True)
            self.interact_popup = None
            self.interact_data = None

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
            self._clear_popup()
            popup = ReturnPopup(
                titletext='Invalid Account Settings',
                bodytext='Please check account\ninformation in\nthe settings',
            )
            popup.open()

    def interaction_return(self, data):
        if data['interaction_type'] == 'swap':
            titletext = 'Swap Complete'
            bodytext = f'Paid {data["paid"]} for {data["received"]}\n(anticipated {data["anticipated"]})'
        elif data['interaction_type'] == 'deposit':
            pass
        elif data['interaction_type'] == 'withdraw':
            pass
        popup = ReturnPopup(
            titletext=titletext,
            bodytext=bodytext,
        )
        popup.open()
