import shutil, psutil
import signal
import pickle

from os import execl, path, remove
from sys import executable
import time

from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, delete


@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>Uᴘᴛɪᴍᴇ:</b> {currentTime}\n' \
            f'<b>Dɪꜱᴋ ꜱᴘᴀᴄᴇ:</b> {total}\n' \
            f'<b>Uꜱᴇᴅ:</b> {used}  ' \
            f'<b>Fʀᴇᴇ:</b> {free}\n\n' \
            f'Dᴀᴛᴀ ᴜꜱᴀɢᴇ\n<b>Uᴘʟᴏᴀᴅ:</b> {sent}\n' \
            f'<b>Dᴏᴡɴʟᴏᴀᴅ:</b> {recv}\n\n' \
            f'<b>CPU:</b> {cpuUsage}% ' \
            f'<b>RAM:</b> {memory}% ' \
            f'<b>Dɪꜱᴋ:</b> {disk}%'
    sendMessage(stats, context.bot, update)


@run_async
def start(update, context):
    start_string = f'''
Tʜɪꜱ ɪꜱ ᴀ ʙᴏᴛ ᴡʜɪᴄʜ ᴄᴀɴ ᴍɪʀʀᴏʀ a̶l̶l̶ ̶y̶o̶u̶r̶ ̶l̶i̶n̶k̶s̶ ᴡʜᴏʟᴇ ᴜɴɪᴠᴇʀꜱᴇ  ᴛᴏ Gᴏᴏɢʟᴇ ᴅʀɪᴠᴇ!
Tʏᴘᴇ /{BotCommands.HelpCommand} ᴛᴏ ɢᴇᴛ ᴀ ʟɪꜱᴛ ᴏғ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ
Bᴏᴛ ʙʏ @unkusr
'''
    sendMessage(start_string, context.bot, update)


@run_async
def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update, context):
    help_string = f'''
/{BotCommands.MirrorCommand} [ᴅᴏᴡɴʟᴏᴀᴅ_ᴜʀʟ][ᴍᴀɢɴᴇᴛ_ʟɪɴᴋ]: Sᴛᴀʀᴛ ᴍɪʀʀᴏʀɪɴɢ ᴛʜᴇ ʟɪɴᴋ ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ

/{BotCommands.UnzipMirrorCommand} [ᴅᴏᴡɴʟᴏᴀᴅ_ᴜʀʟ][ᴍᴀɢɴᴇᴛ_ʟɪɴᴋ] : ꜱᴛᴀʀᴛꜱ ᴍɪʀʀᴏʀɪɴɢ ᴀɴᴅ ɪғ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ғɪʟᴇ ɪꜱ ᴀɴʏ ᴀʀᴄʜɪᴠᴇ, ᴇxᴛʀᴀᴄᴛꜱ ɪᴛ ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ

/{BotCommands.TarMirrorCommand} [ᴅᴏᴡɴʟᴏᴀᴅ_ᴜʀʟ][ᴍᴀɢɴᴇᴛ_ʟɪɴᴋ]: ꜱᴛᴀʀᴛ ᴍɪʀʀᴏʀɪɴɢ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ᴀʀᴄʜɪᴠᴇᴅ (.tar) ᴠᴇʀꜱɪᴏɴ ᴏғ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ

/{BotCommands.WatchCommand} [ʏᴏᴜᴛᴜʙᴇ-ᴅʟ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ]: Mɪʀʀᴏʀ ᴛʜʀᴏᴜɢʜ ʏᴏᴜᴛᴜʙᴇ-ᴅʟ

/{BotCommands.TarWatchCommand} [ʏᴏᴜᴛᴜʙᴇ-ᴅʟ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ]: Mɪʀʀᴏʀ ᴛʜʀᴏᴜɢʜ ʏᴏᴜᴛᴜʙᴇ-ᴅʟ ᴀɴᴅ ᴛᴀʀ ʙᴇғᴏʀᴇ ᴜᴘʟᴏᴀᴅɪɴɢ

/{BotCommands.CancelMirror} : Uꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡɪᴛʜ ᴘʀᴏᴠɪᴅᴇᴅ GID ᴛᴏ ᴄᴀɴᴄᴇʟ ʏᴏᴜʀ ᴍɪʀʀᴏʀ ᴘʀᴏᴄᴇꜱꜱ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ

/{BotCommands.StatusCommand}: Sʜᴏᴡꜱ ᴀ ꜱᴛᴀᴛᴜꜱ ᴏғ ᴀʟʟ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅꜱ

/{BotCommands.ListCommand} [ꜱᴇᴀʀᴄʜ ᴛᴇʀᴍ]: Sᴇᴀʀᴄʜᴇꜱ ᴛʜᴇ ꜱᴇᴀʀᴄʜ ᴛᴇʀᴍ ɪɴ ᴛʜᴇ Gᴏᴏɢʟᴇ ᴅʀɪᴠᴇ, ɪғ ғᴏᴜɴᴅ ʀᴇᴘʟɪᴇꜱ ᴡɪᴛʜ ᴛʜᴇ ʟɪɴᴋ

/{BotCommands.StatsCommand}: Sʜᴏᴡꜱ ꜱᴛᴀᴛꜱ ᴏғ ᴛʜᴇ ᴍᴀᴄʜɪɴᴇ ᴡʜᴇʀᴇ ᴛʜᴇ ʙᴏᴛ ɪꜱ ʜᴏꜱᴛᴇᴅ ᴏɴ

/{BotCommands.AuthorizeCommand}: Aᴜᴛʜᴏʀɪᴢᴇ ᴀ ᴄʜᴀᴛ ᴏʀ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ (Bʏ ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ)

/{BotCommands.LogCommand}: Gᴇᴛ ᴀ ʟᴏɢ ғɪʟᴇ ᴏғ ᴛʜᴇ ʙᴏᴛ (Bʏ ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ)

'''
    sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
