# Noob-Bot
A discord bot with lots of features.

# Build
At first install required python packages:
```
$ pip3 install -r requirements.txt
```

Now you have to set up 3 enviroment varibales.

First one is `BOT_TOKEN` which is your bot token.
```
$ export BOT_TOKEN=<your_bot_token>
```
Second one is `GOOGLE_API_KEY` which is your google api key for [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/)
```
$ export GOOGLE_API_KEY=<your_google_api_key>
```

Third one is `CX_TOKEN` which is your google custom search engine token for [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/)
```
$ export CX_TOKEN=<your_google_cx_token>
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
You can also run the bot using docker. To build the docker container execute the following command:
```
$ docker build -t noob-bot .
```

Run the docker container passing the required enviroment variables.
```
$ docker run -e "BOT_TOKEN=<your_bot_token>"\
                -e "GOOGLE_API_KEY=<your_google_api_key>"\
                -e "CX_TOKEN=<your_google_cx_token>"\
                noob-bot
```

More info on how to pass enviroment variables to docker can be found [here](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file).