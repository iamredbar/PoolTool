from bitshares.amount import Amount
from bitshares.bitshares import BitShares
from bitshares.block import Block
from bitshares.account import Account
from bitshares.instance import set_shared_bitshares_instance
from websocket import create_connection
from datetime import datetime
import json
from bitshares.utils import formatTimeFromNow


bs = BitShares(
    node='wss://api.iamredbar.com/ws',
)
set_shared_bitshares_instance(bs)
ws = create_connection('wss://api.iamredbar.com/ws')
payload = {"id": 1,
           "method": "call",
           "params": [
               "history",
               "get_liquidity_pool_history",
               [
                   '1.19.0',
                   formatTimeFromNow(0),
                   None,
                   100,
                   63
               ]
           ]
           }
ws.send(json.dumps(payload))
result = ws.recv()
print(result)



# ACC_ID = '1.2.546734'
# ACC_NAME = 'iamredbar1'
# history_gen = Account(ACC_NAME).history()
# unknown_ops = []
#
# with open(f'{ACC_NAME}_readable_timestamp.txt', 'w') as file:
#     file.writelines('Parsed ops:\n')
#     for i in history_gen:
#         if i['op'][0] == 0:
#             if i['op'][1]['from'] == ACC_ID:
#                 file.writelines(f'Sent {Amount(i["op"][1]["amount"])} to {Account(i["op"][1]["to"]).name}. Time: {Block(i["block_num"])["timestamp"]}\n')
#             else:
#                 file.writelines(f'Received {Amount(i["op"][1]["amount"])} from {Account(i["op"][1]["from"]).name}. Time: {Block(i["block_num"])["timestamp"]}\n')
#         elif i['op'][0] == 1:
#             file.writelines(f'Created order ref {i["result"][1]}: Sell {Amount(i["op"][1]["amount_to_sell"])} for min {Amount(i["op"][1]["min_to_receive"])}. Time: {Block(i["block_num"])["timestamp"]}\n')
#         elif i['op'][0] == 2:
#             file.writelines(f'Cancelled order ref: {i["op"][1]["order"]}. Time: {Block(i["block_num"])["timestamp"]}\n')
#         elif i['op'][0] == 4:
#             file.writelines(f'Order filled ref {i["op"][1]["order_id"]}: Sold {Amount(i["op"][1]["pays"])} for {Amount(i["op"][1]["receives"])}. Maker: {i["op"][1]["is_maker"]}. Time: {Block(i["block_num"])["timestamp"]}\n')
#         elif i['op'][0] == 5:
#             file.writelines(f'Account <{i["op"][1]["name"]}> created. Time: {Block(i["block_num"])["timestamp"]}\n')
#         elif i['op'][0] == 8:
#             file.writelines(f'Paid {Amount(i["op"][1]["fee"])} to upgrade to Lifetime Member. Time: {Block(i["block_num"])["timestamp"]}\n')
#         elif i['op'][0] == 14:
#             file.writelines(f'{Amount(i["op"][1]["asset_to_issue"])} issued to {Account(i["op"][1]["issue_to_account"]).name}. Time: {Block(i["block_num"])["timestamp"]}\n')
#         elif i['op'][0] == 33:
#             file.writelines(f'Withdrew vesting balance of {Amount(i["op"][1]["amount"])}. Time: {Block(i["block_num"])["timestamp"]}\n')
#         # elif i['op'][0] == 38:
#         #     file.writelines(f'\n')
#         else:
#             unknown_ops.append(i)
#
#     file.writelines('Unparsed ops:\n')
#     for j in unknown_ops:
#         file.writelines(str(j) + '\n')
