import logging
from telegram import Update, ChatMember, ParseMode
from telegram.ext import CallbackContext, Dispatcher, JobQueue, Updater, CommandHandler, MessageHandler, Filters, ChatMemberHandler
from datetime import timedelta
from telegram.error import BadRequest

# Define constants
APPROVED_CHAT_ID = -1002080839951  # Replace with your group chat ID
TARGET_TAG = "『ßᎬ么ᏚᎢ』"
SUDO_USERS = [6259443940]  # List of sudo user IDs
approved_users = set()  # Users exempted from the forbidden tag check

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Check all users for the forbidden tag and ban if necessary
def check_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id in SUDO_USERS:  # Ensure only sudo users can run this
        try:
            banned_users = []
            # Use get_chat_administrators to fetch admin list
            admins = context.bot.get_chat_administrators(chat_id)
            admin_ids = [admin.user.id for admin in admins]

            # Get all chat members using bot API
            members = context.bot.get_chat_members_count(chat_id)

            for i in range(members):
                try:
                    member = context.bot.get_chat_member(chat_id, i)
                    user = member.user

                    # Check if the user has the forbidden tag in their full name or username
                    if TARGET_TAG in user.full_name or (user.username and TARGET_TAG in user.username):
                        if user.id in SUDO_USERS:
                            context.bot.send_message(chat_id=chat_id, text=f"Alert: Sudo user {mention_html(user.id, user.full_name)} has the forbidden tag. No action taken.", parse_mode='HTML')
                        elif user.id in admin_ids:
                            context.bot.send_message(chat_id=chat_id, text=f"Alert: Admin {mention_html(user.id, user.full_name)} has the forbidden tag. No action taken.", parse_mode='HTML')
                        else:
                            context.bot.ban_chat_member(chat_id, user.id)
                            banned_users.append(user.full_name)

                except Exception as e:
                    logging.error(f"Error processing user {i}: {str(e)}")
                    continue

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

    # Skip processing for sudo users and approved users
    if user.id in SUDO_USERS or user.id in approved_users:
        return

    try:
        # Fetch the chat member object to get the user's status
        chat_member = context.bot.get_chat_member(chat_id, user.id)

        # Check if the user has the forbidden tag in their name or username
        if TARGET_TAG in user.full_name or TARGET_TAG in (user.username or ''):
            if chat_member.status in ['administrator', 'creator']:
                # Log admin with forbidden tag
                logging.info(f"Admin {user.full_name} has the forbidden tag, cannot ban.")
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Admin {user.mention_html()} has the forbidden tag '{TARGET_TAG}', but cannot be banned.",
                    parse_mode=ParseMode.HTML
                )
            else:
                # Ban the user
                logging.info(f"User {user.full_name} has the forbidden tag, banning.")
                context.bot.ban_chat_member(chat_id=chat_id, user_id=user.id)
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f"{user.mention_html()} has been banned for having the forbidden tag '{TARGET_TAG}' in their name.",
                    parse_mode=ParseMode.HTML
                )
    except BadRequest as e:
        logging.error(f"Error fetching chat member: {e.message}")


# When a new user joins, check if they have the forbidden tag
def approve_chat_join_request(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if chat_id == APPROVED_CHAT_ID:  # Check if the user joined the specific group
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

# Main function to start the bot
def main():
    # Initialize Updater and Dispatcher
    updater = Updater("5527818445:AAE7TLprBfyUuQvYZsaOesQ0F-9C2sl2I80", use_context=True)
    dispatcher = updater.dispatcher

    # Add command handler for /auth command
    dispatcher.add_handler(CommandHandler("auth", handle_auth, pass_args=True))

    # Add the handler to approve join requests and check for forbidden tags
    dispatcher.add_handler(ChatMemberHandler(approve_chat_join_request, ChatMemberHandler.MY_CHAT_MEMBER))

    # Add message handler to check for forbidden tags in chat messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_forbidden_tag))

    # Add the command handler for checking users
    dispatcher.add_handler(CommandHandler("check", check_users, filters=Filters.user(user_id=SUDO_USERS)))

    # Log the start of the bot
    logging.info("Bot started.")

    # Start the bot
    updater.start_polling()

    # Idle to keep the bot running
    updater.idle()

# Call the main() function when starting the script
if __name__ == '__main__':
    main()
