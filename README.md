# Noob-Bot
A discord bot with lots of features.

# Build
At first install required python packages:
```
$ pip3 install -r requirements.txt
```

Now you have to set up a enviroment varibale named **BOT_TOKEN**
```
$ export BOT_TOKEN=<your_bot_token>
```

Now you have to set up [nsjail](https://github.com/google/nsjail.git) to use `exec` command of the bot. A shell script is availlable to build nsjail.
```
$ ./installNsJail.sh
```
Now you can run the bot
```
$ python3 bot.py
```

# Build Using Docker
A docker image is also available. To build it execute the following command:
```
$ docker build -t noob-bot .
```

Run the docker container.
```
$ docker run -e "BOT_TOKEN=<your_bot_token> noob-bot
```