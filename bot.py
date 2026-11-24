import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("session-guide-bot")

WARNING = (
    "⚠️ STRING SESSION SECURITY WARNING\n\n"
    "A String Session can give someone access to your Telegram account. "
    "Treat it like your account password. Never share it with strangers, "
    "bots, groups, or support staff. Anyone who gets it may be able to "
    "control your account.\n\n"
    "This bot will NEVER ask for your phone number, login code, 2-step "
    "verification password, or String Session."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("I Understand — Continue", callback_data="continue"),
                InlineKeyboardButton("Cancel", callback_data="cancel"),
            ]
        ]
    )
    await update.effective_message.reply_text(WARNING, reply_markup=keyboard)


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        await query.edit_message_text(
            "Cancelled. No account details were requested or collected."
        )
        return

    if query.data == "continue":
        await query.edit_message_text(
            "✅ You can continue with a local-only setup.\n\n"
            "1. Open this repository's README: "
            "https://github.com/nexdev17463-cell/String-session-\n"
            "2. Follow the Local Generator instructions on your own trusted "
            "computer. Your login code and 2-step password stay on your device.\n"
            "3. Keep the generated session private. If you need it in Saved "
            "Messages, send it there yourself from your own Telegram account.\n\n"
            "This bot cannot generate, receive, store, or forward your session."
        )


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    log.info("Starting safe session guide bot")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
