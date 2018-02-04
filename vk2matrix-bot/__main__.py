# -*- coding: utf-8 -*-
"""
Our main file!
"""
import logging
import signal
import sys
import time
from typing import Dict

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mcommand_handler import MCommandHandler
from matrix_client.room import Room

try:
    from . import config
except ImportError:
    import config

EXIT_SUCCESS = 0  # By SIGINT/SIGTERM, successfully
EXIT_ENV = 1  # Incorrect ENV variables
EXIT_VK_API = 2  # vk_api error
EXIT_MATRIX_API = 4  # matrix_bot_api error
EXIT_UNKNOWN = 128  # WTF?!

# event Dict:
# {
#   'origin_server_ts':10000000000,
#   'sender':'@username:matrix.org',
#   'event_id':'$ididid:matrix.org',
#   'unsigned':{
#     'age':602
#   },
#   'content':{
#     'body':'!ping',
#     'msgtype':'m.text'
#   },
#   'type':'m.room.message',
#   'room_id':'!ololololo:matrix.org'
# }


def bot_cmd_ping_echo(room: Room, event: Dict[str, str]):
    """
    Check bot availability, echo text.

    :param Room room: Matrix room
    :param dict event: event content
    """
    # noinspection PyTypeChecker
    room.send_html("ALIVE!<br/>"
                   "<b>You sent:</b> {}".format(event["content"]["body"]))


def register_bot_callbacks(bot: MatrixBotAPI):
    """
    Define all handlers and register callbacks.

    :param MatrixBotAPI bot: bot instance
    """
    bot.add_handler(MCommandHandler('ping', bot_cmd_ping_echo))


# noinspection PyBroadException
def main() -> int:
    """
    Our main() function!

    :return: exit code
    :rtype: int
    """
    log.info("Init MatrixBotAPI...")
    try:
        bot = MatrixBotAPI(config.USERNAME, config.PASSWORD, config.SERVER)
        register_bot_callbacks(bot)
        bot.start_polling()
        log.info("...success, started polling")
    except:
        log.critical("...failure!\nDetails:\n", exc_info=1)
        return EXIT_MATRIX_API

    log.info("Suspending MainThread")
    while True:
        try:
            time.sleep(2.628e+6)  # Approximately 1 month...
        except SystemExit:
            return EXIT_SUCCESS
        log.info("A month passed, lol~")


# noinspection PyUnusedLocal
def exit_handler(sig, frame):
    """
    SIGINT (^C)/SIGTERM handler for graceful shutdown.
    """
    log.info('Bye!')
    sys.exit(EXIT_SUCCESS)


if __name__ == '__main__':
    print("init...")

    l_logger = logging.getLogger()
    l_logger.setLevel(config.LOG_LEVEL)
    l_logger_sh = logging.StreamHandler()
    l_logger_sh.setFormatter(logging.Formatter(config.LOG_FORMAT))
    l_logger_sh.setLevel(config.LOG_LEVEL)
    l_logger.addHandler(l_logger_sh)

    log = l_logger

    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    # noinspection PyBroadException
    try:
        status = main()
    except:
        log.critical("Unknown exception was caught!\n"
                     "You can report issue w/ following information at:\n"
                     "https://github.com/saber-nyan/vk2matrix-bot/issues\n"
                     "(But do not report problems with API servers or network connection!)\n\n"
                     "Details:\n", exc_info=1)
        sys.exit(EXIT_UNKNOWN)
    sys.exit(status)
