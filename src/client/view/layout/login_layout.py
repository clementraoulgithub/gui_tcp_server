"""Login layout module."""

import os

from dotenv import load_dotenv
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.client.view.custom_widget.custom_avatar_label import AvatarLabel
from src.client.view.custom_widget.custom_line_edit import CustomQLineEdit
from src.tools.utils import Icon, ImageAvatar, Themes, icon_from_svg

load_dotenv()


# pylint: disable=too-many-instance-attributes
class LoginLayout(QHBoxLayout):
    """
    LoginLayout widget class.

    Args:
        QHBoxLayout (QHBoxLayout): the horizontal layout widget
    """

    def __init__(self, theme: Themes):
        super().__init__()

        self.theme = theme
        self.setContentsMargins(0, 0, 0, 0)

        self.create_main_widget()
        self.create_main_layouts()

        self.create_title_widgets()
        self.create_username_widgets()
        self.create_password_widgets()
        self.create_error_widgets()
        self.create_button_widgets()

        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addLayout(self.error_layout)
        self.main_layout.addLayout(self.username_layout)
        self.main_layout.addLayout(self.password_layout)

    def create_main_widget(self) -> None:
        """
        Create the main widget.
        """
        self.main_widget = QWidget()
        self.main_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_widget.setStyleSheet(
            f"background-color: {self.theme.background_color};\
            color: {self.theme.title_color};\
            border-radius: 0px;\
            border: 0px solid {self.theme.nav_color};"
        )
        self.addWidget(self.main_widget)

    def create_main_layouts(self) -> None:
        """
        Create the main layouts.
        """
        # --- Main Layout --- #
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        item = QLabel()
        item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # --- Title Layout --- #
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 30)
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Error Layout --- #
        self.error_layout = QHBoxLayout()
        self.error_layout.setContentsMargins(0, 0, 0, 15)
        self.error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Username Layout --- #
        self.username_layout = QHBoxLayout()
        self.username_layout.addWidget(item)
        self.username_layout.setContentsMargins(0, 0, 0, 0)
        self.username_layout.setSpacing(15)

        # --- Password Layout --- #
        self.password_layout = QHBoxLayout()
        self.password_layout.addWidget(item)
        self.password_layout.setContentsMargins(0, 0, 0, 0)
        self.password_layout.setSpacing(15)
        self.password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def create_title_widgets(self) -> None:
        """
        Create the title widgets.
        """
        self.icon_soft = AvatarLabel(content=ImageAvatar.SERVER.value)
        self.icon_soft.setStyleSheet(
            "font-weight: bold;\
            border: none"
        )
        self.icon_soft.setAlignment(Qt.AlignCenter | Qt.AlignCenter)

        self.title_label = QLabel("Hello")
        self.title_label.setStyleSheet(
            f"color: {self.theme.title_color};\
            border: none; font-size: 36px;\
            font-weight: bold;\
            font-style: italic"
        )
        self.title_layout.addWidget(self.icon_soft)
        self.title_layout.addWidget(self.title_label)

    def create_error_widgets(self) -> None:
        """
        Create the error widgets.
        """
        self.error_label = QLabel("Please login or register if you havn't account yet")
        self.error_label.setStyleSheet(
            f"color: {self.theme.title_color};\
            border: none;"
        )
        self.error_layout.addWidget(self.error_label)

    def create_username_widgets(self) -> None:
        """
        Create the username widgets.
        """
        self.username_label = QLabel("Username: ")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_label.setStyleSheet(
            "font-weight: bold;\
            border: none;"
        )
        self.username_entry = CustomQLineEdit(
            place_holder_text="Enter your username",
            text=os.environ["USERNAME"],
        )
        self.username_entry.setMinimumWidth(300)
        self.username_entry.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.username_entry.setContentsMargins(0, 0, 0, 0)

        self.username_layout.addWidget(self.username_entry)
        item = QLabel()
        item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.username_layout.addWidget(item)

    def create_password_widgets(self) -> None:
        """
        Create the password widgets.
        """
        self.password_label = QLabel("Password: ")
        self.password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_label.setStyleSheet(
            "font-weight: bold;\
            border: none"
        )
        self.password_entry = CustomQLineEdit(
            place_holder_text="Enter your password",
            text=os.environ["PASSWORD"],
        )
        self.password_entry.setMinimumWidth(300)
        self.password_entry.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.password_entry.setTextMargins(55, 0, 0, 0)
        self.password_entry.setContentsMargins(0, 0, 0, 0)
        self.password_entry.setEchoMode(QLineEdit.Password)

        item = QLabel()
        item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.password_layout.addWidget(self.password_entry)
        self.password_layout.addWidget(item)

    def create_button_widgets(self) -> None:
        """
        Create the button widgets.
        """
        self.send_icon = QIcon(
            icon_from_svg(Icon.SEND.value, color=self.theme.text_color)
        )
        self.register_icon = QIcon(
            icon_from_svg(Icon.LOGIN.value, color=self.theme.text_color)
        )
        self.entry_action = self.password_entry.addAction(
            self.register_icon, QLineEdit.TrailingPosition
        )
        self.entry_action.setToolTip("Register")
        self.send_action = self.password_entry.addAction(
            self.send_icon, QLineEdit.TrailingPosition
        )
        self.send_action.setToolTip("Login")
