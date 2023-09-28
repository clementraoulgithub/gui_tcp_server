import logging
import os
import re
from enum import Enum, unique
import io
import sys
from typing import Optional, Tuple, List
from cairosvg import svg2png
from PIL import Image, ImageTk, PngImagePlugin
import configparser

from resources.icon.icon_path import ICON_PATH
from src.client.core.qt_core import (
    QColor,
    QIcon,
    QPainter,
    QPixmap,
    QWidget,
    QVBoxLayout
)

LM_USE_SVG = 1

# set PIL.PngImagePlugin logger off
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.INFO)


@unique
class Icon(Enum):
    CLEAR = f"{ICON_PATH}/clear.svg"
    LOGIN = f"{ICON_PATH}/login.svg"
    LOGOUT = f"{ICON_PATH}/logout.svg"
    SEND = f"{ICON_PATH}/send.svg"
    CONFIG = f"{ICON_PATH}/config.svg"
    STATUS = f"{ICON_PATH}/status_user_conn.svg"
    MESSAGE = f"{ICON_PATH}/message.svg"
    USER_ICON = f"{ICON_PATH}/default_user_icon.svg"
    LEFT_ARROW = f"{ICON_PATH}/left_arrow.svg"
    RIGHT_ARROW = f"{ICON_PATH}/right_arrow.svg"
    DOWN_ARROW = f"{ICON_PATH}/down_arrow.svg"
    ARROW_RIGHT = f"{ICON_PATH}/arrow_right.svg"
    AVATAR = f"{ICON_PATH}/avatar_update.svg"
    SMILEY = f"{ICON_PATH}/smiley.svg"
    ROOM = f"{ICON_PATH}/home.svg"
    SEPARATOR = f"{ICON_PATH}/separator.svg"
    SEPARATOR_HORIZ = f"{ICON_PATH}/separator_ho.svg"
    CROWN = f"{ICON_PATH}/crown.svg"
    REPLY = f"{ICON_PATH}/reply.svg"
    REPLY_ROTATED = f"{ICON_PATH}/reply_rotated.svg"
    CLOSE_USERS = f"{ICON_PATH}/close_users.svg"
    CLOSE_DM = f"{ICON_PATH}/close_dm.svg"
    LINK = f"{ICON_PATH}/link.svg"
    MESSAGE_DM = f"{ICON_PATH}/icon.svg"
    USER_CONNECTED = f"{ICON_PATH}/user_connected.svg"
    USER_DISCONNECTED = f"{ICON_PATH}/user_disconnected.svg"
    CLOSE = f"{ICON_PATH}/close.svg"
    FILE = f"{ICON_PATH}/file.svg"
    SEARCH = f"{ICON_PATH}/search.svg"
    SWITCH_COLOR = f"{ICON_PATH}/switch_color.svg"


@unique
class BlackColor(Enum):
    GREY = "#383A3F"
    MIDDLE_GREY = "#2A2C2F"
    LIGHT_GREY = "#B6BAC0"
    DARK_GREY = "#313338"
    LIGHT_BLACK = "#232328"
    WHITE = "#FFFFFF"
    BLACK = "#1C1D1F"
    YELLOW = "#F6DF91"

@unique
class WhiteColor(Enum):
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    LIGHT_GREY = "#e4e4e4"
    DARK_GREY = "#A6A6A7"
    GREY = "#CFCFD0"
    BLUE = "#1D87E5"
    
@unique
class GenericColor(Enum):
    RED = "#E03232"
    
