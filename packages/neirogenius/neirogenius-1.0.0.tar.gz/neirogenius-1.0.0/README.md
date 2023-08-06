# ⚠️THE API IS PRIVATE AT THE MOMENT, YOU WILL NOT BE ABLE TO USE IT!

# NeirogeniusPY

NeirogeniusPY is a Python wrapper for the Neirogenius API.

Neurogenius is a discord bot created by [Pelfox](https://github.com/Pelfox) that entertains people. It generates funny
sentences using words from server members' messages.

![](https://i.imgur.com/z6jr2no.png)

# Installation

* Using PyPi

```
pip install neirogenius
```

* Using GitHub

```
git clone https://github.com/itsSourCream/NeirogeniusPY.git
cd neirogeniuspy
python setup.py install
```

# Example usage

```python
# Import the API class
from neirogenius import API

# Create an instance of the API class
api = API()

# Get the ID of the first guild
guild = api.get_statistic().guilds[0]['id']  # 677481923995500566

# Get the first message
message = api.get_messages(guild).messages[0]  # {'guild_id': 677481923995500566,
#                                                 'author_id': 943434038541172766,
#                                                 'timestamp': 1650860764,
#                                                 'content': 'Я думаю паяльник по ефектівней будет',
#                                                 'id': '626622dc4b21d121e6eae1b1'}

# Print message content
print(message['content'])  # "Я думаю паяльник по ефектівней будет"
```

# License

This project is licensed under
the [Apache License Version 2.0](https://github.com/itsSourCream/NeirogeniusAPI/blob/master/LICENSE).