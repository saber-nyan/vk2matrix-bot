# -*- coding: utf-8 -*-
"""
Our main file!
"""
import logging
import os
import re
import signal
import sys
import tempfile
import time

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mcommand_handler import MCommandHandler
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_client.room import Room
from vk_api import vk_api

try:
    from . import config
except ImportError:
    import config

EXIT_SUCCESS = 0  # By SIGINT/SIGTERM, successfully
EXIT_ENV = 1  # Incorrect ENV variables
EXIT_VK_API = 2  # vk_api error
EXIT_MATRIX_API = 4  # matrix_bot_api error
EXIT_UNKNOWN = 128  # WTF?!

VK_VER = 5.71

vk: vk_api.VkApiMethod

VK_PHOTO_ATTACH_REGEX = re.compile(r"photo_(\d+)")


def vk_photo_select_max_url(photo_attach: dict):
    """
    Selects the link to the maximum resolution image from
    the retarded JSON structure of the VKontakte response.

    :param dict photo_attach: original response
    :return: maximum resolution url
    :rtype: str
    """
    log.debug("attach {}".format(photo_attach))
    max_size = 75
    for key in photo_attach:
        value = photo_attach[key]
        log.debug("<{}> -> {}".format(key, value))
        if VK_PHOTO_ATTACH_REGEX.match(key):  # Key ``photo_<res>``, where 25 <= <res> <= inf
            size = int(re.sub(VK_PHOTO_ATTACH_REGEX, r"\1", key))
            if size > max_size:
                max_size = size
    max_size_url = photo_attach["photo_" + str(max_size)]
    return max_size_url

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


def bot_cmd_ping_echo(room: Room, event: dict):
    """
    Check bot availability, echo text.

    :param Room room: Matrix room
    :param dict event: event content
    """
    room.send_html("ALIVE!<br/>"
                   "<b>You sent:</b> {}".format(event["content"]["body"]))


def bot_rgx_vk_wall(room: Room, event: dict):
    """
    Process VKontakte wall posts.

    :param Room room: Matrix room
    :param dict event: event content
    """
    input_text = event["content"]["body"]
    post_id = re.search(r"vk\.com/.*wall(-?\d+_\d+)", input_text).group(1)
    log.debug("got post ID {}".format(post_id))
    room.send_text("Post ID is {}".format(post_id))
    vk_result: dict = vk.wall.getById(
        posts=post_id,
        version=VK_VER
    )[0]
    text = vk_result["text"]
    attachments = vk_result.get("attachments", [])
    room.send_text(text)
    for base_attach in attachments:
        if base_attach["type"] == "photo":  # TODO: moar types!
            attach = base_attach["photo"]
            max_url = vk_photo_select_max_url(attach)
            # thumb_url = attach["photo_75"]
            room.send_image(
                url=max_url,
                name=str(attach["id"]),
                imageinfo={
                    "h": attach["height"],
                    "w": attach["width"],
                }
            )


def register_bot_callbacks(bot: MatrixBotAPI):
    """
    Define all handlers and register callbacks.

    :param MatrixBotAPI bot: bot instance
    """
    bot.add_handler(MCommandHandler('ping', bot_cmd_ping_echo))
    bot.add_handler(MRegexHandler(r'vk\.com/.*wall(-?\d+_\d+)', bot_rgx_vk_wall))


# noinspection PyBroadException
def main() -> int:
    """
    Our main() function!

    :return: exit code
    :rtype: int
    """
    log.info("Init vk_api...")
    try:
        vk_session = vk_api.VkApi(
            login=config.VK_LOGIN,
            password=config.VK_PASSWORD,
            config_filename=os.path.join(tempfile.gettempdir(), 'vk2matrix_tmp.json'),
            api_version=str(VK_VER)
        )
        vk_session.http.headers.update({
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/65.0.3325.31 Safari/537.36"
        })
        vk_session.auth(token_only=True)
        global vk
        vk = vk_session.get_api()
        log.info("...success!")
    except:
        log.critical("...failure!\nDetails:\n", exc_info=1)
        return EXIT_VK_API

    log.info("Init MatrixBotAPI...")
    try:
        bot = MatrixBotAPI(config.USERNAME, config.PASSWORD, config.SERVER)
        register_bot_callbacks(bot)
        bot.start_polling()
        log.info("...success, started polling!")
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
