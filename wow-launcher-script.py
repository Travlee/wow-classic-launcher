#!/usr/bin/env python3

import pyautogui, os, psutil, sys, subprocess, cv2, signal, patterns
from time import time
from time import sleep

PROCESS_BNET = "Battle.net.exe"
EXE_BNET = "C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe"
PROCESS_WOW = "Wow.exe"
SECONDS_MAX_WAIT = 15
SECONDS_MAX_WAIT_PROCESS = 30
SECONDS_SLEEP = 15
SECONDS_CHAR_SCREEN = 30
SECONDS_LOOP_WAIT = 1
STATE_INIT = "INIT"
STATE_LAUNCH_WOW = "LAUNCHING_WOW"
STATE_WAIT_WOW = "WAITING_WOW"
STATE_LAUNCH_BNET = "LAUNCHING_BNET"
STATE_WAIT_BNET = "WAITING_BNET"
STATE_CHAR_SCREEN = "CHARACTER_SCREEN"
STATE_REALM_WAIT = "REALM_WAIT"
STATE_REALM_LIST = "REALM_LIST"
STATE_REALM_QUE = "REALM_QUE"
STATE_GAMESERVER_WAIT = "GAMESERVER_WAIT"
STATE_CONNECTING_WAIT = "CONNECTING_WAIT"
STATE_HAPPINESS = r"""
                      WELCOME HOME, FRIENDS!!!
                      Also, dying now. Enjoy...
         .(O).      /
     o.`       `.o
     /_ _ _ _ _ _\
      |==|===|==|
      |==|===|==|
      |_=|===|=_|
.-._.-[]\_____/[]-O
 -'   /=|=|=|=|=\
     |o |o|o|o| o|
     |o |o|o|o| o|
     |o |o|o|o| o|
     '-.|o|o|o|.-'
     '--.=====.--'
"""

def main():

  state = STATE_INIT
  timer = time()
  last = timer
  timeout = 0

  while True:
    if time() <= last + SECONDS_LOOP_WAIT:
      continue
    # print("\nSTATE:", state, "\nEXE_TIME:", (time() - last), "\nTIMER:", (timer - time()), "\n")
    last = time()


    if state == STATE_INIT:
      if not get_is_wow_running():
        if get_is_bnet_running() and get_is_bnet_visible():
          state = STATE_LAUNCH_WOW
        else:
          state = STATE_LAUNCH_BNET
      else:

        if get_is_char_screen():
          print("Found character screen")
          state = STATE_CHAR_SCREEN

        if get_is_gameserver_wait():
          state = STATE_GAMESERVER_WAIT

        if get_is_realm_que():
          state = STATE_REALM_QUE

        if get_is_realm_list():
          state = STATE_REALM_LIST

        if get_is_realm_wait():
          state = STATE_REALM_WAIT

        if get_is_connecting():
          state = STATE_CONNECTING_WAIT

        if state == STATE_INIT:
          state = STATE_LAUNCH_WOW

      timer = time() + SECONDS_MAX_WAIT_PROCESS
      timeout = 0
      continue


    elif state == STATE_LAUNCH_BNET:
      if launch_bnet():
        state = STATE_WAIT_BNET
        timer = time() + SECONDS_MAX_WAIT_PROCESS
      continue


    elif state == STATE_WAIT_BNET:
      if get_is_bnet_running() and get_is_bnet_visible():
        state = STATE_LAUNCH_WOW
        timer = time() + SECONDS_MAX_WAIT_PROCESS
      elif time() >= timer:
        state = STATE_LAUNCH_BNET
      continue


    elif state == STATE_LAUNCH_WOW:
      if (not get_is_bnet_running() or not get_is_bnet_visible()) and not get_is_wow_running():
        state = STATE_LAUNCH_BNET
        timer = time() + SECONDS_MAX_WAIT_PROCESS
      elif launch_wow():
        state = STATE_WAIT_WOW
        timer = time() + SECONDS_MAX_WAIT_PROCESS
      elif time() >= timer:
        state = STATE_LAUNCH_BNET
      continue


    elif state == STATE_WAIT_WOW:
      if get_is_wow_running():
        state = STATE_CONNECTING_WAIT
        timer = time() + SECONDS_MAX_WAIT
      elif time() >= timer:
        state = STATE_LAUNCH_WOW
        timer = time() + SECONDS_MAX_WAIT_PROCESS
      continue


    elif state == STATE_CONNECTING_WAIT or state == STATE_REALM_WAIT:
      if get_is_connecting() or get_is_realm_wait():
        # msleep(SECONDS_SLEEP, "Waiting for connection/realm...")
        print("Waiting for connection...")
        timer = time() + SECONDS_MAX_WAIT
      elif get_is_realm_list():
        state = STATE_REALM_LIST
        timer = time() + SECONDS_MAX_WAIT
      elif time() >= timer:
        print("Error waiting for connection/realm listing... Restarting...")
        state = STATE_LAUNCH_WOW
        timer = time() + SECONDS_MAX_WAIT
      continue


    elif state == STATE_REALM_LIST:
      if load_realm():
          state = STATE_GAMESERVER_WAIT
          timer = time() + SECONDS_MAX_WAIT
      elif time() >= timer:
        print("Error finding realm listing... Restarting...")
        state = STATE_GAMESERVER_WAIT
        timer = time() + SECONDS_MAX_WAIT
      continue


    elif state == STATE_REALM_QUE:
      if get_is_gameserver_wait():
        state = STATE_GAMESERVER_WAIT
        timer = time() + SECONDS_MAX_WAIT
      elif get_is_char_screen():
        print("Found character screen")
        state = STATE_CHAR_SCREEN
        timer = time() + SECONDS_MAX_WAIT
      elif get_is_realm_que():
        print("Waiting for realm queue...")
        timer = time() + SECONDS_MAX_WAIT
      elif time() >= timer:
        state = STATE_GAMESERVER_WAIT
        timer = time() + SECONDS_MAX_WAIT
      continue


    elif state == STATE_GAMESERVER_WAIT:
      if get_is_gameserver_wait():
        print("Waiting for gameserver...")
        timer = time() + SECONDS_MAX_WAIT
      elif get_is_char_screen():
        print("Found character screen")
        state = STATE_CHAR_SCREEN
        timer = time() + SECONDS_MAX_WAIT
      elif get_is_realm_list():
        state = STATE_REALM_LIST
        print("Back to realmlist for some reason.")
      elif time() >= timer:
        print("Error timed out waiting for gameserver... Restarting...")
        state = STATE_INIT
      continue


    elif state == STATE_CHAR_SCREEN:
      salvation = get_is_live()
      if salvation:
        click(salvation)
        print(STATE_HAPPINESS)
        sys.exit(0)
      elif get_is_char_screen():
        if timeout == 0:
          timeout = time() + 60*30
          print("Time till timeout: 30 minutes")
        else:
          doom = int((timeout - time()))
          if doom % 300 == 0:
            print("Time till timeout: %s minutes" % int((timeout - time()) / 60))
        timer = time() + SECONDS_CHAR_SCREEN
      elif not get_is_wow_running():
        state = STATE_INIT
      elif time() >= timer and not get_is_char_screen():
        print("Error confirming character screen... Restarting...")
        state = STATE_INIT
      elif time() >= timer - (SECONDS_CHAR_SCREEN/2):
        print("Losing character screen...")


