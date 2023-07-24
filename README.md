# 32a-discord-bot
A Discord.py bot used for managing academic servers at UC Davis.

# Documentation
## Overview
The bot is designed to facilitate interaction between students and tutors in a learning community hosted on a Discord server. The bot manages channels for asking questions, answering them, and registering for tutoring sessions. It ensures the proper flow of interaction, keeping the server organized and efficient.

## Initialization
The bot is initialized with a token, which is not provided in the code for security reasons.

```python
bot = interactions.Client(token='<token>')
```

The waiting_list is a global list that will hold the queue of students waiting for a tutor.

```python
global waiting_list
waiting_list = []
```
Two button objects are defined for user interaction: `public_button` and `private_button`.

## Utility Functions
There are several utility functions that help in retrieving information about categories and roles in the Discord server:

1. `get_categories(ctx)`: This function returns the IDs of the channels "ASK HERE", "ACTIVE QUESTIONS", "TUTORING", and "ANSWERED QUESTIONS".

2. `tutor_check(ctx)`: This function checks if a user has the role of "Tutor" and returns a boolean value.

3. `get_relevant_roles(ctx)`: This function returns the IDs of the roles "Tutor", "@everyone", "Student", and "Active Tutor".

## Commands
Commands in the bot are defined using the `@bot.command` decorator. Here are the commands defined in the bot:

1. `resolve`: This command is used to close a channel. It checks if the channel is open and if the user executing the command has the necessary permissions. If the channel is private, it deletes the message history.

2. `register`: This command allows a user to get in line for a tutor. It adds the user to the waiting_list and notifies them of their position.

3. `next`: This command allows a tutor to notify the next student in line that they are ready. It checks if the user executing the command is a tutor and if there is a student in line.

4. `signin`: This command allows a tutor to sign into their tutoring shift. It checks if the user executing the command is a tutor and if they are not already signed in.

5. `signout`: This command allows a tutor to sign out of their tutoring shift. It checks if the user executing the command is a tutor and if they are not already signed out.

6. `forceresolve`: This is a debug command reserved for use by admins to force any channel to become a new Ask Here channel. If a channel ever fails to resolve into a proper state, an admin can use this command to fix it.

## Button Responses
There are two button responses defined in the bot, `public_button_response` and `private_button_response`. These responses are triggered when a user clicks on the respective button. They handle the process of opening a question in a public or private channel.

## Running the Bot
The bot is started with the `bot.start()` command at the end of the script.

## Note
Please remember to replace `<token>` with the actual bot token in the `interactions.Client(token='<token>')` line before running the bot.
