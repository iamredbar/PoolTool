![PoolTool 2.0.0](https://user-images.githubusercontent.com/16945982/108139311-715fd800-7085-11eb-90bf-61ea19ae9fb5.png)
___

ACCOUNT AND ACTIVE KEY ARE NOT PERSISTENT, YOU WILL NEED TO
ENTER THEM EACH TIME YOU LAUNCH THE APP (but not every transaction. that's a win).

If / when Beet receives an update,
Beet will be used. More info about Beet here:
[Beet GitHub Page](https://github.com/bitshares/beet)

---

## First Time Setup Instructions:
Download software from GitHub:
```shell
git clone https://github.com/iamredbar/PoolTool
```

Once downloaded, make sure to change to that directory:

```shell
cd PoolTool/
```

Before installing the requirements make sure to create a virtual environment.
in this case, we are creating an environment named `env`:

```shell
python3 -m venv env
```

Activate the newly created environment and install the requirements:

```shell
source env/bin/activate
pip3 install -r requirements.txt
```

---

## Running PoolTool after First Time Setup is complete:

Make sure you have your environment active (if it's not already):

```shell
source env/bin/activate
```

Run PoolTool:

```shell
./PoolTool
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