__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
import os
import re
from math import log10
from shutil import copy2, SameFileError
from typing import List

from media_tools.util import AudaciousTools


class PlaylistCopier:
    def __init__(self, audacious: AudaciousTools, playlist_id: str) -> None:
        self.audacious = audacious
        self.playlist_id = playlist_id

    def copy_playlist(self, number: int, target: str, renumber: bool = False) -> None:
        if not os.path.isdir(target):
            os.mkdir(target)

        playlist_id = self.playlist_id or self.audacious.get_currently_playing_playlist_id()

        copy_files(self.audacious.get_files_to_copy(number, playlist_id), target, renumber)

    def move_files_to_original_places(self, music_dir: str = os.path.expanduser('~/Music')) -> None:
        playlist_id = self.playlist_id or self.audacious.get_currently_playing_playlist_id()
        for file in self.audacious.files_in_playlist(playlist_id):
            move_file(file, music_dir)


def copy_files(files_to_copy: List[str], target_dir: str, renumber: bool) -> None:
    for i, file in enumerate(files_to_copy):
        filename = file.split('/')[-1]
        target_filename = renumber_file(filename, i + 1, len(files_to_copy)) if renumber \
            else filename
        logging.info("%s/%s: %s", i + 1, len(files_to_copy), target_filename)
        copy_file(file, os.path.join(target_dir, target_filename))


def find_file(name: str, path: str) -> str:
    for root, _, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return ''


def copy_file(file: str, target: str) -> None:
    try:
        copy2(file, target)
    except SameFileError as error:
        logging.warning(str(error))


def renumber_file(filename: str, number: int, total: int) -> str:
    width = max(int(log10(total)) + 1, 2)
    return f"{number:0{width}d} - {strip_leading_numbers(filename)}"


def move_file(file: str, music_dir: str):
    if os.path.isfile(file):
        return
    filename = file.split('/')[-1]
    target_dir = '/'.join(file.split('/')[:-1])
    original_file = find_file(filename, music_dir)
    if not original_file:
        return
    original_file_parent_dir = '/'.join(original_file.split('/')[:-1])
    files_to_move = [
        f for f in os.listdir(original_file_parent_dir)
        if os.path.isfile(original_file_parent_dir + '/' + f)
    ]
    logging.info('TO MOVE: %s %s %s', original_file, target_dir, files_to_move)
    os.makedirs(target_dir, exist_ok=True)
    for move in files_to_move:
        os.rename(original_file_parent_dir + '/' + move, target_dir + '/' + move)
        logging.info(
            '        MOVING %s -> %s', original_file_parent_dir + '/' + move, target_dir
        )
    os.rmdir(original_file_parent_dir)


def strip_leading_numbers(filename: str) -> str:
    return re.sub(r'^\d+\s*[-.]?\s*', '', filename)
