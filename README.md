![PoolTool 2.0.0](https://user-images.githubusercontent.com/16945982/108139311-715fd800-7085-11eb-90bf-61ea19ae9fb5.png)
___

ACCOUNT AND ACTIVE KEY ARE NOT PERSISTENT, YOU WILL NEED TO
ENTER THEM EACH TIME YOU LAUNCH THE APP (but not every transaction. that's a win).

If / when Beet receives an update,
Beet will be used. More info about Beet here:
[Beet GitHub Page](https://github.com/bitshares/beet)

---

## First Time Setup Instructions:
### Environment Setup
Before doing anything else, make sure to create a virtual environment.
In this case, we are creating an environment named `env`:

```shell
python3 -m venv env
```

Activate the newly created environment:

```shell
source env/bin/activate
```

### Installation
Method 1: Use `pip` to download and install from PyPI:
```shell
python3 -m pip install PoolTool
```

Method 2: Download and install from source:
```shell
git clone https://github.com/iamredbar/PoolTool
cd PoolTool/
python3 -m pip install .
```

---

## Running PoolTool after First Time Setup is complete

Make sure you have your environment active (if it's not already):

```shell
source env/bin/activate
```

Run PoolTool:

```shell
PoolTool
```

___

## Using:

You will need to enter your account and active key via the menu in the top right.
Here you can also set a node to use if you would prefer a different node
than the default one (wss://api.iamredbar.com/ws).

___

### Links:

Telegram: https://t.me/pooltool_community_edition

Issues: https://github.com/iamredbar/PoolTool/issues