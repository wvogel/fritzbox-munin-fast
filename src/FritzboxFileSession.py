#!/usr/bin/env python3
"""
  Handling FRITZ!Box file sessions
"""

import os

def get_session_dir() -> str:
  return os.getenv('MUNIN_PLUGSTATE') + '/fritzbox'

class FritzboxFileSession:
  __separator = "__"
  __server = ""
  __user = ""
  __port = None

  # default constructor
  def __init__(self, server: str, user: str, port: int):
    if self.__separator in server or self.__separator in user:
      raise Exception("Reserved string \"" + self.__separator + "__\" in server or user name")

    self.__server = server
    self.__user = user
    self.__port = port

  def __get_session_filename(self) -> str:
    return self.__server + self.__separator + str(self.__port) + self.__separator + self.__user + '.sid'

  def save_session_id(self, session_id):
    statedir = get_session_dir()

    if not os.path.exists(statedir):
      os.makedirs(statedir)

    statefilename = statedir + '/' + self.__get_session_filename()

    with open(statefilename, 'w', encoding='utf8') as statefile:
      statefile.write(session_id)

  def load_session_id(self) -> str:
    statefilename = get_session_dir() + '/' + self.__get_session_filename()
    if not os.path.exists(statefilename):
      return None

    with open(statefilename, 'r', encoding='utf8') as statefile:
      session_id = statefile.readline()
      return session_id

  def clear_session(self):
    os.remove(get_session_dir() + '/' + self.__get_session_filename())
