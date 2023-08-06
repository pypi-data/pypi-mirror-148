# PyStark2 - Python add-on extension to Pyrogram
# Copyright (C) 2022 Stark Bots <https://github.com/StarkBotsIndustries>
#
# This file is part of PyStark2.
#
# PyStark2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyStark2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyStark2. If not, see <https://www.gnu.org/licenses/>.


import os
import yaml
from pystark.env import settings
from pystark.logger import logger


file = ""
folder = ""


def l10n_setup():
    global file
    global folder
    folder = settings.LOCALIZATION
    if folder:
        try:
            files = os.listdir(folder)
        except FileNotFoundError:
            logger.critical("Your localization path does not exist. Please correct it. Exiting...")
            raise SystemExit
        sup = ["english.yaml", "english.yml", "en.yaml", "en.yml"]
        for s in sup:
            if s in files:
                file = f"{folder}/{s}"
                break
        if not file:
            f = [f for f in files if f.endswith('.yaml') or f.endswith(".yml") or f.endswith('.json')]
            if f:
                file = f"{folder}/{f[0]}"
            else:
                logger.warn("Your localization directory does not have yaml file")
        return True
    else:
        logger.critical("No localization directory found.")
        raise SystemExit


async def l10n(lang: str = None):
    if not file:
        return
    if not lang:
        current_file = file
    else:
        current_file = ""
        for fi in os.listdir(folder):
            if lang in fi:
                current_file = fi
                break
        if not current_file:
            logger.warn(f"Lang '{lang}' not found. Choosing default.")
            current_file = file
    if current_file.endswith(".yaml") or current_file.endswith(".yml"):
        return await yaml_load(current_file)


def yaml_load(f):
    with open(f, "r", encoding="utf-8") as fi:
        return yaml.safe_load(fi)


def get_all_langs(only_list: bool = False):
    l10n_setup()
    if not file:
        return [] if only_list else {}
    langs = {}
    for fi in os.listdir(folder):
        if fi.endswith(".yaml") or fi.endswith(".yml"):
            data = yaml_load(folder+"/"+fi)
        else:
            continue
        langs[fi.rsplit(".", 1)[0]] = data
    if only_list:
        langs = list(langs.keys())
    return langs
