# PoolTool
A simple GUI tool to help anyone use Liquidity Pools on the BitShares blockchain.

Written entirely in Python, it will work on any platform that can run Python.

## Installation
Requires Python 3.8+

Tested on MacOS 10.14.6, Ubuntu 20.10, and 32-bit Raspberry Pi OS. No Windows solution currently.

```sudo apt-get install libffi-dev libssl-dev python3-dev python3-tk```

```git clone https://github.com/iamredbar/PoolTool.git```

```cd PoolTool```

```sudo pip3 install -r requirements.txt```

## Set up

You will need to set a default node using `uptick`. Syntax is like this:

```uptick set node <node_goes_here>```

Example:

```uptick set node 'wss://btsfullnode.bangzi.info/ws'```

**If this step is not done, it is very unlikely that it will work.**

(read more about `uptick` here: http://docs.uptick.rocks/en/latest/)

## Start Up

```python3 controller.py```

## Basic Walkthrough

Upon start up, you will need to select the pool you would like to use via the dropdown menu.

![PoolTool Screenshot](https://i.ibb.co/nw6bz6H/Screen-Shot-2020-10-25-at-9-30-10-AM.png)

At that time, you will need to select whether you would like to buy or sell, choose the asset, and enter the amount. Click `Update Price`. This will give you an amount that it will cost or amount you will receive, depending on your choices. Clicking `Take Offer` will display a pop-up asking for confirmation of the exchange.

![PoolTool Screenshot](https://i.ibb.co/b68n3TN/Screen-Shot-2020-10-25-at-9-30-40-AM.png)

![PoolTool Screenshot](https://i.ibb.co/fkFxRFB/Screen-Shot-2020-10-25-at-9-30-53-AM.png)

Enter your account name, and your active key. This will then broadcast the transaction.

![PoolTool Screenshot](https://i.ibb.co/jyyGhdD/Screen-Shot-2020-10-25-at-9-31-11-AM.png)

![PoolTool Screenshot](https://i.ibb.co/H29tbYd/Screen-Shot-2020-10-25-at-9-31-32-AM.png)

If it is successful, you will get another pop-up window with the `amount paid`, `amount anticipated`, and `amount received`.

![PoolTool Screenshot](https://i.ibb.co/9Yj3kCb/Screen-Shot-2020-10-25-at-9-31-58-AM.png)

### Please report any issues you have via Github. 
