# Plant ID Bot
## A plant identification bot for your Discord server.

Plant ID Bot identifies plants from photos of their organs, passing to the [Plantnet API] for identification. This bot was written for [Sustainable Living Hub](https://discord.com/invite/gQU5yWg)

## Features

- Takes the message picture attachments and attempts to identify them
- Returns a suggested plant name and up to 2 alternatives, with a percentage confidence rating
- Plant names are given in latin with a list of possible common names
- Provides links to [GBIF] and [PFAF] for the identified plant

## Prerequisites

Plant ID Bot uses a small number of prerequisites in order to work properly:

- [Pycord] -  a modern, easy to use, feature-rich, and async ready API wrapper for Discord, written in Python
- [Beautiful Soup] - a python library for pulling data out of HTML and XML files
- [python-dotenv] - for reading local .env files during development


## Installation

To add the Plant ID bot from this repository to your discord server, use this [invite](https://discord.com/api/oauth2/authorize?client_id=948227126094598204&permissions=19520&scope=bot).

If you fork this repository and wish to host your own version of this bot, you will need to:

- Create a new account at [Plantnet API]
- Create a new application and bot at the [Discord Developer Portal](https://discord.com/developers/applications). Follow this [guide](https://realpython.com/how-to-make-a-discord-bot-python/) if you are unsure.
- create a local .env file to store `DISCORD_TOKEN` and `PLANTNET_API_KEY`. Add both your bot's secret token and PlantNet API key here repectively
- Enable the bot permissions 'Read Messages/View Channels', 'Send Messages', 'Embed Links', 'Add Reactions'
- Host the files on your platform of choice. A procfile is included if you wish to use [Heroku](https://www.heroku.com)
- Add the bot's secret token and your PlantNet API key to your platform's environment variables under the keys `DISCORD_TOKEN` and `PLANTNET_API_KEY`. 

## Development

Want to contribute? Simply fork, clone, edit and then create a pull request. Details of how to do this can be found [here](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github).

## Credits
- [themanifold](https://github.com/themanifold) who cast his careful eye over the code, making sure that I wasn't making any obvious errors, and for making my todo list longer each day
- [Country Roles](https://github.com/dolphingarlic/country-roles) from which my knowledge of Discord.py 'cogs' was solidified. Their implementation of 'BotInfo' was used to create more information on the bot, and generally helped me clean up my code 

## License

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [git-repo-url]: <https://github.com/TheRealOwenRees/plantID_discordbot>
   [Plantnet API]: <https://my.plantnet.org/>
   [Pycord]: <https://pycord.dev/>
   [GBIF]: <https://pypi.org/project/python-dotenv/>
   [PFAF]: <https://pfaf.org>
   [python-dotenv]: <https://pypi.org/project/python-dotenv/>
   [Beautiful Soup]: <https://beautiful-soup-4.readthedocs.io/en/latest/>
