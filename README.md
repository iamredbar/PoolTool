# PoolTool
A simple GUI tool to help anyone use Liquidity Pools on the BitShares blockchain.

Written entirely in Python, it will work on any platform that can run Python.

Telegram Group: https://t.me/pooltool_community_edition

## Installation
Requires Python 3.8+

Tested on MacOS 10.14.6, Ubuntu 20.10, and 32-bit Raspberry Pi OS. No Windows solution currently.

```sudo apt-get install libffi-dev libssl-dev python3-dev python3-tk```

```git clone https://github.com/iamredbar/PoolTool.git```

```cd PoolTool```

```pip3 install -r requirements.txt```

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

PoolTool currently supports exchanging with liquidity pools and depositing to liquidity pools.

## WIP | NEW SCREENSHOTS SOON

### Please report any issues you have via Github. 
