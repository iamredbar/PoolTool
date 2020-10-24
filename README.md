# PoolTool
A simple tool to help anyone use Liquidity Pools on the BitShares blockchain.

Written entirely in Python, it will work on any platform that can run Python.

## Installation
Requires Python 3.8+

Tested on MacOS 10.14.6, Ubuntu 20.10, and 32-bit Raspberry Pi OS. No Windows solution currently.

```sudo apt-get install libffi-dev libssl-dev python3-dev python3-tk```

```git clone https://github.com/iamredbar/PoolTool.git```

```cd PoolTool```

```pip3 install -r requirements.txt```

## Set up

You will need to set a default node using `Uptick`. Syntax is like this:

```uptick set node <node_goes_here>```

Example:

```uptick set node 'wss://btsfullnode.bangzi.info/ws'```

If this step is not done, it is very unlikely that it will work.

## Start Up

```python3 controller.py```

## Basic Walkthrough

Upon start up, you will need to select the pool you would like to use via the dropdown menu.

![PoolTool Screenshot](https://i.ibb.co/6Z2gSZq/Screen-Shot-2020-10-23-at-9-38-55-PM.png)

At that time, you will need to select whether you would like to buy or sell, choose the asset, and enter the amount. Click `Update Price`. This will give you an amount that it will cost or amount you will receive, depending on your choices. Clicking `Take Offer` will display a pop-up asking for confirmation of the exchange.

![PoolTool Screenshot](https://i.ibb.co/25drNXh/Screen-Shot-2020-10-23-at-9-39-31-PM.png)

Enter your account name, and your active key. This will then broadcast the transaction.

![PoolTool Screenshot](https://i.ibb.co/BqXb1n7/Screen-Shot-2020-10-23-at-9-40-00-PM.png)

If it is successful, you will get another pop-up window with the `amount paid`, `amount expected`, and `amount received`.

![PoolTool Screenshot](https://i.ibb.co/0FW3ddD/Screen-Shot-2020-10-23-at-9-40-42-PM.png)

### Please report any issues you have in Github. 
