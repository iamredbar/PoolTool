from pubsub import pub
from bitshares.bitshares import BitShares
from bitshares.asset import Asset
from bitshares.amount import Amount
from bitshares.market import Market
from bitshares.blockchain import Blockchain
from bitshares.instance import set_shared_blockchain_instance
from bitshares.utils import formatTimeFromNow
from pprint import pprint
import json
from websocket import create_connection

POOL_ID_LIMIT = 200


class Model:
    BLOCK_HOUR = 1200

    def __init__(self, **kwargs):
        self.bs = None
        self.keyed_bs = None
        self.ws = None
        self.node = None
        self.denomination = None
        self.pool_id = None
        self.asset_a_precision = None
        self.asset_b_precision = None
        self.share_asset_precision = None
        self.virtual_value = None
        self.invariant = None
        self.asset_a_id = None
        self.asset_a_symbol = None
        self.asset_a_balance = None
        self.asset_b_id = None
        self.asset_b_symbol = None
        self.asset_b_balance = None
        self.share_asset_id = None
        self.share_asset_symbol = None
        self.share_asset_balance = None
        self.swap_fee = None
        self.withdraw_fee = None
        self.price_switch = 'b/a'
        self.history = []
        self.usd_val_a = 0
        self.usd_val_b = 0
        self.bts_val_a = 0
        self.bts_val_b = 0
        self.cny_val_a = 0
        self.cny_val_b = 0

    def pool_change(self, new_pool_str):
        new_data = {}
        pool_obj = self.bs.rpc.get_object(new_pool_str.split(' ')[1])
        self.usd_val_a = 0
        self.usd_val_b = 0
        self.bts_val_a = 0
        self.bts_val_b = 0
        self.cny_val_a = 0
        self.cny_val_b = 0
        asset_a = Asset(pool_obj['asset_a'])
        asset_b = Asset(pool_obj['asset_b'])
        share_asset = Asset(pool_obj['share_asset'])
        self.pool_id = pool_obj['id']
        self.asset_a_precision = asset_a.precision
        new_data['asset_a_precision'] = self.asset_a_precision
        self.asset_b_precision = asset_b.precision
        new_data['asset_b_precision'] = self.asset_b_precision
        self.share_asset_precision = share_asset.precision
        self.virtual_value = pool_obj['virtual_value']
        self.invariant = int(self.virtual_value) / (10 ** (int(self.asset_a_precision) + int(self.asset_b_precision)))
        self.asset_a_id = asset_a.identifier
        new_data['asset_a_id'] = self.asset_a_id
        self.asset_a_symbol = asset_a.symbol
        new_data['asset_a_symbol'] = self.asset_a_symbol
        self.asset_a_balance = str(int(pool_obj['balance_a']) / 10 ** asset_a.precision)
        new_data['asset_a_balance'] = self.asset_a_balance
        self.asset_b_id = asset_b.identifier
        new_data['asset_b_id'] = self.asset_b_id
        self.asset_b_symbol = asset_b.symbol
        new_data['asset_b_symbol'] = self.asset_b_symbol
        self.asset_b_balance = str(int(pool_obj['balance_b']) / 10 ** asset_b.precision)
        new_data['asset_b_balance'] = self.asset_b_balance
        self.share_asset_id = share_asset.identifier
        new_data['share_asset_id'] = self.share_asset_id
        self.share_asset_symbol = share_asset.symbol
        new_data['share_asset_symbol'] = self.share_asset_symbol
        temp = self.bs.rpc.get_object(share_asset['dynamic_asset_data_id'])['current_supply']
        self.share_asset_balance = str(int(temp) / (10 ** share_asset['precision']))
        new_data['share_asset_balance'] = self.share_asset_balance
        Asset.clear_cache()
        # this is the generation of the stats panel information
        self.swap_fee = f'{pool_obj["taker_fee_percent"] / 100}%'
        new_data['swap_fee'] = self.swap_fee
        self.withdraw_fee = f'{pool_obj["withdrawal_fee_percent"] / 100}%'
        new_data['withdraw_fee'] = self.withdraw_fee
        history_info = self.generate_history(new_pool_str.split(' ')[1])
        # Get pool value
        self._get_pool_value(
            self.asset_a_symbol,
            self.asset_a_balance,
            self.asset_b_symbol,
            self.asset_b_balance,
        )
        if self.denomination == 'BitUSD':
            _precision = 2
            new_data['value'] = f'{(self.usd_val_a + self.usd_val_b):.2f} USD'
        elif self.denomination == 'BTS':
            _precision = 5
            new_data['value'] = f'{(self.bts_val_a + self.bts_val_b):.5f} BTS'
        elif self.denomination == 'BitCNY':
            _precision = 4
            new_data['value'] = f'{(self.cny_val_a + self.cny_val_b):.4f} CNY'
        new_data['swap_count'] = history_info['swap_count']
        new_data['history'] = []
        for item in history_info['history']:
            new_data['history'].append(item)
        if float(self.share_asset_balance) != 0:
            new_data['poolshare_value'] = f'{round(float(new_data["value"].split(" ")[0]) / float(self.share_asset_balance), _precision)} {new_data["value"].split(" ")[1]}'
        else:
            new_data['poolshare_value'] = 0
        pub.sendMessage('update_pool_change', data=new_data)

    def display_pool_value(self):
        pass

    def price_swap(self):
        self.price_switch = 'a/b' if self.price_switch == 'b/a' else 'b/a'
        history = []
        for op in self.history:
            if self.price_switch == 'a/b':
                history.append(
                    {
                        'asset_a': op['asset_a'],
                        'icon': op['icon'],
                        'asset_b': op['asset_b'],
                        'price': op['price_ab'],
                        'price_color': op['price_ab_color'],
                    }
                )
            else:
                history.append(
                    {
                        'asset_a': op['asset_a'],
                        'icon': op['icon'],
                        'asset_b': op['asset_b'],
                        'price': op['price_ba'],
                        'price_color': op['price_ba_color'],
                    }
                )
        pub.sendMessage('refresh_history_panel', data=history)

    def generate_history(self, pool):
        return_data = {}
        op_list = {}
        payload = {"id": 1,
                   "method": "call",
                   "params": [
                       "history",
                       "get_liquidity_pool_history",
                       [
                           pool,
                           formatTimeFromNow(0),
                           None,
                           100,
                           63
                       ]
                   ]
                   }
        self._set_ws_connection()
        self.ws.send(json.dumps(payload))
        result = self.ws.recv()
        r = json.loads(result)
        if r['result']:
            for i in r['result']:
                if not i['sequence'] in op_list.keys():
                    op_list[i['sequence']] = i
        sort_order = sorted(op_list, reverse=True)
        return_data['history'] = []
        _prev_price = None
        for index, op in enumerate(sort_order):
            # the dictionary keys are always asset_a, icon, asset_b, price, price_color
            # this determines what is for sale, and puts the correct arrow and asset order
            if op_list[op]['op']['op'][1]['amount_to_sell']['asset_id'] == self.asset_a_id:
                icon = 'arrow-right'
                asset_a = str(Amount(op_list[op]['op']['result'][1]['paid'][0]))
                asset_b = str(Amount(op_list[op]['op']['result'][1]['received'][0]))
            else:
                icon = 'arrow-left'
                asset_a = str(Amount(op_list[op]['op']['result'][1]['received'][0]))
                asset_b = str(Amount(op_list[op]['op']['result'][1]['paid'][0]))
            try:
                if op_list[sort_order[index + 1]]['op']['op'][1]['amount_to_sell']['asset_id'] == self.asset_a_id:
                    _asset_a = str(Amount(op_list[sort_order[index + 1]]['op']['result'][1]['paid'][0]))
                    _asset_b = str(Amount(op_list[sort_order[index + 1]]['op']['result'][1]['received'][0]))
                else:
                    _asset_a = str(Amount(op_list[sort_order[index + 1]]['op']['result'][1]['received'][0]))
                    _asset_b = str(Amount(op_list[sort_order[index + 1]]['op']['result'][1]['paid'][0]))
            except:
                pass
            _price_ab = float(asset_a.split(' ')[0].replace(',', '')) / float(asset_b.split(' ')[0].replace(',', ''))
            _price_ba = float(asset_b.split(' ')[0].replace(',', '')) / float(asset_a.split(' ')[0].replace(',', ''))
            # check previous y/x price, change color depending on result
            price_ab_color = '#808080'
            price_ba_color = '#808080'
            if index != 99:
                _prev_price_ab = float(_asset_a.split(' ')[0].replace(',', '')) / float(_asset_b.split(' ')[0].replace(',', ''))
                _prev_price_ba = float(_asset_b.split(' ')[0].replace(',', '')) / float(_asset_a.split(' ')[0].replace(',', ''))
                if _price_ab > _prev_price_ab:
                    price_ab_color = '#669f38'
                    price_ba_color = '#e9002c'
                elif _price_ab < _prev_price_ab:
                    price_ab_color = '#e9002c'
                    price_ba_color = '#669f38'
            self.history.append(
                {
                    'asset_a': asset_a,
                    'icon': icon,
                    'asset_b': asset_b,
                    'price_ab': f'{_price_ab:.3f}',
                    'price_ab_color': price_ab_color,
                    'price_ba': f'{_price_ba:.3f}',
                    'price_ba_color': price_ba_color,
                }
            )
        # Generate activity from history for stats panel
        _last_confirmed_block = Blockchain(mode='irreversible').get_current_block_num()
        swap_count = 0
        for op in sort_order:
            if op_list[op]['op']['block_num'] > _last_confirmed_block - (self.BLOCK_HOUR * 24):
                swap_count += 1
        return_data['swap_count'] = swap_count
        for op in self.history:
            if self.price_switch == 'b/a':
                return_data['history'].append(
                    {
                        'asset_a': op['asset_a'],
                        'icon': op['icon'],
                        'asset_b': op['asset_b'],
                        'price': op['price_ba'],
                        'price_color': op['price_ba_color'],
                    }
                )
            else:
                return_data['history'].append(
                    {
                        'asset_a': op['asset_a'],
                        'icon': op['icon'],
                        'asset_b': op['asset_b'],
                        'price': op['price_ab'],
                        'price_color': op['price_ab_color'],
                    }
                )
        return return_data

    def set_denomination(self, data):
        self.denomination = data
        self._get_pool_value(
            self.asset_a_symbol,
            self.asset_a_balance,
            self.asset_b_symbol,
            self.asset_b_balance,
        )
        new_data = {}
        if self.denomination == 'BitUSD':
            _precision = 2
            new_data['value'] = f'{(self.usd_val_a + self.usd_val_b):.2f} USD'
        elif self.denomination == 'BTS':
            _precision = 5
            new_data['value'] = f'{(self.bts_val_a + self.bts_val_b):.5f} BTS'
        elif self.denomination == 'BitCNY':
            _precision = 4
            new_data['value'] = f'{(self.cny_val_a + self.cny_val_b):.4f} CNY'
        if float(self.share_asset_balance) != 0:
            new_data['poolshare_value'] = f'{round(float(new_data["value"].split(" ")[0]) / float(self.share_asset_balance), _precision)} {new_data["value"].split(" ")[1]}'
        else:
            new_data['poolshare_value'] = 0
        pub.sendMessage('refresh_stats_panel', data=new_data)

    def correct_pool_amount(self, higher_amount, lower_amount, asset):
        precision = Asset(asset).precision
        Asset.clear_cache()
        difference = higher_amount - lower_amount
        return float(round(difference, precision))

    # exchange preserves x*y
    # buying subtracts from that side of the pool
    # selling adds to that side of the pool
    def update_pool_price(self, data):
        if data['swap_asset'] == self.asset_a_symbol:
            swap_flag = 'a'
            reference = float(self.asset_a_balance)
        else:
            swap_flag = 'b'
            reference = float(self.asset_b_balance)
        addition_to = reference + float(data['amount'])
        new_balance = self.invariant / addition_to
        output_amount = self.correct_pool_amount(
            float(self.asset_b_balance) if swap_flag == 'a' else float(self.asset_a_balance),
            new_balance,
            data['purchase_asset']
        )
        pub.sendMessage('update_pool_estimate', data=str(output_amount))

    def _set_ws_connection(self):
        self.ws = create_connection(self.node)

    def get_pools(self, data):
        self.node = data['node']
        self.denomination = data['denomination']
        self.bs = BitShares(
            node=self.node,
            nobroadcast=True,
            blocking='head',
        )
        set_shared_blockchain_instance(self.bs)
        self._set_ws_connection()
        _counter = 0
        data = []
        while _counter < POOL_ID_LIMIT:
            payload_string = "1.19." + str(_counter)
            payload1 = {
                "id": 1,
                "method": "call",
                "params": [
                    "database",
                    "list_liquidity_pools",
                    [
                        100,
                        payload_string,
                        False
                    ]
                ]
            }
            self.ws.send(json.dumps(payload1))
            result1 = self.ws.recv()
            r = json.loads(result1)
            # print(r)
            for i in r['result']:
                data.append(f'{Asset(self.bs.rpc.get_object(i["id"])["share_asset"]).symbol} {i["id"]}')
            _counter += 100
        pub.sendMessage('return_pool_list', data=data)

    def _get_pool_value(self, asset_a, amount_a, asset_b, amount_b):
        # check each asset separately, first for USD, then BTS, then derive
        # asset a
        if asset_a == 'USD':
            self.usd_val_a = float(amount_a)
        if asset_a == 'BTS':
            self.bts_val_a = float(amount_a)
        if asset_a == 'CNY':
            self.cny_val_a = float(amount_a)
        # derive BTS then others, validate they aren't already there
        if self.bts_val_a == 0:
            self.bts_val_a = round(float(str(Market(f'{asset_a}/BTS').ticker()['latest']).split(' ')[0]) * float(amount_a), 5)
        if self.usd_val_a == 0:
            bts_usd_val = float(str(Market('BTS/USD').ticker()['latest']).split(' ')[0])
            self.usd_val_a = self.bts_val_a * bts_usd_val
        if self.cny_val_a == 0:
            bts_cny_val = float(str(Market('BTS/CNY').ticker()['latest']).split(' ')[0])
            self.cny_val_a = self.bts_val_a * bts_cny_val
        # asset b
        if asset_b == 'USD':
            self.usd_val_b = float(amount_b)
        if asset_b == 'BTS':
            self.bts_val_b = float(amount_b)
        if asset_b == 'CNY':
            self.cny_val_b = float(amount_b)
        # derive
        if self.bts_val_b == 0:
            self.bts_val_b = round(float(str(Market(f'{asset_b}/BTS').ticker()['latest']).split(' ')[0]) * float(amount_b), 5)
        if self.usd_val_b == 0:
            bts_usd_val = float(str(Market('BTS/USD').ticker()['latest']).split(' ')[0])
            self.usd_val_b = self.bts_val_b * bts_usd_val
        if self.cny_val_b == 0:
            bts_cny_val = float(str(Market('BTS/CNY').ticker()['latest']).split(' ')[0])
            self.cny_val_b = self.bts_val_b * bts_cny_val

    # def _verify_active_key(self, key):
    #     """
    #     returns account from private key
    #     this will be used to verify whether or not the
    #     supplied key will be sufficient enough to do the
    #     operation
    #     """
    #     print(self.bs.wallet.getAccountFromPrivateKey(key))

    def _set_keyed_bs(self, key):
        self.keyed_bs = BitShares(
            node=self.node,
            keys=key,
            blocking='head',
            nobroadcast=False,
        )

    def swap_assets(self, data):
        self._set_keyed_bs(data['key'])
        amount_to_sell = Amount(data["sell_amount"], data["sell_asset"])
        anticipated = Amount(data['receive_approx_amount'], data['receive_asset'])
        min_to_receive = anticipated * 0.993
        trade_message = self.keyed_bs.exchange_with_liquidity_pool(
            pool=self.pool_id,
            amount_to_sell=amount_to_sell,
            min_to_receive=min_to_receive,
            account=data['account'],
        )
        return_data = {
            'anticipated': anticipated,
            'paid': Amount(trade_message['operation_results'][0][1]['paid'][0]),
            'received': Amount(trade_message['operation_results'][0][1]['received'][0]),
            'operation_results': trade_message['operation_results'],
            'interaction_type': 'swap',
        }
        pub.sendMessage('interaction_return', data=return_data)

    def deposit_assets(self, data):
        self._set_keyed_bs(data['key'])
        trade_message = self.keyed_bs.deposit_into_liquidity_pool(
            pool=self.pool_id,
            amount_a=Amount(data['amount_a'], data['asset_a']),
            amount_b=Amount(data['amount_b'], data['asset_b']),
            account=data['account'],
        )
        return_data = {
            'paid_a': Amount(trade_message['operation_results'][0][1]['paid'][0]),
            'paid_b': Amount(trade_message['operation_results'][0][1]['paid'][1]),
            'received': Amount(trade_message['operation_results'][0][1]['received'][0]),
            'operation_results': trade_message['operation_results'],
            'interaction_type': 'deposit',
        }
        pub.sendMessage('interaction_return', data=return_data)

    def withdraw_assets(self, data):
        self._set_keyed_bs(data['key'])
        trade_message = self.keyed_bs.withdraw_from_liquidity_pool(
            pool=self.pool_id,
            share_amount=Amount(data['amount'], data['share_asset']),
            account=data['account'],
        )
        return_data = {
            'exchanged': Amount(trade_message['operation_results'][0][1]['paid'][0]),
            'received_a': Amount(trade_message['operation_results'][0][1]['received'][0]),
            'received_b': Amount(trade_message['operation_results'][0][1]['received'][1]),
            'operation_results': trade_message['operation_results'],
            'interaction_type': 'withdraw',
        }
        pub.sendMessage('interaction_return', data=return_data)
