#!env/python3
# coding: utf-8
import os
import datetime
import logging
import uuid
import time
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.exc import IntegrityError

from config import ANNSO_DIR


# =====================================================================================================================
# TOOLS
# =====================================================================================================================


def humansize(nbytes):
    """
        Todo : doc
    """
    suffixes = ['o', 'Ko', 'Mo', 'Go', 'To', 'Po']
    if nbytes == 0:
        return '0 o'
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def array_diff(array1, array2):
    """
        Return the list of element in array2 that are not in array1
    """
    return [f for f in array2 if f not in array1]


def array_merge(array1, array2):
    """
        Merge the two arrays in one (by removing duplicates)
    """
    result = []
    for f in array1:
        if f not in result:
            result.append(f)
    for f in array2:
        if f not in result:
            result.append(f)
    return result





# =====================================================================================================================
# LOGS MANAGEMENT
# =====================================================================================================================


def setup_logger(logger_name, log_file, level=logging.INFO):
    """
        Todo : doc
    """
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s | %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)


def log(msg):
    global plog
    plog.info(msg)


def war(msg):
    global plog
    plog.warning(msg)


def err(msg):
    global plog
    plog.error(msg)


# =====================================================================================================================
# ERROR MANAGEMENT
# =====================================================================================================================


class AnnsoException(Exception):
    """
        Todo : doc
    """
    msg = "Unknow error :/"
    code = 0
    id = None
    date = None

    def __init__(self, msg: str, code: int=0, logger=None):
        self.code = AnnsoException.code
        self.msg = AnnsoException.msg
        self.id = str(uuid.uuid4())
        self.date = datetime.datetime.utcnow().timestamp()

        if logger is not None:
            logger.err(msg)

    def __str__(self):
        return "[ERROR:{:05}] {} : {}".format(self.code, self.id, self.msg)


# =====================================================================================================================
# TIMER
# =====================================================================================================================


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            log(self.msecs, ' ms')

    def __str__(self):
        if self.msecs >= 1000:
            return "{0} s".format(self.secs)
        return "{0} ms".format(self.msecs)

    def total_ms(self):
        return self.msecs

    def total_s(self):
        return self.secs


# =====================================================================================================================
# INIT OBJECTS
# =====================================================================================================================

# Create annso logger : plog
setup_logger('annso', os.path.join(ANNSO_DIR, "annso.log"))
plog = logging.getLogger('annso')


# =====================================================================================================================
# DATA MODEL TOOLS
# =====================================================================================================================
CHR_DB_MAP = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 20: "20", 21: "21", 22: "22", 23: "X", 24: "Y", 25: "M"}
CHR_DB_RMAP = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12, "13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18, "19": 19, "20": 20, "21": 21, "22": 22, "X": 23, "Y": 24, "M": 25}


def chr_from_db(chr_value):
    if chr_value in CHR_DB_MAP.keys():
        return CHR_DB_MAP[chr_value]
    return None


def chr_to_db(chr_value):
    if chr_value in CHR_DB_RMAP.keys():
        return CHR_DB_RMAP[chr_value]
    return None
