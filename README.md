<img width="822" alt="Screen Shot 2020-12-06 at 3 09 29 PM" src="https://user-images.githubusercontent.com/16945982/101292483-52b3aa00-37d5-11eb-91bd-d19311883fbe.png">

### How-to Use video here:

[![How To Use PoolTool for Liquidity Pools on the BitShares Blockchain](http://img.youtube.com/vi/1UNUVwYSjRo/0.jpg)](http://www.youtube.com/watch?v=1UNUVwYSjRo "How To Use PoolTool for Liquidity Pools on the BitShares Blockchain")

# PoolTool

A simple GUI tool to help anyone use Liquidity Pools on the BitShares blockchain.

Written entirely in Python, it will work on any platform that can run Python.

中文翻译如下

Telegram Group: https://t.me/pooltool_community_edition

## Installation
Requires Python 3.8+

Tested on MacOS 10.14.6, Ubuntu 20.10, and 32-bit Raspberry Pi OS. No Windows solution currently.

Linux install:

```sudo apt-get install libffi-dev libssl-dev python3-dev python3-tk```

```git clone https://github.com/iamredbar/PoolTool.git```

```cd PoolTool```

```pip3 install -r requirements.txt```

## Set up

You will need to set a default node using `uptick`. Syntax is like this:

```uptick set node <node_goes_here>```

Example:

```uptick set node 'wss://dex.iobanker.com/ws'```

**If this step is not done, it is very unlikely that it will work.**

(read more about `uptick` here: http://docs.uptick.rocks/en/latest/)

## Start Up

```python3 controller.py```

## Basic Walkthrough

Upon start up, you will need to select the pool you would like to use via the dropdown menu.

PoolTool currently supports exchanging with liquidity pools and depositing to liquidity pools.

## WIP | NEW SCREENSHOTS SOON

### Please report any issues you have via Github.


# 流动池工具
一个便于操作的比特股区块链AMM流动池界面工具。
Python编写，适用于能够运行Python的任意平台。
Telegram群：https://t.me/pooltool_community_edition

## 安装
需求：Python 3.8+
MacOS 10.14.6, Ubuntu 20.10, and 32-bit Raspberry Pi OS已测试。当前尚无Windows解决方案。

```sudo apt-get install libffi-dev libssl-dev python3-dev python3-tk```

```git clone https://github.com/iamredbar/PoolTool.git```

```cd PoolTool```

```pip3 install -r requirements.txt```

## 设置
你需要使用uptick设置一个默认的连接节点.语法如下：
```uptick set node <node_goes_here>```

例子:

```uptick set node 'wss://api.bts.mobi/ws'```

**如果这一步没有完成，将不能正常运行**

(更多关于 uptick : http://docs.uptick.rocks/en/latest/)

## 开始
```python3 controller.py```

## 基本操作
启动后，你可以按照你的需求在面板下拉菜单上选择流动池。

流动池工具当前支持流动池交易及充值。

## WIP | NEW SCREENSHOTS SOON
### Please report any issues you have via Github.
