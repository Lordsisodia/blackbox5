#!/usr/bin/env python3
"""
Message Saver for MoltBot
Saves Telegram messages to files for later review
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7643203581")
BB5_DIR = Path("/opt/blackbox5")
MESSAGES_FILE = BB5_DIR / "agents" / "moltbot-autonomous" / "saved-messages.jsonl"
LAST_UPDATE_ID_FILE = BB5_DIR / "agents" / "moltbot-autonomous" / ".last_update_id"


def get_last_update_id():
    """Get the last processed update ID"""
    if LAST_UPDATE_ID_FILE.exists():
        try:
            return int(LAST_UPDATE_ID_FILE.read_text().strip())
        except:
            return 0
    return 0


def save_last_update_id(update_id):
    """Save the last processed update ID"""
    LAST_UPDATE_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
    LAST_UPDATE_ID_FILE.write_text(str(update_id))


def save_message(message_data):
    """Save a message to the JSONL file"""
    MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MESSAGES_FILE, "a") as f:
        f.write(json.dumps(message_data, default=str) + "\n")


def process_messages():
    """Check for and save new messages"""
    last_id = get_last_update_id()

    try:
        response = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
            params={"offset": last_id + 1, "limit": 100},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            print(f"Telegram API error: {data}")
            return

        updates = data.get("result", [])
        if not updates:
            return

        for update in updates:
            update_id = update["update_id"]

            if "message" not in update:
                save_last_update_id(update_id)
                continue

            message = update["message"]
            chat_id = message.get("chat", {}).get("id")

            # Only save messages from authorized chat
            if str(chat_id) != TELEGRAM_CHAT_ID:
                save_last_update_id(update_id)
                continue

            # Build message record
            msg_data = {
                "saved_at": datetime.now().isoformat(),
                "update_id": update_id,
                "message_id": message.get("message_id"),
                "date": message.get("date"),
                "text": message.get("text", ""),
                "from": {
                    "id": message.get("from", {}).get("id"),
                    "username": message.get("from", {}).get("username"),
                    "first_name": message.get("from", {}).get("first_name")
                },
                "chat": {
                    "id": chat_id,
                    "type": message.get("chat", {}).get("type"),
                    "title": message.get("chat", {}).get("title")
                }
            }

            # Add topic info if present
            if "message_thread_id" in message:
                msg_data["topic_id"] = message["message_thread_id"]

            # Save the message
            save_message(msg_data)
            print(f"Saved message {message.get('message_id')}: {msg_data['text'][:50]}...")

            # Update last ID
            save_last_update_id(update_id)

    except Exception as e:
        print(f"Error processing messages: {e}")


def list_saved_messages(limit=20):
    """List recently saved messages"""
    if not MESSAGES_FILE.exists():
        print("No messages saved yet")
        return []

    messages = []
    with open(MESSAGES_FILE, "r") as f:
        for line in f:
            try:
                messages.append(json.loads(line.strip()))
            except:
                continue

    return messages[-limit:]


def search_messages(query, limit=50):
    """Search saved messages for a query"""
    if not MESSAGES_FILE.exists():
        return []

    matches = []
    with open(MESSAGES_FILE, "r") as f:
        for line in f:
            try:
                msg = json.loads(line.strip())
                if query.lower() in msg.get("text", "").lower():
                    matches.append(msg)
                    if len(matches) >= limit:
                        break
            except:
                continue

    return matches


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            messages = list_saved_messages(limit)
            for msg in messages:
                print(f"[{msg['saved_at']}] {msg.get('from', {}).get('username', 'Unknown')}: {msg['text'][:100]}")

        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: message-saver.py search <query>")
                sys.exit(1)
            query = sys.argv[2]
            matches = search_messages(query)
            for msg in matches:
                print(f"[{msg['saved_at']}] {msg['text'][:200]}")

        elif command == "process":
            process_messages()
            print("Messages processed")

        else:
            print(f"Unknown command: {command}")
            print("Commands: list [limit], search <query>, process")
    else:
        # Default: process messages
        process_messages()
