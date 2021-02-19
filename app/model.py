from pubsub import pub
from bitshares.bitshares import BitShares
from bitshares.asset import Asset
from bitshares.amount import Amount
from bitshares.market import Market
from bitshares.blockchain import Blockchain
from bitshares.instance import set_shared_blockchain_instance
from pprint import pprint
import json
from websocket import create_connection


class Model:
    BLOCK_HOUR = 1200

    def __init__(self, **kwargs):
        self.bs = BitShares(
            node='wss://api.iamredbar.com/ws',
            nobroadcast=True,
            blocking='head',
        )
        set_shared_blockchain_instance(self.bs)
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

    def pool_change(self, new_pool_str):
        new_data = {}
        pool_obj = self.bs.rpc.get_object(new_pool_str.split(' ')[1])
        # pprint(pool_obj)
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
        # this is the generation of the history panel information
        ws = create_connection('wss://api.iamredbar.com/ws')
        buckets = [100, 200, 300]
        op_list = {}
        prev_result = None
        for bucket in buckets:
            payload = {"id": 1,
                       "method": "call",
                       "params": [
                           "history",
                           "get_liquidity_pool_history_by_sequence",
                           [
                               new_pool_str.split(' ')[1],
                               bucket,
                               None,
                               100,
                               63
                           ]
                       ]
                       }
            ws.send(json.dumps(payload))
            result = ws.recv()
            r = json.loads(result)
            if prev_result == r:
                break
            else:
                if not r['result']:
                    break
                for i in r['result']:
                    if not i['sequence'] in op_list.keys():
                        op_list[i['sequence']] = i
            prev_result = r
        sort_order = sorted(op_list, reverse=True)
        new_data['history'] = []
        for op in sort_order:
            # the dictionary keys are always asset_a icon asset_b
            # this determines what is for sale, and puts the correct arrow and asset order
            if op_list[op]['op']['op'][1]['amount_to_sell']['asset_id'] == self.asset_a_id:
                icon = 'arrow-right'
                asset_a = str(Amount(op_list[op]['op']['result'][1]['paid'][0]))
                asset_b = str(Amount(op_list[op]['op']['result'][1]['received'][0]))
            else:
                icon = 'arrow-left'
                asset_a = str(Amount(op_list[op]['op']['result'][1]['received'][0]))
                asset_b = str(Amount(op_list[op]['op']['result'][1]['paid'][0]))
            new_data['history'].append(
                {
                    'asset_a': asset_a,
                    'icon': icon,
                    'asset_b': asset_b
                }
            )
        # Generate activity from history for stats panel
        _last_confirmed_block = Blockchain(blockchain_instance=self.bs, mode='irreversible').get_current_block_num()
        swap_count = 0
        for op in sort_order:
            if op_list[op]['op']['block_num'] > _last_confirmed_block - (self.BLOCK_HOUR * 24):
                swap_count += 1
        # Get pool value
        new_data['value'] = self._get_pool_value(self.asset_a_symbol, self.asset_a_balance, self.asset_b_symbol, self.asset_b_balance)
        new_data['swap_count'] = swap_count
        if float(new_data['share_asset_balance']) != 0:
            new_data['poolshare_value'] = float(new_data['value'] / float(new_data['share_asset_balance']))
        else:
            new_data['poolshare_value'] = 0
        # print(new_data['poolshare_value'])
        pub.sendMessage('update_pool_change', data=new_data)

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

    def get_pools(self):
        ws = create_connection('wss://api.iamredbar.com/ws')
        payload1 = {
            "id": 1,
            "method": "call",
            "params": [
                "database",
                "list_liquidity_pools",
                []
            ]
        }
        ws.send(json.dumps(payload1))
        result1 = ws.recv()
        r = json.loads(result1)
        data = []
        for i in r['result']:
            data.append(f'{Asset(self.bs.rpc.get_object(i["id"])["share_asset"]).symbol} {i["id"]}')
        pub.sendMessage('return_pool_list', data=data)

    def _get_pool_value(self, asset_a, amount_a, asset_b, amount_b):
        if asset_a == 'BTS':
            bts_value_a = float(amount_a)
        else:
            temp = float(str(Market(f'{asset_a}/BTS').ticker()['latest']).split(' ')[0]) * float(amount_a)
            bts_value_a = round(temp, 5)
        if asset_b == 'BTS':
            bts_value_b = float(amount_b)
        else:
            temp = float(str(Market(f'{asset_b}/BTS').ticker()['latest']).split(' ')[0]) * float(amount_b)
            bts_value_b = round(temp, 5)
        bts_usd_val = float(str(Market('BTS/USD').ticker()['latest']).split(' ')[0])
        usd_val = (bts_value_a * bts_usd_val) + (bts_value_b * bts_usd_val)
        return round(usd_val, 2)

    def swap_assets(self, data):
        l_bs = BitShares(
            node='wss://api.iamredbar.com/ws',
            keys=data['key'],
            blocking='head',
            nobroadcast=False,
        )
        amount_to_sell = Amount(data["sell_amount"], data["sell_asset"])
        anticipated = Amount(data['receive_approx_amount'], data['receive_asset'])
        min_to_receive = anticipated * 0.993
        trade_message = l_bs.exchange_with_liquidity_pool(
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
        l_bs = BitShares(
            node='wss://api.iamredbar.com/ws',
            keys=data['key'],
            blocking='head',
            nobroadcast=False,
        )
        trade_message = l_bs.deposit_into_liquidity_pool(
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
        l_bs = BitShares(
            node='wss://api.iamredbar.com/ws',
            keys=data['key'],
            blocking='head',
            nobroadcast=False,
        )
        trade_message = l_bs.withdraw_from_liquidity_pool(
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
