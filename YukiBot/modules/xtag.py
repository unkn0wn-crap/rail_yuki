# import section
import html
import logging
from telegram import Update, ChatMember, ParseMode
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ChatMemberHandler
from telegram.error import BadRequest
from YukiBot import pbot as yuki
from YukiBot import StartTime, dispatcher
from YukiBot import DRAGONS as SUDO_USERS

# Constants
APPROVED_CHAT_ID = -1001801945066  # Replace with your specific group chat ID
TARGET_TAG = "『ßᎬ么ᏚᎢ』"
approved_users = set()  # Users exempted from the forbidden tag check


# Function to check users for the forbidden tag and ban them
def check_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Ensure the command is only run in the specific group
    if chat_id != APPROVED_CHAT_ID:
        context.bot.send_message(chat_id=chat_id, text="This command can only be used in the authorized group.")
        return

    if user_id in SUDO_USERS:
        banned_users = []

        try:
            # Fetch all chat members
            members = context.bot.get_chat_administrators(chat_id)
            for member in members:
                user = member.user

                # Check if the user has the forbidden tag
                if TARGET_TAG in user.full_name or (user.username and TARGET_TAG in user.username):
                    if member.status not in ['administrator', 'creator']:  # Don't ban admins
                        context.bot.ban_chat_member(chat_id=chat_id, user_id=user.id)
                        banned_users.append(user.full_name)

            if banned_users:
                report_message = "Banned users with the forbidden tag:\n" + "\n".join(banned_users)
                context.bot.send_message(chat_id=chat_id, text=report_message)
            else:
                context.bot.send_message(chat_id=chat_id, text="No users were banned.")
        except Exception as e:
            logging.error(f"Error while checking users: {str(e)}")
            context.bot.send_message(chat_id=chat_id, text="An error occurred while checking users.")
    else:
        context.bot.send_message(chat_id=chat_id, text="You do not have permission to use this command.")


# Function to handle /auth -yes and /auth -no commands
def handle_auth(update: Update, context: CallbackContext):
    sudo_user_id = update.effective_user.id

    # Ensure only sudo users can execute this command
    if sudo_user_id not in SUDO_USERS:
        update.message.reply_text("You are not authorized to use this command.")
        return

    # Extract command and arguments
    command = context.args[0] if len(context.args) > 0 else None
    user_to_auth = None

    # If command is used in reply to a user
    if update.message.reply_to_message:
        user_to_auth = update.message.reply_to_message.from_user
    elif len(context.args) > 1:
        # If username or user_id is specified
        try:
            user_to_auth = context.bot.get_chat_member(APPROVED_CHAT_ID, context.args[1]).user
        except BadRequest as e:
            update.message.reply_text(f"Error: {e.message}")
            return

    if not user_to_auth:
        update.message.reply_text("Please reply to a user or provide a username/user_id.")
        return

    # Handle the /auth -yes and /auth -no commands
    if command == "-yes":
        approved_users.add(user_to_auth.id)
        update.message.reply_text(f"{user_to_auth.full_name} has been approved.")
    elif command == "-no":
        if user_to_auth.id in approved_users:
            approved_users.remove(user_to_auth.id)
        context.bot.ban_chat_member(chat_id=APPROVED_CHAT_ID, user_id=user_to_auth.id)
        update.message.reply_text(f"{user_to_auth.full_name} has been banned.")
    else:
        update.message.reply_text("Unknown command. Use /auth -yes or /auth -no.")


# Function to handle all messages and check if a user has the forbidden tag
def check_forbidden_tag(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Ensure this only runs in the specific group
    if chat_id != APPROVED_CHAT_ID:
        return

    # Skip processing for sudo users and approved users
    if user.id in SUDO_USERS or user.id in approved_users:
        return

    try:
        # Fetch the chat member object to get the user's status
        chat_member = context.bot.get_chat_member(chat_id, user.id)

        # Check if the user has the forbidden tag in their name or username
        if TARGET_TAG in user.full_name or TARGET_TAG in (user.username or ''):
            if chat_member.status in ['administrator', 'creator']:
                logging.info(f"Admin {user.full_name} has the forbidden tag, cannot ban!")
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Admin {user.mention_html()} has the forbidden tag '{TARGET_TAG}', but cannot be banned.",
                    parse_mode=ParseMode.HTML
                )
            else:
                logging.info(f"User {user.full_name} has the forbidden tag, banning.")
                context.bot.ban_chat_member(chat_id=chat_id, user_id=user.id)
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"{user.mention_html()} has been banned for having the forbidden tag '{TARGET_TAG}' in their name.",
                    parse_mode=ParseMode.HTML
                )
    except BadRequest as e:
        logging.error(f"Error fetching chat member: {e.message}")


# Function to approve or reject chat join requests based on the forbidden tag
def approve_chat_join_request(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Only handle join requests in the approved chat
    if chat_id == APPROVED_CHAT_ID:
        if TARGET_TAG in user.full_name or TARGET_TAG in (user.username or ''):
            if user.id not in approved_users:
                logging.info(f"User {user.full_name} was banned for having the forbidden tag '{TARGET_TAG}' upon joining.")
                context.bot.ban_chat_member(chat_id=chat_id, user_id=user.id)
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"{user.mention_html()} has been banned for having the forbidden tag '{TARGET_TAG}' in their name.",
                    parse_mode=ParseMode.HTML
                )
            else:
                logging.info(f"Approved user {user.full_name} joined the chat with the forbidden tag.")
        else:
            logging.info(f"User {user.full_name} was approved to join the chat.")
            context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user.id)


# Dispatcher and handlers
dispatcher.add_handler(CommandHandler("auth", handle_auth, pass_args=True))
dispatcher.add_handler(ChatMemberHandler(approve_chat_join_request, ChatMemberHandler.MY_CHAT_MEMBER))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_forbidden_tag))
dispatcher.add_handler(CommandHandler("check", check_users))

__handlers__ = [
    CommandHandler("auth", handle_auth),
    CommandHandler("check", check_users),
]

__mod_name__ = "UɴOғғɪᴄɪᴀʟ"

__help__ = """
*FOR SUDO USERS*
`/auth -yes @username` ➥ Approve the user to send messages even with the tag.
`/auth -no @username` ➥ Ban the user with the forbidden tag.
"""