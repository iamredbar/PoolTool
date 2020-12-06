import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from pubsub import pub
from depthchart import DepthChart

class View:
    def __init__(self, window):
        # initialize variables
        self.window = window

    def setup(self, settings):
        #calls methods to setup the ui
        self.get_string_var()
        self.assign_string_var()
        self.create_widgets()
        self.set_dropdown_values(settings)
        self.create_menu()
        self.setup_layout()

    def create_widgets(self):
        # frames
        self.frame_pool_info = tk.Frame(
            self.window,
        )
        self.frame_market_info = tk.Frame(
            self.window,
        )
        self.frame_depthchart = DepthChart(
            self.window,
            None,
            height=100,
        )
        self.frame_pooltool_helper = tk.Frame(
            self.window,
            #background='#c9c9c9',
        )
        self.frame_deposit = tk.Frame(
            self.window,
            background='#c9c9c9',
        )
        self.frame_deposit_upper = tk.Frame(
            self.frame_deposit,
        )
        self.frame_deposit_lower = tk.Frame(
            self.frame_deposit
        )

        # pool info widgets
        self.lbl_pool_id = tk.Label(self.frame_pool_info)
        self.lbl_pool_id['textvariable'] = self.string_var['sv_lbl_pool_id']
        self.cmb_pool_id = ttk.Combobox(self.frame_pool_info)
        self.cmb_pool_id.state(statespec=['readonly'])
        self.cmb_pool_id.bind('<<ComboboxSelected>>', self.change_pool)
        self.lbl_pool_name = tk.Label(self.frame_pool_info)
        self.lbl_pool_name['textvariable'] = self.string_var['sv_lbl_pool_name']
        self.lbl_pool_balance_a = tk.Label(self.frame_pool_info)
        self.lbl_pool_balance_a['textvariable'] = self.string_var['sv_lbl_pool_balance_a']
        self.lbl_pool_balance_b = tk.Label(self.frame_pool_info)
        self.lbl_pool_balance_b['textvariable'] = self.string_var['sv_lbl_pool_balance_b']
        self.lbl_pool_invariant = tk.Label(self.frame_pool_info)
        self.lbl_pool_invariant['textvariable'] = self.string_var['sv_lbl_pool_invariant']
        self.lbl_pool_price_ab = tk.Label(self.frame_pool_info)
        self.lbl_pool_price_ab['textvariable'] = self.string_var['sv_lbl_pool_price_ab']
        self.lbl_pool_price_ba = tk.Label(self.frame_pool_info)
        self.lbl_pool_price_ba['textvariable'] = self.string_var['sv_lbl_pool_price_ba']
        
        # market info widgets
        self.lbl_assets = tk.Label(self.frame_market_info)
        self.lbl_assets['textvariable'] = self.string_var['sv_lbl_assets']
        self.lbl_market_percentage_change = tk.Label(self.frame_market_info)
        self.lbl_market_percentage_change['textvariable'] = self.string_var['sv_lbl_market_percentage_change']
        self.lbl_latest_price = tk.Label(self.frame_market_info)
        self.lbl_latest_price['textvariable'] = self.string_var['sv_lbl_latest_price']
        self.lbl_highest_bid = tk.Label(self.frame_market_info, bg=self.palette('green'))
        self.lbl_highest_bid['textvariable'] = self.string_var['sv_lbl_highest_bid']
        self.lbl_lowest_ask = tk.Label(self.frame_market_info, bg=self.palette('red'))
        self.lbl_lowest_ask['textvariable'] = self.string_var['sv_lbl_lowest_ask']
        self.lbl_market_base_volume = tk.Label(self.frame_market_info)
        self.lbl_market_base_volume['textvariable'] = self.string_var['sv_lbl_market_base_volume']
        self.lbl_market_quote_volume = tk.Label(self.frame_market_info)
        self.lbl_market_quote_volume['textvariable'] = self.string_var['sv_lbl_market_quote_volume']

        # pooltool helper widgets
        self.rd_buy = ttk.Radiobutton(
            self.frame_pooltool_helper,
            text='Buy',
            variable=self.string_var['rd_buy_sell'],
            value='buy',
            state='disabled',
        )
        self.rd_sell = ttk.Radiobutton(
            self.frame_pooltool_helper,
            text='Sell',
            variable=self.string_var['rd_buy_sell'],
            value='sell',
            state='disabled',
        )
        self.lbl_trade_amount = tk.Label(
            self.frame_pooltool_helper,
            text='Amount:',
        )
        self.ent_trade_amount = tk.Entry(
            self.frame_pooltool_helper,
            width=10,
            state='disabled',
        )
        self.ls_assets = tk.Listbox(
            self.frame_pooltool_helper,
            listvariable = self.string_var['ls_assets'],
            height=2,
            width=10,
            state='disabled',
        )
        self.ls_assets.bind('<<ListboxSelect>>',self.change_asset)
        self.rd_use_market = ttk.Radiobutton(
            self.frame_pooltool_helper,
            text='Use Market =',
            variable=self.string_var['rd_market_or_pool'],
            value='market',
            state='disabled'
        )
        self.rd_use_pool = ttk.Radiobutton(
            self.frame_pooltool_helper,
            text='Use Pool =',
            variable=self.string_var['rd_market_or_pool'],
            value='pool',
            state='disabled',
        )
        self.lbl_helper_market_price = tk.Label(
            self.frame_pooltool_helper,
            textvariable=self.string_var['lbl_helper_market_price']
        )
        self.lbl_helper_pool_price = tk.Label(
            self.frame_pooltool_helper,
            textvariable=self.string_var['lbl_helper_pool_price']
        )
        self.btn_update_trade_prices = ttk.Button(
            self.frame_pooltool_helper,
            text='Update Prices',
            command=self.update_prices,
            state='disabled',
        )
        self.btn_take_offer = ttk.Button(
            self.frame_pooltool_helper,
            text='Take Offer',
            command=self.take_offer,
            state='disabled',
        )

        # deposit widgets
        self.ent_assetx_amount = tk.Entry(
            self.frame_deposit_upper,
            width=10,
            state='disabled',
            justify='right',
        )
        self.ent_assety_amount = tk.Entry(
            self.frame_deposit_upper,
            width=10,
            state='disabled',
            justify='right',
        )
        self.lbl_assetx_deposit = tk.Label(
            self.frame_deposit_upper,
            textvariable=self.string_var['lbl_assetx_deposit']
        )
        self.lbl_assety_deposit = tk.Label(
            self.frame_deposit_upper,
            textvariable=self.string_var['lbl_assety_deposit']
        )
        self.btn_check_deposit = ttk.Button(
            self.frame_deposit_upper,
            text='Estimate Coming Soon',
            command=self.update_shares,
            state='disabled',
        )
        self.btn_deposit = ttk.Button(
            self.frame_deposit_upper,
            text='Deposit to LP',
            command=self.deposit_to_lp,
            state='disabled',
        )
        self.lbl_poolshare_deposit = tk.Label(
            self.frame_deposit_lower,
            textvariable=self.string_var['lbl_poolshare_deposit'],
        )
        self.lbl_poolshare_symbol = tk.Label(
            self.frame_deposit_lower,
            textvariable=self.string_var['lbl_poolshare_symbol']
        )

    def create_menu(self):
        menubar = tk.Menu(self.window)
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label='Quit', command=self.quit_program)
        menubar.add_cascade(label='File', menu=menu_file)
        self.window.config(menu=menubar)
        self.window.config

    def setup_layout(self):
        # frames
        self.frame_pool_info.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nw')
        self.frame_market_info.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky='ne')
        self.frame_depthchart.grid(row=1, column=0, columnspan=4, padx=5, pady=5, stick='ew')
        self.frame_pooltool_helper.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        self.frame_deposit.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        self.frame_deposit_upper.grid(row=0, column=0, padx=5, pady=5)
        self.frame_deposit_lower.grid(row=1, column=0, padx=5, pady=5)
       
        # pool info
        self.lbl_pool_id.grid(row=0, column=0, padx=5, sticky='w')
        self.cmb_pool_id.grid(row=0, column=0, padx=5, sticky='e')
        self.lbl_pool_name.grid(row=1, column=0, padx=5, sticky='w')
        self.lbl_pool_balance_a.grid(row=2, column=0, padx=5, sticky='w')
        self.lbl_pool_balance_b.grid(row=3, column=0, padx=5, sticky='w')
        self.lbl_pool_price_ab.grid(row=5, column=0, padx=5, sticky='w')
        self.lbl_pool_price_ba.grid(row=6, column=0, padx=5, sticky='w')

        # market info
        self.lbl_assets.grid(row=0, column=0, padx=5, sticky='e')
        self.lbl_latest_price.grid(row=3, column=0, padx=5, sticky='e')
        self.lbl_highest_bid.grid(row=4, column=0, padx=5, sticky='ew')
        self.lbl_lowest_ask.grid(row=5, column=0, padx=5, sticky='ew')
        self.lbl_market_base_volume.grid(row=6, column=0, padx=5, sticky='e')
        self.lbl_market_quote_volume.grid(row=7, column=0, padx=5, sticky='e')

        # pooltool helper
        self.rd_buy.grid(row=0, column=0, padx=5)
        self.rd_sell.grid(row=1, column=0, padx=5)
        self.lbl_trade_amount.grid(row=0, column=1, padx=5)
        self.ent_trade_amount.grid(row=1, column=1, padx=5)
        self.ls_assets.grid(row=0, rowspan=2, column=2, padx=5)
        self.rd_use_market.grid(row=0, column=3, padx=5, sticky='ew')
        self.rd_use_pool.grid(row=1, column=3, padx=5, sticky='ew')
        self.lbl_helper_market_price.grid(row=0, column=4, padx=5, sticky='ew')
        self.lbl_helper_pool_price.grid(row=1, column=4, padx=5, sticky='ew')
        self.btn_update_trade_prices.grid(row=0, column=5, padx=5)
        self.btn_take_offer.grid(row=1, column=5, padx=5, sticky='ew')

        # deposit section
        self.ent_assetx_amount.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_assetx_deposit.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.btn_check_deposit.grid(row=0, column=2, padx=5, pady=5)
        self.ent_assety_amount.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_assety_deposit.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.btn_deposit.grid(row=1, column=2, padx=5, pady=5)

    def get_string_var(self):
        self.string_var = {}
        self.string_var['sv_lbl_pool_id'] = tk.StringVar()
        self.string_var['sv_lbl_pool_name'] = tk.StringVar()
        self.string_var['sv_lbl_pool_balance_a'] = tk.StringVar()
        self.string_var['sv_lbl_pool_balance_b'] = tk.StringVar()
        self.string_var['sv_lbl_pool_invariant'] = tk.StringVar()
        self.string_var['sv_lbl_pool_price_ab'] = tk.StringVar()
        self.string_var['sv_lbl_pool_price_ba'] = tk.StringVar()
        self.string_var['sv_lbl_assets'] = tk.StringVar()
        self.string_var['sv_lbl_market_percentage_change'] = tk.StringVar()
        self.string_var['sv_lbl_latest_price'] = tk.StringVar()
        self.string_var['sv_lbl_highest_bid'] = tk.StringVar()
        self.string_var['sv_lbl_lowest_ask'] = tk.StringVar()
        self.string_var['sv_lbl_market_base_volume'] = tk.StringVar()
        self.string_var['sv_lbl_market_quote_volume'] = tk.StringVar()

        self.string_var['rd_buy_sell'] = tk.StringVar()
        self.string_var['ls_assets'] = tk.StringVar()
        self.string_var['rd_market_or_pool'] = tk.StringVar()
        self.string_var['lbl_helper_market_price'] = tk.StringVar()
        self.string_var['lbl_helper_pool_price'] = tk.StringVar()

        self.string_var['lbl_assetx_deposit'] = tk.StringVar()
        self.string_var['lbl_assety_deposit'] = tk.StringVar()
        self.string_var['lbl_poolshare_deposit'] = tk.StringVar()
        self.string_var['lbl_poolshare_symbol'] = tk.StringVar()

    def assign_string_var(self):
        self.string_var['sv_lbl_pool_id'].set('Pool:')
        self.string_var['sv_lbl_pool_name'].set('Pool name:')
        self.string_var['sv_lbl_pool_balance_a'].set('X Balance:')
        self.string_var['sv_lbl_pool_balance_b'].set('Y Balance:')
        self.string_var['sv_lbl_pool_invariant'].set('Invariant (k=xy):')
        self.string_var['sv_lbl_pool_price_ab'].set('X/Y Price:')
        self.string_var['sv_lbl_pool_price_ba'].set('Y/X Price:')
        self.string_var['sv_lbl_assets'].set('(Market X/Y)')
        self.string_var['sv_lbl_market_percentage_change'].set('(Market % Change)')
        self.string_var['sv_lbl_latest_price'].set('Latest Price:')
        self.string_var['sv_lbl_highest_bid'].set('Highest Bid:')
        self.string_var['sv_lbl_lowest_ask'].set('Lowest Ask:')
        self.string_var['sv_lbl_market_base_volume'].set('24h Base Volume:')
        self.string_var['sv_lbl_market_quote_volume'].set('24h Quote Volume:')

        self.string_var['rd_buy_sell'].set('buy')
        self.string_var['ls_assets'].set(['Asset X', 'Asset Y'])
        self.string_var['rd_market_or_pool'].set('pool')
        self.string_var['lbl_helper_market_price'].set('(Market Price)')
        self.string_var['lbl_helper_pool_price'].set('(Pool Price)')

        self.string_var['lbl_assetx_deposit'].set('Asset X')
        self.string_var['lbl_assety_deposit'].set('Asset y')
        self.string_var['lbl_poolshare_deposit'].set('0')
        self.string_var['lbl_poolshare_symbol'].set('Share Asset')

    def set_dropdown_values(self, settings):
        self.cmb_pool_id['values'] = settings['valid_assets']

    def update_gui(self, data):
        self.string_var['sv_lbl_pool_name'].set('Pool Name: {}'.format(data['pool_name']))
        self.string_var['sv_lbl_pool_balance_a'].set('X Balance: {}'.format(data['amount_x']))
        self.string_var['sv_lbl_pool_balance_b'].set('Y Balance: {}'.format(data['amount_y']))
        self.string_var['sv_lbl_pool_invariant'].set('Invariant (k=xy): {}'.format(data['pool_invariant']))
        self.string_var['sv_lbl_pool_price_ab'].set('X/Y Price: {}'.format(data['price_xy']))
        self.string_var['sv_lbl_pool_price_ba'].set('Y/X Price: {}'.format(data['price_yx']))
        self.string_var['sv_lbl_assets'].set('{}/{}'.format(data['asset_x'].symbol, data['asset_y'].symbol))
        self.string_var['sv_lbl_market_percentage_change'].set('{}%'.format(data['market_ticker_object']['percentChange']))
        self.string_var['sv_lbl_latest_price'].set('Latest Price: {}'.format(data['market_ticker_object']['latest']))
        self.string_var['sv_lbl_highest_bid'].set('Highest Bid: {}'.format(data['market_ticker_object']['highestBid']))
        self.string_var['sv_lbl_lowest_ask'].set('Lowest Ask: {}'.format(data['market_ticker_object']['lowestAsk']))
        self.string_var['sv_lbl_market_base_volume'].set('24hr Base Volume: {}'.format(data['market_ticker_object']['baseVolume']))
        self.string_var['sv_lbl_market_quote_volume'].set('24hr Quote Volume: {}'.format(data['market_ticker_object']['quoteVolume']))

        self.string_var['ls_assets'].set([data['asset_x'].symbol, data['asset_y'].symbol])
        self.string_var['lbl_helper_market_price'].set('')
        self.string_var['lbl_helper_pool_price'].set('')
        self.frame_depthchart.update_blockchain_data(data)

        self.string_var['lbl_assetx_deposit'].set(data['asset_x'].symbol)
        self.string_var['lbl_assety_deposit'].set(data['asset_y'].symbol)
        self.string_var['lbl_poolshare_symbol'].set(data['pool_name'])

        self.rd_buy['state'] = 'normal'
        self.rd_sell['state'] = 'normal'
        self.ent_trade_amount['state'] = 'normal'
        self.ls_assets['state'] = 'normal'
        self.rd_use_pool['state'] = 'normal'
        self.btn_update_trade_prices['state'] = 'enabled'

        self.ent_assetx_amount['state'] = 'normal'
        self.ent_assety_amount['state'] = 'normal'
        self.btn_deposit['state'] = 'enabled'

        self.loading_pop_up.destroy()
        self.window.update()

    def create_menu(self):
        menubar = tk.Menu(self.window)
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label='Quit', command=self.quit_program)
        menubar.add_cascade(label='File', menu=menu_file)
        self.window.config(menu=menubar)
        self.window.config

    def change_pool(self, event):
        self.loading_popup()
        pub.sendMessage('pool_change_requested',
                        data=self.cmb_pool_id['values'][self.cmb_pool_id.current()]
        )

    def change_asset(self, event):
        sel_tuple = event.widget.curselection()
        sel = 0 if (len(sel_tuple) and sel_tuple[0] == 0) else 1
        pub.sendMessage('asset_of_interest_change', data=sel)

    def update_shares(self):
        pass

    def deposit_to_lp(self):
        data = {
            'asset_x_amount': self.ent_assetx_amount.get(),
            'asset_x_symbol': self.string_var['lbl_assetx_deposit'].get(),
            'asset_y_amount': self.ent_assety_amount.get(),
            'asset_y_symbol': self.string_var['lbl_assety_deposit'].get(),
            'poolshare_symbol': self.string_var['lbl_poolshare_symbol'].get()
        }
        answer = messagebox.askyesno(
            'Verify Action',
            'You want to deposit {} {} and {} {} in exchange for {}?'.format(
                data['asset_x_amount'],
                data['asset_x_symbol'],
                data['asset_y_amount'],
                data['asset_y_symbol'],
                data['poolshare_symbol']
            ),
            parent=self.window
        )
        if answer:
            data['account'] = simpledialog.askstring('Account Name', 'Enter your account:', parent=self.window)
            data['key'] = simpledialog.askstring('Active Key', 'Enter your active key:', show='*', parent=self.window)
            self.deposit_popup()
            pub.sendMessage('deposit_lp', data=data)

    def take_offer(self):
        data = {
            'market_or_pool': self.string_var['rd_market_or_pool'].get(),
            'buy_or_sell': self.string_var['rd_buy_sell'].get(),
            'amount_to_buy_sell': self.ent_trade_amount.get(),
            'selected_asset': self.ls_assets.get(self.ls_assets.curselection()),
            'pool_id': self.cmb_pool_id.get(),
            'expected_price': self.string_var['lbl_helper_market_price'].get() \
                if self.string_var['rd_market_or_pool'].get() == 'market' \
                else self.string_var['lbl_helper_pool_price'].get()
        }
        answer = messagebox.askyesno(
            'Verify Action',
            'You want to use the {} to {} {} {} for {}?'.format(
                data['market_or_pool'],
                data['buy_or_sell'],
                data['amount_to_buy_sell'],
                data['selected_asset'],
                data['expected_price']
            ),
            parent=self.window
        )
        if answer:
            data['account'] = simpledialog.askstring('Account Name', 'Enter your account:', parent=self.window)
            data['key'] = simpledialog.askstring('Active Key', 'Enter your active key:', show='*', parent=self.window)
            pub.sendMessage('take_offer', data=data)

    def print_transaction(self, data):
        messagebox.showinfo(
            'Trade Data',
            '{}\nPaid: {}\nAnticipated: {}\nReceived: {}'.format(
                data['operation_type'],
                data['paid'],
                data['anticipated'],
                data['received']
            ),
            parent=self.window
        )

    def print_deposit(self, data):
        if len(data) != 0:
            self.deposit_pop_up.destroy()
            self.window.update()
            messagebox.showinfo(
                'Deposit Data',
                'Deposited:\n\t{}\n\t{}\nfor:\n\t{}'.format(
                    data['paid_x'],
                    data['paid_y'],
                    data['received']
                ),
                parent=self.window,
            )

    def deposit_popup(self):
        self.deposit_pop_up = tk.Toplevel(
            self.window
        )
        pos_x = self.window.winfo_x()
        pos_y = self.window.winfo_y()
        self.deposit_pop_up.geometry(f'+{pos_x}+{pos_y}')
        self.lbl_deposit_pop = tk.Label(
            self.deposit_pop_up,
            text='depositing to liquidity pool...'
        )
        self.lbl_deposit_pop.grid(row=0, column=0, padx=5, pady=5)
        self.deposit_pop_up.update()

    def loading_popup(self):
        self.loading_pop_up = tk.Toplevel(
            self.window
        )
        pos_x = self.window.winfo_x()
        pos_y = self.window.winfo_y()
        self.loading_pop_up.geometry(f'+{pos_x}+{pos_y}')
        self.lbl_loading = tk.Label(
            self.loading_pop_up,
            text='loading new pool information...'
        )
        self.lbl_loading.grid(row=0, column=0, padx=5, pady=5)
        self.loading_pop_up.update()

    def update_prices(self):
        data = {}
        data['buy_or_sell'] = str(self.string_var['rd_buy_sell'].get())
        data['amount'] = float(self.ent_trade_amount.get())
        data['assets'] = self.string_var['ls_assets'].get()
        data['balance_x'] = self.string_var['sv_lbl_pool_balance_a'].get()
        data['balance_y'] = self.string_var['sv_lbl_pool_balance_b'].get()
        data['invariant'] = float(self.string_var['sv_lbl_pool_invariant'].get()[18:])
        data['selected_asset'] = self.ls_assets.curselection()[0]
        pub.sendMessage('update_prices', data=data)
        self.btn_take_offer['state'] = 'enabled'

    def update_trading_prices(self, data):
        self.string_var['lbl_helper_market_price'].set(data['market'])
        self.string_var['lbl_helper_pool_price'].set(data['pool'])

    def invalid_pool(self):
        self.loading_pop_up.destroy()
        self.window.update()
        messagebox.showinfo(
                'Error',
                'Invalid pool selection. Pool was likely deleted or has a zero balance somewhere. Please try a different pool.',
                parent=self.window,
            )

    def quit_program(self):
        pub.sendMessage('quit_program_requested')

    def palette(self, item):
        color_palette = {
            'header': '#333333',
            'body': '#1E1E1E',
            'green': '#69872D',
            'red': '#DF413A'
        }
        return color_palette[item]