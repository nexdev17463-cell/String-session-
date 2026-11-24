# Telegram Session Guide Bot

A small Telegram bot that displays a clear security warning and guides users to a **local-only** session generator.

## Security model

- The bot never asks for or receives a phone number, Telegram login code, 2-step verification password, or session string.
- The local generator runs on the account owner's trusted device.
- The generated session is printed locally and is not uploaded by this project.
- If you want the session in Telegram Saved Messages, send it there manually from your own Telegram account.
- Never paste a session string into this bot, a group, an issue, a log, or a public repository.

A String Session is a powerful account credential. Anyone who obtains it may be able to access your Telegram account. Use this only for your own account and revoke active sessions from Telegram Settings > Devices if you suspect exposure.

## 1. Create the Telegram bot

Create a bot with BotFather and copy its token. Add it to your GitHub repository as an Actions/repository secret named `BOT_TOKEN` only if you later configure a dedicated bot-running workflow. Do not commit tokens to source code.

## 2. Run the guide bot locally

Install Python 3.10+ and dependencies:

```bash
python -m pip install -r requirements.txt
```

Set the token as an environment variable:

- Linux/macOS: `export BOT_TOKEN="your_bot_token"`
- Windows PowerShell: `$env:BOT_TOKEN="your_bot_token"`

Then run:

```bash
python bot.py
```

The bot responds to `/start` with a warning and Continue/Cancel buttons.

## 3. Generate your own session locally

1. On your own trusted computer, install dependencies: `python -m pip install -r requirements.txt`.
2. Get your own API ID and API hash from https://my.telegram.org.
3. Run `python local_generator.py`.
4. Enter your API ID, API hash, phone number and the login code in the local terminal. If prompted, enter your 2-step verification password.
5. The session string is printed in that terminal. Keep it private and do not share it.
6. If you need it in Saved Messages, manually send it to Saved Messages from your own Telegram account.

The script uses an in-memory Pyrogram client and does not send the session string to this bot or to this repository.

## GitHub Actions

The included workflow validates Python syntax on pushes, pull requests and manual runs. It does **not** deploy a 24/7 bot. GitHub Actions runners are temporary; do not use workflow logs or artifacts to store session strings or other credentials.

## Commands

- `/start` — show the security warning and setup guidance.
