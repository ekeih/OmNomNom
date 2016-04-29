# OmNomNom

OmNomNom is a Telegram bot that can tell you what you can eat in some canteens in Berlin (Germany). You can invite the bot to a group or ask it directly.

## How to use it
Usually you do not need to run the bot yourself. You can just talk to the @OmnBot in Telegram. Feel free to invite it in your groups. But if you want to run it anyways or would like to improve the code you can do so by following these steps.

This assumes that you use virtualenv and virtualenvwrapper. Otherwise you can use virtualenv directly without virtualenvwrapper or install the dependencies global.

At first you have to create a bot by talking to Telegrams [BotFather](https://core.telegram.org/bots#6-botfather). Copy your access token and keep it a secret!


```bash
# Create a new env
$ mkvirtualenv omnomnom

# Or use an existing one
$ workon omnomnom

# Checkout the repository
(omnomnom) $ git clone https://github.com/ekeih/OmNomNom.git
(omnomnom) $ cd OmNomNom

# Create a configuration file with your access token
# This line would add your access token to your shell history.
# It would be clever to avoid this by using an editor 
# or temporary disabling the history.
$ echo "AUTH_TOKEN = 'YOUR_ACCESS_TOKEN'" > config.py

# Install dependencies
(omnomnom) $ pip install -r requirements.txt

# Run OmNomNom
(omnomnom) $ python3 main.py
```


## Developer
* Max Rosin
* Christian Beneke
* Matthias Loibl

## License

```
A simple Telegram bot to get canteen information.
Copyright (C) 2016  Max Rosin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
