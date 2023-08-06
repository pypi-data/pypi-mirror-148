# Copyright (C) 2022 Sebastien Guerri
#
# This file is part of ppass.
#
# ppass is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# ppass is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Main application file
"""

import os
import json
import webbrowser

import click
import pyclip
from rich import print

from .modules.ui import ui
from .modules.git import git
from .modules.gpg import gpg
from .modules.utils import utils
from .modules.rjson import rjson
from .modules.params import params
from .modules.folders import folders
from .modules.xdotool import xdotool
from .modules.passwords import passwords

from .appConfig import app, AppConfig, AliasedGroup


class Config(AppConfig):
    """Specific application config class
    """
    path: str = ""
    identity: str = ""
    sep_username: str = "└─ USERNAME :: "
    sep_url: str = "└─ URL      :: "
    usegit: bool = False
    gitrepo: str = ""
    gituser: str = ""
    gitmail: str = ""
    gitbranch: str = "main"


# RUN #################################################################################################################

def create_config_file(path: str) -> Config:
    """Create config file

    Args:
        path (str): config file path

    Returns:
        Config: config object
    """
    config = Config(path)
    config.create()
    return config


def load_config(is_json: bool, section: str, new_section: bool = False) -> Config:
    """Load config file

    Args:
        is_json (bool): is cli in JSON mode
        section (str): config section
        new_section (bool, optional): if True, creates a new section. Defaults to False.

    Returns:
        Config: config object
    """
    config_file = app.default_rcpath()
    if not os.path.exists(config_file):
        config = create_config_file(config_file)
    else:
        config = Config(config_file)
    if new_section:
        AppConfig.add_section(config_file, section, Config(config_file))
    if not config.load(section):
        handle_error(is_json, "Application cannot load config file")
    return config


def init_context(is_json: bool, section: str) -> Config:
    """Initialise the context

    Args:
        is_json (bool): is cli in JSON mode
        section (str): config section

    Returns:
        Config: config object
    """
    config = load_config(is_json, section)
    if (not os.path.exists(config.path)):
        handle_error(is_json, f"Application is not initialized. Please run [code] {app.name()} init [/]")
    return config


def recup_context(ctx) -> (str, bool, bool):
    """Get context elements from global

    Args:
        ctx: cli context

    Returns:
        (str, bool, bool): tuple of context, is json mode, is yes mode
    """
    context: str = ctx.obj["context"]
    is_json: bool = ctx.obj["is_json"]
    is_yes: bool = ctx.obj["is_yes"]
    return (context, is_json, is_yes)


def init_command(ctx) -> (Config, bool, bool):
    """Initialise a command

    Args:
        ctx: cli context

    Returns:
        (Config, bool, bool): tuple of config object, is json mode, is yes mode
    """
    (context, is_json, is_yes) = recup_context(ctx)
    config: Config = init_context(is_json, context)
    if not is_json and not config.usegit:
        print("[yellow italic]WARNING: Git is not configured[/]\n")
    # if config.usegit:
    #     git.pull(config.path)
    return (config, is_json, is_yes)


# GLOBAL ##############################################################################################################

def handle_success(is_json: bool, message: str):
    """Handle success return

    Args:
        is_json (bool): is cli in JSON mode
        message (str): message
    """
    if is_json:
        rjson.success(message=message)
    else:
        ui.print_info(message)


def handle_data(is_json: bool, data: json, fn):
    """Handle success return (with data)

    Args:
        is_json (bool): is cli in JSON mode
        data (json): data
        fn (function): message
    """
    if is_json:
        rjson.success(data)
    else:
        fn(data)


def handle_error(is_json: bool, error):
    """Handle error return

    Args:
        is_json (bool): is cli in JSON mode
        error (_type_): error message
    """
    if is_json:
        rjson.error(str(error))
        exit(0)
    else:
        ui.print_error(error)
        exit(2)


# UTILS ###############################################################################################################

# TODO move function
def get_content(config: Config, password: str, user: str, url: str, comment: str = "") -> str:
    """Get password content in string format

    Args:
        config (Config): config object
        password (str): password value
        user (str): user value
        url (str): url value
        comment (str, optional): comment value. Defaults to "".

    Returns:
        str: password file content
    """
    content = ""
    content += password + "\n"
    content += config.sep_username + user + "\n"
    content += config.sep_url + url + "\n"
    content += comment + ("" if comment == "" else "\n")
    return content


# COMPLETION ##########################################################################################################

def complete_store(ctx, param, incomplete):
    items = app.sections()
    return list(filter(lambda i: incomplete.lower() in i.lower(), items))


def complete_filter(ctx, param, incomplete):
    store = ctx.parent.params["context"]
    config: Config = init_context(False, store)
    items = passwords.get_list(config.path, incomplete)
    return list(map(lambda i: f"\"{i.f_name}\"", items))


def complete_folder(ctx, param, incomplete):
    store = ctx.parent.parent.params["context"]
    config: Config = init_context(False, store)
    items = folders.get_list(config.path)
    items = list(filter(lambda i: incomplete.lower() in i.name.lower(), items))
    return list(map(lambda i: f"\"{i.name}\"", items))


# CLI #################################################################################################################

@click.group(cls=AliasedGroup)
@click.pass_context
@click.version_option(app.version())
@click.option("-c", "--context", default="DEFAULT", help="Section of config file to load (default is DEFAULT)",
              shell_complete=complete_store)
@click.option("-y", "--yes", is_flag=True, help="Auto confirm all prompts")
@click.option("--json", is_flag=True, help="Return json values instead of ui")
def cli(ctx, context, yes, json):
    """GPG Password Manager
    """
    ctx.obj["context"] = context
    ctx.obj["is_yes"] = yes
    ctx.obj["is_json"] = json
    pass


# INITIALISATION ######################################################################################################

@cli.command("init")
@click.pass_context
@click.option("--new-section", is_flag=True, help="Create a new section for selected context")
@click.option("--path", default=app.default_path(), help="Path where the files are stored")
@click.option("--identity", default="", help="Identity")
@click.option("--edit", is_flag=True, help="Edit configuration file")
def cli_init(ctx, new_section: bool, path: str, identity: str, edit: bool):
    """Initialize the application for the current context
    """
    (context, is_json, is_yes) = recup_context(ctx)
    try:
        if edit:
            assert (not is_json), "Edit action not available in JSON mode"
            click.edit(filename=app.default_rcpath())
        else:
            config = load_config(is_json, context, new_section)
            if path == app.default_path() and new_section:
                path = path[:len(path)-1] + "-" + context.lower()
            # if not os.path.exists(path):
            #     os.makedirs(path)
            config.identity = params.validate_identity(is_json, identity)
            config.path = params.validate_path(is_json, path, "Path")
            config.save(context)
            handle_success(is_json, "Application initialized")
    except Exception as error:
        handle_error(is_json, error)


@cli.command("init-git")
@click.pass_context
@click.option("--repo", default="", help="Git repository")
@click.option("--user", default="", help="Git username")
@click.option("--mail", default="", help="Git email")
@click.option("--branch", default="", help="Git branch")
@click.option("--pull", is_flag=True, help="Pull existing git repository")
def cli_init_git(ctx, repo: str, user: str, mail: str, branch: str, pull: bool):
    """Initialize git
    """
    (context, is_json, is_yes) = recup_context(ctx)
    try:
        config = load_config(is_json, context)
        config.usegit = True
        config.gitrepo = params.validate(is_json, repo, "Git repository")
        config.gituser = params.validate(is_json, user, "Git username")
        config.gitmail = params.validate(is_json, mail, "Git email")
        config.gitbranch = params.validate(is_json, branch, "Git branch", "main")
        config.save(context)
        if not pull:
            # Write default files
            f = open(os.path.join(config.path, ".gitattributes"), "w")
            f.write("*.gpg diff=gpg")
            f.close()
            f = open(os.path.join(config.path, ".gpg-id"), "w")
            f.write(config.identity)
            f.close()
        git.init(config.path, config.gitrepo, config.gitbranch, config.gituser, config.gitmail, pull)
        handle_success(is_json, "Git initialized")
    except Exception as error:
        handle_error(is_json, error)


# PASSWORDS ###########################################################################################################

@cli.command("list")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_list(ctx, filter: str):
    """List passwords
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        handle_data(is_json, items, ui.show_passwords)
    except Exception as error:
        handle_error(is_json, error)


