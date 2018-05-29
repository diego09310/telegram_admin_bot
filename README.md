# AdminBot
Telegram bot that simply notifies admins in groups (Admins or a list of users configured in groups.json).

## Configuration
There are two configuration files:  
**config.py**: In this file you need to configure the bot token, log level, log file and unauthorized log file, and the json file containing the information of the admins and the groups. An empty example is provided (config\_example.py, which should be renamed to config.py).  
**groups.json**: This file contains the information related to the groups using this bot: name, id, link, and the list of admins with their data: id and name. An empty example is provided (groups\_example.json, which should be renamed to groups.json). 

## Commands
**/spam, /admins, /notificar\_admins, /notify\_admins**: Notify the admins listed in groups.json for that group. This command can only be used in a group that is in groups.json.  
**@admins**: same behavior as previous command, though it won't work if the bot is in privacy mode in the group.  
**/help**: shows a description of the commands to notify the admins.  

## Logs
Two log files are generated: regular logfile, with the information from the logger and unauthorized log, with a list of "unauthorized" access attempts.

## Create systemd service
To create a service to control the bot in systemd, copy the file `admin\_bot.service` to `/etc/systemd/system/` and change `USERNAME` and `FULL_PATH_TO_EXECUTABLE`. Also edit the file `launcher.sh` with the correct path.
Use `sudo systemctl daemon-reload` to reload the services, then use `systemctl <command> admin_bbot.service` with `enable` for start at boot, `start` to start it and `stop` to stop it.

## Future
I have some ideas I'd like to implement. If I have time and I'm motivated or someone wants to help.  
Ideas:  
-Add admins with the bot without touching the config files.  
-Command to list admins in a group.  
-Time range in which each admin can be notified.  
