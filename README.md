# HTCondorReporter

A simple monitoring tool for jobs that were submitted to CERN's HTCondor infrastructure. It sends status reports to a Telegram bot.


# Quick setup guide

## Install dependencies

This tool requires the *requests* library. Install it by running
```
pip install --user requests
```


## Create and configure a Telegram bot

The setup of a Telegram bot requires two steps: getting an API token for your bot from Telegram and registering your bot connection details in `Tools/python/telegramUser.py`.

### Creating a Telegram bot and getting its API token

Visit telegram.me/botfather and type `/newbot`. Then, simply follow the instructions of the botfather.

You will receive an API token in this process. Keep it, we will need it in a minute!

Next, start chatting with your newly created bot by clicking the "t.me/[yourNewBot]" link which the botfather has sent in the same message that contained the API token.

As a last step, a user ID has to be retrieved. This ID can be found by visiting https://api.telegram.org/bot[yourAPItoken]/getme, where you have to search for the integer number corresponding to the "id" data entry.

Having obtained API token and user ID for your new Telegram bot, let's proceed to the final setup step.

### Registering your Telegram bot in the software

Copy the file `template.telegramUser.py` to `telegramUser.py`, open it and enter your API token and your user ID.

> Attention: Never push your `telegramUser.py` file to GitHub etc. as it contains sensitive information.


## Integration in CMSSW

If you are a CMS user, you might want to integrate this software into your CMSSW environment. To do this, simply move the entire folder with this software to the `src/` folder in your CMSSW release folder and compile with `scram b -j 8`.


# Running the software

In order to start monitoring your Condor jobs, go to `Tools/scripts/` and run
```./runCondorReporter.sh```
(or, if you have complied with `scram`, simply run `runCondorReporter.sh`).
