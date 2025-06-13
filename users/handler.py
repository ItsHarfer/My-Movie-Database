from config.config import COLOR_MENU_OPTIONS, COLOR_SUCCESS
from printers import print_colored_output
from users import storage_sql
from users.users import set_active_user, clear_active_user


def handle_list_users(_: None, __: None, ___: None) -> None:
    """
    Displays all existing users from the SQL database.

    :param _: Placeholder parameter.
    :param __: Placeholder parameter.
    :param ___: Placeholder parameter.
    :return: None
    """
    users = storage_sql.list_users()
    for user in users:
        print(f"{user} - ", end="")


def handle_select_user(_: None, data: dict[int, dict[str, str]], user_id: int) -> bool:
    """
    Sets the specified user as active and confirms the selection.

    :param _: Placeholder parameter.
    :param data: Dictionary containing user data.
    :param user_id: ID of the user to set as active.
    :return: True if the user was successfully selected.
    """
    username = data[user_id]["username"]
    set_active_user(user_id, username)
    print_colored_output(
        f"✔️ User '{username}' (ID: {user_id}) selected!", COLOR_SUCCESS
    )
    return True


def handle_create_user(_: None, __: None, ___: None) -> None:
    """
    Prompts for a new username and creates a new user entry in the SQL database.

    :param _: Placeholder parameter.
    :param __: Placeholder parameter.
    :param ___: Placeholder parameter.
    :return: None
    """
    username = input("Enter a username: ")
    storage_sql.create_user_if_not_exists(username)
    print_colored_output(f"User {username} created successfully", COLOR_MENU_OPTIONS)


def handle_switch_user(_: None, __: None, ___: None) -> None:
    """
    Clears the current active user, effectively switching user state to none.

    :param _: Placeholder parameter.
    :param __: Placeholder parameter.
    :param ___: Placeholder parameter.
    :return: None
    """
    clear_active_user()