@cli.command("show")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_show(ctx, filter: str):
    """Show password details
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password["path"], config.sep_username, config.sep_url)
        handle_data(is_json, password, ui.show_password)
    except Exception as error:
        handle_error(is_json, error)


@cli.command("delete")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_delete(ctx, filter: str):
    """Delete password
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password = params.validate_password(is_json, items)
        # CONFIRM DELETION
        if (not is_yes) and (not is_json):
            confirmed = ui.confirm("Delete password file")
            assert (confirmed), "Password deletion has been cancelled"
        # DELETE
        os.remove(password.path)
        if config.usegit:
            git.commit(config.path, f"Password file <{password.f_name}> has been deleted", config.gitbranch)
        handle_success(is_json, f"Password file <{password.f_name}> has been deleted")
    except Exception as error:
        handle_error(is_json, error)


@cli.command("open")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_open(ctx, filter: str):
    """Open password url
    For SSH : Open and connect
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password["path"], config.sep_username, config.sep_url)
        assert (password.url != ""), "Missing url"
        if is_json:
            pyclip.copy(password.url)
            rjson.success(data=password.url)
        elif password.url.startswith("ssh+"):
            domain = password.url.removeprefix("ssh+")
            xdotool.ssh_open(password.username, domain, password.password)
        else:
            webbrowser.open_new_tab(password.url)
    except Exception as error:
        handle_error(is_json, error)


@cli.command("user")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_user(ctx, filter: str):
    """Copy password username
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password["path"], config.sep_username, config.sep_url)
        assert (password.username != ""), "Missing username"
        if is_json:
            pyclip.copy(password.username)
            rjson.success(data=password.username)
        else:
            pyclip.copy(password.username)
            ui.print_info(f"[{password.app}] Username copied to clipboard")
    except Exception as error:
        handle_error(is_json, error)


