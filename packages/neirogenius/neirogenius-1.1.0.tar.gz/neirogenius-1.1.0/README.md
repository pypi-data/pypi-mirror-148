[![CodeFactor](https://www.codefactor.io/repository/github/itssourcream/neirogeniuspy/badge)](https://www.codefactor.io/repository/github/itssourcream/neirogeniuspy)
![PyPI](https://img.shields.io/pypi/v/neirogenius)

# NeirogeniusPY

NeirogeniusPY is a Python wrapper for the Neirogenius API.

Neurogenius is a Discord bot created by [@Pelfox](https://github.com/Pelfox) that entertains people. It generates funny
sentences using words from server members' messages.

![](https://i.imgur.com/z6jr2no.png)

# Installation

* Using PyPi

```
pip install neirogenius
```

# Example usage

```python
# Import the API class.
from neirogenius import API

# Create an instance of the API class.
api = API()

# Get the ID of the first guild.
guild = api.get_statistic().guilds[0].name  # Some name.

# Get the first message.
message = api.get_messages(677481923995500566).messages[0]  # Instance of Message class.

# Print message content.
print(message.content)
```

# License

This project is licensed under
the [Apache License Version 2.0](https://github.com/itsSourCream/NeirogeniusAPI/blob/master/LICENSE).
