"""Generate a Pyrogram session locally on the account owner's device.

This script does not send credentials or the resulting session to any server.
Keep the resulting session string private. Anyone possessing it may access
your Telegram account.
"""
import asyncio
import getpass
import os
import sys

from pyrogram import Client


def required_int(name: str) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        value = input(f"{name}: ").strip()
    try:
        return int(value)
    except ValueError as exc:
        raise SystemExit(f"{name} must be an integer") from exc


def required_text(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        value = getpass.getpass(f"{name} (input hidden): ").strip()
    if not value:
        raise SystemExit(f"{name} is required")
    return value


async def main() -> None:
    print("LOCAL TELEGRAM SESSION GENERATOR")
    print("Only continue on your own trusted device.")
    print("Never share the generated session string.\n")

    api_id = required_int("API_ID")
    api_hash = required_text("API_HASH")
    phone = input("Phone number with country code (e.g. +91...): ").strip()

    if not phone.startswith("+"):
        raise SystemExit("Enter the phone number with its country code, starting with +")

    client = Client(
        name="my_telegram_account",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    )

    try:
        await client.connect()
        sent = await client.send_code(phone)
        code = getpass.getpass("Telegram login code (input hidden): ").strip()

        try:
            await client.sign_in(phone, sent.phone_code_hash, code)
        except Exception as exc:
            # Pyrogram raises SessionPasswordNeeded for accounts with 2-step verification.
            from pyrogram.errors import SessionPasswordNeeded

            if not isinstance(exc, SessionPasswordNeeded):
                raise
            password = getpass.getpass("Telegram 2-step verification password: ")
            await client.check_password(password)

        session_string = await client.export_session_string()
        print("\nSESSION STRING (KEEP PRIVATE):\n")
        print(session_string)
        print("\nCopy it only into a private, secure place you control.")
        print("If you want it in Saved Messages, send it there manually.")
    finally:
        if client.is_connected:
            await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