@cli.command("pass")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_pass(ctx, filter: str):
    """Copy password password
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password["path"], config.sep_username, config.sep_url)
        if is_json:
            pyclip.copy(password.password)
            rjson.success(data=password.password)
        else:
            pyclip.copy(password.password)
            ui.print_info(f"[{password.app}] Password copied to clipboard")
    except Exception as error:
        handle_error(is_json, error)


@cli.command("clip")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_clip(ctx, filter: str):
    """Clip password to opened web url
    For SSH : Open and connect
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        assert (not is_json), "Clip is not available in JSON mode"
        items = passwords.get_list(config.path, filter)
        password = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password["path"], config.sep_username, config.sep_url)
        assert (password.username != ""), "Missing username"
        if password.url.startswith("ssh+"):
            domain = password.url.removeprefix("ssh+")
            xdotool.ssh_open(password.username, domain, password.password)
        else:
            xdotool.clip(password.username, password.password)
    except Exception as error:
        handle_error(is_json, error)


@cli.command("generate")
@click.pass_context
@click.option("--folder", default="", help="Folder name", shell_complete=complete_folder)
@click.option("--name", default="", help="Password name")
@click.option("--user", default="", help="User name")
@click.option("--url", default="", help="Site url")
def cli_generate(ctx, folder: str, name: str, user: str, url: str):
    """Generate a new password file (with random password)
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        folder_items = folders.get_list(config.path)
        folder = params.validate_folder(is_json, folder, folder_items)
        name = params.validate(is_json, name, "Password name")
        password = utils.generate_password()
        user = params.validate(is_json, user, "User name")
        url = params.validate_url(is_json, url, "Site url")
        content = get_content(config, password, user, url)
        filepath = os.path.join(config.path, folder, name + ".gpg")
        gpg.encrypt_to_file(content, config.identity, filepath)
        if config.usegit:
            git.commit(config.path, "Password file created", config.gitbranch)
        handle_success(is_json, "Password file created")
    except Exception as error:
        handle_error(is_json, error)


@cli.command("insert")
@click.pass_context
@click.option("--folder", default="", help="Folder name", shell_complete=complete_folder)
@click.option("--name", default="", help="Password name")
@click.option("--password", default="", help="Password")
@click.option("--user", default="", help="User name")
@click.option("--url", default="", help="Site url")
def cli_insert(ctx, folder: str, name: str, password: str, user: str, url: str):
    """Create a new password file (password is already known)
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        folder_items = folders.get_list(config.path)
        folder = params.validate_folder(is_json, folder, folder_items)
        name = params.validate(is_json, name, "Password name")
        password = params.validate_passwordvalue(is_json, password)
        user = params.validate(is_json, user, "User name")
        url = params.validate_url(is_json, url, "Site url")
        content = get_content(config, password, user, url)
        filepath = os.path.join(config.path, folder, name + ".gpg")
        gpg.encrypt_to_file(content, config.identity, filepath)
        if config.usegit:
            git.commit(config.path, "Password file created", config.gitbranch)
        handle_success(is_json, "Password file created")
    except Exception as error:
        handle_error(is_json, error)