def msleep(count=1, msg=""):
  print("%s - sleeping for %s seconds" % (msg, count) if msg else "Sleeping for %s seconds..." % count)
  sleep(count)

def get_is_live():
  return find_pattern(patterns.CHAR_SCREEN_LIVE, .7, grayscale=False)

def get_is_bnet_running():
  return process_exists(PROCESS_BNET)

def get_is_bnet_visible():
  return find_pattern(patterns.BNET_PLAY, .6)

def get_is_wow_running():
  return process_exists(PROCESS_WOW)

def get_is_char_screen():
  return find_pattern(patterns.CHAR_SCREEN_DOWN, .5) or get_is_live()

def get_is_realm_que():
  return find_pattern(patterns.REALM_QUE, .3)

def get_is_gameserver_wait():
  return find_pattern(patterns.GAMESERVER_WAIT, .4)

def get_is_realm_list():
  return find_pattern(patterns.REALM_LIST, .3)

def get_is_connecting():
  return find_pattern(patterns.CONNECTING, .6)

def get_is_realm_wait():
  return find_pattern(patterns.REALM_WAIT, .6)

def process_exists(process):
  try:
    if psutil.pid_exists(process):
      return process
  except:
    for proc in psutil.process_iter():
      try:
        if proc.name() == process:
          return True
      except Exception as ex:
        print("Error", ex)
  return False

def process_kill(process):
  try:
    os.system("taskkill /f /im " + process + " >NUL")
    print("Killing rogue '%s'" % process)
  except:
    print("Error can't kill '%s'" % process)

def find_pattern(pattern, confidence=.7, grayscale=True):
  try:
    return pyautogui.locateCenterOnScreen(pattern, grayscale=grayscale, confidence=confidence)
  except:
    return False

def click(coords):
  try:
    pyautogui.doubleClick(coords)
  except:
    print("Error can't click idk weird ...")
    sys.exit(1)

def launch_bnet():
  if get_is_bnet_running():
    process_kill(PROCESS_BNET)

  try:
    subprocess.Popen([EXE_BNET])
    print("Launching %s" % EXE_BNET)
    return True
  except Exception as ex:
    print("Error launching %s" % EXE_BNET, ex)
    sys.exit(1)

  return False

def launch_wow():
  if get_is_wow_running():
    process_kill(PROCESS_WOW)

  coords = get_is_bnet_visible()

  if coords:
    click(coords)
    print("Launching %s" % PROCESS_WOW)
    return True

  return False

def load_realm():
  coords = get_is_realm_list()
  if coords:
    click([coords[0] + 30, coords[1] + 60])
    print("Logging into Realm")
    return True
  return False


if __name__ == "__main__":
  main()
