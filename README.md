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

Now you have to build [nsjail](https://github.com/google/nsjail.git) to use `exec` command of the bot.
First clone the repository:
```
$ git clone https://github.com/google/nsjail.git nsjail
```
Then build it and put the binary in `/usr/sbin`. You can tweak the path of the binary by editing the variable `NSJAIL_PATH` of [nsjail.py](cogs/helpers/snekbox/nsjail.py):
```
$ cd nsjail
$ make
$ mv nsjail /usr/sbin/nsjail
```
Now you can run the bot
```
$ python3 bot.py
```

# Build Using Docker
You can also run the bot using. To build the docker container execute the following command:
```
$ docker build -t noob-bot .
```

Run the docker container.
```
$ docker run -e "BOT_TOKEN=<your_bot_token> noob-bot
```