@cli.command("edit")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_edit(ctx: click.Context, filter: str):
    """Edit password file
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password_item = params.validate_password(is_json, items)
        content = gpg.decrypt_file(password_item["path"])
        new_content = click.edit(content)
        assert (new_content is not None), "Edition cancelled"
        os.remove(password_item["path"])
        gpg.encrypt_to_file(new_content, config.identity, password_item["path"])
        if config.usegit:
            git.commit(config.path, "File modified", config.gitbranch)
        handle_success(is_json, "File modified")
    except Exception as error:
        handle_error(is_json, error)


# MODIFY ##############################################################################################################

@cli.group("modify", cls=AliasedGroup)
@click.pass_context
def cli_modify(ctx: click.Context):
    """Modify actions
    """
    pass


@cli_modify.command("user")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
@click.option("--new", default="", help="New username")
def cli_modify_user(ctx: click.Context, filter: str, new: str):
    """Modify username
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password_item = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password_item["path"], config.sep_username, config.sep_url)
        new = params.validate(is_json, new, "New username", print_old=True, old_value=password.username)
        content = get_content(config, password.password, new, password.url, password.comment)
        os.remove(password_item["path"])
        gpg.encrypt_to_file(content, config.identity, password_item["path"])
        if config.usegit:
            git.commit(config.path, "Username modified", config.gitbranch)
        handle_success(is_json, "Username modified")
    except Exception as error:
        handle_error(is_json, error)


@cli_modify.command("url")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
@click.option("--new", default="", help="New url")
def cli_modify_url(ctx: click.Context, filter: str, new: str):
    """Modify url
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password_item = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password_item["path"], config.sep_username, config.sep_url)
        new = params.validate(is_json, new, "New url", print_old=True, old_value=password.url)
        content = get_content(config, password.password, password.username, new, password.comment)
        os.remove(password_item["path"])
        gpg.encrypt_to_file(content, config.identity, password_item["path"])
        if config.usegit:
            git.commit(config.path, "Url modified", config.gitbranch)
        handle_success(is_json, "Url modified")
    except Exception as error:
        handle_error(is_json, error)


@cli_modify.command("comment")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
@click.option("--new", default="", help="New comment")
def cli_modify_comment(ctx: click.Context, filter: str, new: str):
    """Modify comment
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password_item = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password_item["path"], config.sep_username, config.sep_url)
        new = params.validate_multiline(is_json, new, password.comment, "New comment")
        content = get_content(config, password.password, password.username, password.url, new)
        os.remove(password_item["path"])
        gpg.encrypt_to_file(content, config.identity, password_item["path"])
        if config.usegit:
            git.commit(config.path, "Comment modified", config.gitbranch)
        handle_success(is_json, "Comment modified")
    except Exception as error:
        handle_error(is_json, error)


@cli_modify.group("password", cls=AliasedGroup)
@click.pass_context
def cli_modify_password(ctx: click.Context):
    """Modify passwords actions
    """
    pass


