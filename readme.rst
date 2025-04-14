A discord bot for managing the server "Brac University Competitive Programming Workshop 2025"
=========================================

Main purpose of this bot was so that only registered users can access the server and the channels. Once the users join, they can verify themselves by inputing their email they used to register for the workshop. The bot will then check if the email is in the database, send them a verification code and then verify them by giving them @verified role.

Running the bot
---------------
- Get a discord bot token from the discord developer portal.
- Enable all privileged intents.
- Create a mongodb database
- Create an app for the email that will send the verification code.
- Create a .env file (follow .env-example) and fill in the required fields.
- Make sure venv is installed, then create a virtual environment using ``python -m venv venv`` or ``python3 -m venv venv`` in linux.
- Activate the virtual environment using ``venv\Scripts\activate`` in windows or ``source venv/bin/activate`` in linux.
- Install the required packages using ``pip install -r requirements.txt``. or ``pip3 install -r requirements.txt`` in linux.
- Run ``python main.py`` or ``python3 main.py`` in linux.
- To keep it running in background, use ``nohup python3 -u main.py > stdout.log &`` in linux.