class Themes:
    class ThemeColor(Enum):
        BLACK = 0
        WHITE = 1
        CUSTOM = 2
        
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        
        self.theme_name = self.config['THEME']['theme']
        self.list_colors = [
            "text_color",
            "title_color",
            "inner_color",
            "background_color",
            "nav_color",
            "search_color",
            "rooms_color",
            "emoji_color",
        ]
        
        if self.theme_name == Themes.ThemeColor.BLACK.name:
            self.color = BlackColor.BLACK.value
            self.text_color = BlackColor.WHITE.value
            self.title_color = BlackColor.LIGHT_GREY.value
            self.inner_color = BlackColor.DARK_GREY.value
            self.background_color = BlackColor.GREY.value
            self.rgb_background_color_innactif = QColor(*self.hex_to_rgb(self.background_color))
            self.rgb_background_color_actif = QColor(*self.hex_to_rgb(self.inner_color))
            self.nav_color = BlackColor.MIDDLE_GREY.value
            self.search_color = BlackColor.LIGHT_BLACK.value
            self.rgb_background_color_actif_footer = QColor(*self.hex_to_rgb(self.search_color))
            self.rooms_color = BlackColor.BLACK.value
            self.emoji_color = BlackColor.YELLOW.value
        elif self.theme_name == Themes.ThemeColor.WHITE.name:
            self.color = WhiteColor.WHITE.value
            self.text_color = WhiteColor.BLACK.value
            self.title_color = WhiteColor.BLACK.value
            self.inner_color = WhiteColor.LIGHT_GREY.value
            self.background_color = WhiteColor.WHITE.value
            self.rgb_background_color_innactif = QColor(*self.hex_to_rgb(self.background_color))
            self.rgb_background_color_actif = QColor(*self.hex_to_rgb(self.inner_color))
            self.nav_color = WhiteColor.WHITE.value
            self.search_color = WhiteColor.GREY.value
            self.rgb_background_color_actif_footer = QColor(*self.hex_to_rgb(self.search_color))
            self.rooms_color = WhiteColor.DARK_GREY.value
            self.emoji_color = WhiteColor.BLACK.value
        elif self.theme_name == Themes.ThemeColor.CUSTOM.name:
            self.color = self.config['THEME']['inner_color']
            self.text_color = self.config['THEME']['text_color']
            self.title_color = self.config['THEME']['title_color']
            self.inner_color = self.config['THEME']['inner_color']
            self.background_color = self.config['THEME']['background_color']
            self.rgb_background_color_innactif = QColor(*self.hex_to_rgb(self.background_color))
            self.rgb_background_color_actif = QColor(*self.hex_to_rgb(self.inner_color))
            self.nav_color = self.config['THEME']['nav_color']
            self.search_color = self.config['THEME']['search_color']
            self.rgb_background_color_actif_footer = QColor(*self.hex_to_rgb(self.search_color))
            self.rooms_color = self.config['THEME']['rooms_color']
            self.emoji_color = self.config['THEME']['emoji_color']
        else:
            raise NotImplementedError("Theme not found")
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to rgb color

        Args:
            hex_color (str): hex color

        Returns:
            Tuple[int, int, int]: rgb color
        """
        hex_color = hex_color.lstrip("#")
        hlen = len(hex_color)
        return tuple(int(hex_color[i : i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))
    
    def switch_theme(self, controller, theme: ThemeColor) -> None:
        """
        Switch theme
        """
        self.config['THEME']['theme'] = theme.name 
        with open('./config.ini', 'w') as configfile:
            self.config.write(configfile)
            
        # Restart the app
        controller.logout()
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
        
    def create_custom_theme(self, controller, list_theme_line_edit: List) -> None:
        """
        Create custom theme

        Args:
            controller (GuiController): the controller of the GUI
            list_theme_line_edit (List[CustomQLineEdit]): list of CustomQLineEdit
        """
        for line_edit, color_name in zip(list_theme_line_edit, self.list_colors):
            color = line_edit.text()
            if not color or color[0] != "#" or len(color) != 7:
                return
            else:
                self.config['THEME'][color_name] = color

        self.switch_theme(controller, Themes.ThemeColor.CUSTOM)
        

@unique
class ImageAvatar(Enum):
    SERVER = "./resources/images/server_picture.png"
    ROOM = "./resources/images/room_picture.png"
    EN = "./resources/images/en.png"


def image_from_svg(filename="", size=0):
    if LM_USE_SVG != 1:
        return Image.new("RGBA", [size, size])
    if size == 0:
        # unscaled
        svg2png(url=filename, write_to="/tmp/example_temp_image.png")
    else:
        svg2png(
            url=filename,
            write_to="/tmp/example_temp_image.png",
            parent_width=size,
            parent_height=size,
        )
    return Image.open("/tmp/example_temp_image.png")


def empty_photoimage(size=40):
    photo = Image.new("RGBA", [size, size])
    return ImageTk.PhotoImage(image=photo)


def get_scaled_icon(iconfilename, size=20):
    try:
        # try an svg
        if re.compile(".*\.svg").match(iconfilename):
            photo = image_from_svg(filename=iconfilename, size=size)
        else:
            photo = Image.open(iconfilename)
    except Exception as f:
        logging.error("Error with icon file:", f)
        return empty_photoimage()

    if size != 0 and (
        type(photo) is Image or type(photo) is PngImagePlugin.PngImageFile
    ):
        photo.thumbnail(size=[size, size])

    if type(photo) is not ImageTk.PhotoImage:
        try:
            photo = ImageTk.PhotoImage(photo)
        except Exception as error:
            logging.error(f"Error: {error}")
    return photo


def QIcon_from_svg(svg_name, color: str):
    path = ICON_PATH
    pixmap = QPixmap(os.path.join(path, svg_name))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    if color:
        painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)


def check_str_len(intput_str: str) -> str:
    intput_str.capitalize()
    LEN = 15
    return f"{intput_str[:13]}.." if len(intput_str) >= LEN else intput_str


def resize_picture(path: str, size: Optional[Tuple] = (520, 520)) -> bytes:
    """
    Resize picture to a specific size

    Args:
        path (str): path of the picture
        size (tuple): size of the picture
    """
    with open(path[0], "rb") as f:
        picture_bytes = f.readlines()

    picture = Image.open(io.BytesIO(picture_bytes))
    new_width, new_height = size

    resized_picture = picture.resize((new_width, new_height))

    output_bytes = io.BytesIO()
    resized_picture.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    return output_bytes.read()