@cli_modify_password.command("generate")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
def cli_modify_password_generate(ctx: click.Context, filter: str):
    """Modify password (generate a new random one)
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password_item = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password_item["path"], config.sep_username, config.sep_url)
        new = utils.generate_password()
        content = get_content(config, new, password.username, password.url, password.comment)
        os.remove(password_item["path"])
        gpg.encrypt_to_file(content, config.identity, password_item["path"])
        if config.usegit:
            git.commit(config.path, "New password generated", config.gitbranch)
        handle_success(is_json, "New password generated")
    except Exception as error:
        handle_error(is_json, error)


@cli_modify_password.command("insert")
@click.pass_context
@click.argument("filter", default="", shell_complete=complete_filter)
@click.option("--new", default="", help="New password")
def cli_modify_password_insert(ctx: click.Context, filter: str, new: str):
    """Modify password (password is already known)
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = passwords.get_list(config.path, filter)
        password_item = params.validate_password(is_json, items)
        password = gpg.decrypt_to_password(password_item["path"], config.sep_username, config.sep_url)
        new = params.validate_passwordvalue(is_json, new)
        content = get_content(config, new, password.username, password.url, password.comment)
        os.remove(password_item["path"])
        gpg.encrypt_to_file(content, config.identity, password_item["path"])
        if config.usegit:
            git.commit(config.path, "New password saved", config.gitbranch)
        handle_success(is_json, "New password saved")
    except Exception as error:
        handle_error(is_json, error)


# FOLDERS #############################################################################################################

@cli.group("folders", cls=AliasedGroup, invoke_without_command=True)
@click.pass_context
def cli_folders(ctx: click.Context):
    """List all folders
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(cli_folders_list)


@cli_folders.command("list")
@click.pass_context
def cli_folders_list(ctx: click.Context):
    """List all folders
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        items = folders.get_list(config.path)
        handle_data(is_json, items, ui.show_folders)
    except Exception as error:
        handle_error(is_json, error)


@cli_folders.command("create")
@click.pass_context
@click.option("--name", default="", help="Name of folder to create")
def cli_folders_create(ctx: click.Context, name: str):
    """Create a new folder
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        name = params.validate(is_json, name, "Name")
        path = os.path.join(config.path, name)
        folders.create(name, path)
        if config.usegit:
            git.commit(config.path, f"Folder <{name}> has been created", config.gitbranch)
        handle_success(is_json, f"Folder <{name}> has been created")
    except Exception as error:
        handle_error(is_json, error)


@cli_folders.command("delete")
@click.pass_context
@click.option("--name", default="", help="Name of folder to delete", shell_complete=complete_folder)
def cli_folders_delete(ctx: click.Context, name: str):
    """Delete an existing folder
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        folder_items = folders.get_list(config.path)
        # CHECK VALID NAME
        name = params.validate_folder(is_json, name, folder_items)
        # CONFIRM DELETION
        if (not is_yes) and (not is_json):
            response = ui.confirm("Delete folder and all its content")
            assert (response), "Folder deletion has been cancelled"
        # DELETE FOLDER
        path = os.path.join(config.path, name)
        folders.delete(name, path)
        if config.usegit:
            git.commit(config.path, f"Folder <{name}> has been deleted", config.gitbranch)
        handle_success(is_json, f"Folder <{name}> has been deleted")
    except Exception as error:
        handle_error(is_json, error)


# GIT #################################################################################################################

@cli.group("git", cls=AliasedGroup)
@click.pass_context
def cli_git(ctx: click.Context):
    """Git commands
    """
    pass


@cli_git.command("status")
@click.pass_context
def cli_git_status(ctx: click.Context):
    """Git status
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        git.status(config.path)
    except Exception as error:
        handle_error(is_json, error)


@cli_git.command("pull")
@click.pass_context
def cli_git_pull(ctx: click.Context):
    """Git pull
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        git.pull(config.path, config.gitbranch)
    except Exception as error:
        handle_error(is_json, error)


@cli_git.command("push")
@click.pass_context
def cli_git_push(ctx: click.Context):
    """Git push
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        git.push(config.path, config.gitbranch)
    except Exception as error:
        handle_error(is_json, error)


@cli_git.command("sync")
@click.pass_context
def cli_git_sync(ctx: click.Context):
    """Git pull then Git push
    """
    (config, is_json, is_yes) = init_command(ctx)
    try:
        git.sync(config.path, config.gitbranch)
    except Exception as error:
        handle_error(is_json, error)
