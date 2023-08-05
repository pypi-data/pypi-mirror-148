"Functions related to the episode info DB"

import hashlib
import os, sys
from os.path import expanduser

from sqlobject import SQLObject, col, main, sqlite, SQLObjectNotFound

import logging


class Episode(SQLObject):
    "A DB entry of things we want to remember about an episode"
    hash = col.UnicodeCol(unique=True, alternateID=True)
    pubdate = col.DateTimeCol()
    played = col.BoolCol(default=False)


def init_db(data_dir):
    Episode._connection = sqlite.builder()(
        expanduser(data_dir + os.sep + "episodes.db"), debug=False
    )
    Episode.createTable(ifNotExists=True)


def episode_hash(episode):
    return hashlib.sha1(episode["title"].encode("ascii", "ignore")).hexdigest()


def markDownloaded(episode):
    logging.debug('Mark DLed')
    if not seen(episode):
        Episode(hash=episode.hash, pubdate=episode.pub_date)


def markPlayed(episode):
    logging.debug('Mark Played')
    e = seen(episode)
    e.played = True


def seen(episode):
    logging.debug(f'Searching Episode {episode.title}, hash {episode.hash}')
    try:
        e = Episode.byHash(episode.hash)
        logging.debug(f'Found Episode {e}')
        return e


    except SQLObjectNotFound:
        logging.debug('not found')
        return None

if __name__ == '__main__':

    data_dir = '~/.local/share/podpuller'
    init_db(data_dir)

    assert (len(sys.argv) > 1), 'No command specified'
    cmd = sys.argv[1]

    Episode._connection.debug = True
    eps = Episode.select()
    print(list(eps))   
 