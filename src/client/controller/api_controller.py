"""Module for api controller"""

from enum import Enum, unique
from functools import lru_cache
from typing import Callable, Optional

from src.client.controller import global_variables
from src.client.controller.event_manager import EventManager
from src.client.view.custom_widget.custom_avatar_label import AvatarStatus
from src.tools.utils import Themes


@unique
class ApiStatus(Enum):
    """
    Enum for api status
    """

    SUCCESS = 200
    ERROR = 400
    NOT_FOUND = 404
    FORBIDDEN = 403


theme = Themes()


class ApiController:
    """
    Api controller class.
    """

    def __init__(self, ui, event_manager: EventManager) -> None:
        self.ui = ui
        self.is_connected = False
        self.event_manager = event_manager

    def send_form(self, callback: Callable) -> bool:
        """
        Backend request for login form

        Returns:
            bool: return True if the login is successful
        """
        # Getting username and password from the login form
        username, password = self.remove_empty_char_from_entry()

        # Avoid empty username or password
        if not username or not password:
            return ApiStatus.FORBIDDEN

        # Send login form to the server
        status_code, is_connected = callback(username, password)

        # Check if the login is successful and if the user is not already connected
        if status_code != 200 or is_connected:
            return ApiStatus.ERROR

        self.ui.client.user_name = username

        # Update login status to connected
        if self.send_login_status(username=username, status=True):
            self.is_connected = True
            return ApiStatus.SUCCESS
        return ApiStatus.ERROR

    def send_login_status(self, username: str, status: bool) -> bool:
        """
        Send login status to the server

        Args:
            username (str): username
            status (bool): login status (True if connected, False if disconnected)

        Returns:
            bool: return True if the login status is successfully sent
        """
        return self.ui.backend.send_login_status(username, status)

    def get_last_message_id(self) -> int:
        """
        Backend request for getting last message id

        Returns:
            int: return last message id
        """
        return self.ui.backend.get_last_message_id()

    @lru_cache
    def get_first_message_id(self, user1: str, user2: str) -> int:
        """
        Backend request for getting first message id

        Args:
            username (str): username

        Returns:
            int: return first message id
        """
        return self.ui.backend.get_first_message_id(user1, user2)

    def get_user_icon(
        self,
        username: Optional[bool] = None,
        update_personal_avatar: Optional[bool] = False,
    ) -> None:
        """
        Backend request for getting user icon

        Args:
            username (Optional[bool], optional): usernameto fetch. Defaults to None.
            update_personal_avatar (Optional[bool], optional): Defaults to False.
        """

        # If username is None, get the user icon of the current user
        if not username:
            username = self.ui.client.user_name

        # Get user icon from the server
        if content := self.ui.backend.get_user_icon(username):
            self.ui.users_pict[username] = content

            # Update the personnal avatar if True
            if update_personal_avatar:
                self.ui.footer_widget.user_picture.update_picture(
                    status=AvatarStatus.ACTIVATED,
                    content=content,
                    background_color=theme.rgb_background_color_actif_footer,
                )
            self.update_user_connected(username, content)
        else:
            self.ui.users_pict[username] = ""

    def update_user_connected(self, username: str, content: bytes) -> None:
        """
        Update global user variables with user content bytes

        Args:
            username (str): username
            content (bytes): picture in bytes
        """
        if (
            username in self.ui.users_connected.keys()
            and self.ui.users_connected[username] is True
        ):
            global_variables.user_connected[username] = [content, False]
        else:
            self.ui.users_connected["username"] = False
            global_variables.user_disconnect[username] = [content, False]

        self.event_manager.event_users_connected()
        self.event_manager.event_users_disconnected()

    def get_older_messages(
        self, start: int, number: int, user1: str, user2: str
    ) -> dict:
        """
        Get older messages from the server

        Returns:
            dict: return a dict of older messages
        """
        older_messages: list = self.ui.backend.get_older_messages(
            start, number, user1, user2
        )

        return older_messages["messages"]

    def get_older_message(self, message_id: int) -> dict:
        """
        Get older message from the server
        """
        older_message = self.ui.backend.get_older_message(message_id)
        return older_message["message"]

    def get_all_dm_users_username(self, username: str) -> list:
        """
        Get all dm users username from the server

        Returns:
            list: return a list of dm for the user
        """
        return self.ui.backend.get_all_dm_users_username(username)

    def add_sender_picture(self, sender_id: str) -> None:
        """Add sender picture to the list of sender pictures

        Args:
            sender_id (str): sender identifier
        """
        if sender_id not in list(self.ui.users_pict.keys()):
            self.get_user_icon(sender_id)

    def update_is_readed_status(
        self, sender: str, receiver: str, is_readed=True
    ) -> None:
        """
        Update is readed status of the message

        Args:
            sender (str): sender name
            receiver (str): receiver name
            is_readed (bool, optional): Bool status. Defaults to True.
        """
        self.ui.backend.update_is_readed_status(sender, receiver, is_readed)

    def remove_empty_char_from_entry(self) -> tuple:
        """
        Remove empty char from the entry

        Returns:
            tuple: return username and password without empty char
        """
        username = self.ui.login_form.username_entry.text().replace(" ", "")
        password = self.ui.login_form.password_entry.text().replace(" ", "")

        return username, password

    def get_user_creation_date(self, username: str) -> str:
        """
        Get user creation date from the server

        Args:
            username (str): username

        Returns:
            str: return user creation date
        """
        return self.ui.backend.get_user_creation_date(username)

    def update_user_description(self, username: str, description: str) -> bool:
        """
        Update user description

        Args:
            username (str): username
            description (str): description

        Returns:
            bool: return True if the description is successfully updated
        """
        return self.ui.backend.update_user_description(username, description)
