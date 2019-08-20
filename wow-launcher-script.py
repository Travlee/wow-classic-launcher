#!/usr/bin/env python3

import pyautogui, os, psutil, sys, time, subprocess, cv2, signal


PAT_REALM_LISTING = "patterns/realm.png"
PAT_REALM_QUE = "patterns/realm-que-pat.png"
PAT_LOGGING = "patterns/logging-pat.png"
PAT_BNET_PLAY = "patterns/battlenet-play.png"
PAT_CHAR_SCREEN = "patterns/character-screen.png"
PROCESS_BNET = "Battle.net.exe"
EXE_BNET = "C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe"
PROCESS_WOW = "Wow.exe"
SECONDS_MAX_WAIT = 15
SECONDS_SLEEP = 15
SECONDS_IDLE = 60*10
SECONDS_CHAR_SCREEN = 60

STATE_INIT = "INIT"
STATE_RUNNING = "RUNNING"
STATE_IDLE = "IDLE"
STATE_RESTART = "RESTART"
STATE_LAUNCH_WOW = "LAUNCHING_WOW"
STATE_WAIT_WOW = "WAITING_WOW"
STATE_LAUNCH_BNET = "LAUNCHING_BNET"
STATE_WAIT_BNET = "WAITING_BNET"
STATE_LOAD_REALM = "LOADING_REALM"
STATE_CHAR_SCREEN = "CHARACTER_SCREEN"

def main():
  state = STATE_INIT
  is_bnet_running = False
  is_wow_running = False
  is_realm_list = False
  is_logging = False
  is_realm_que = False
  is_char_screen = False

  state = STATE_RUNNING
  timer = None
  while True:
    current = time.time()

    is_bnet_running = get_is_bnet_running()
    is_wow_running = get_is_wow_running()
    is_char_screen = get_is_char_screen()
    is_realm_que =  get_is_realm_que()
    is_logging = get_is_logging()
    is_realm_list = get_is_realm_list()

    if state == STATE_RUNNING:
      if not is_wow_running:
        if is_bnet_running:
          state = STATE_LAUNCH_WOW
        else:
          state = STATE_LAUNCH_BNET
      else:
        if is_char_screen :
          state = STATE_CHAR_SCREEN
          timer = current + SECONDS_MAX_WAIT
        elif is_logging or is_realm_que:
          state = STATE_IDLE
        elif is_realm_list:
          state = STATE_LOAD_REALM
          timer = current + SECONDS_MAX_WAIT
        else:
          timer = current + SECONDS_MAX_WAIT
          state = STATE_RESTART


    elif state == STATE_LAUNCH_BNET:
      if launch_bnet():
        state = STATE_WAIT_BNET
        timer = current


    elif state == STATE_WAIT_BNET:
      if current >= timer + SECONDS_MAX_WAIT:
        print("Error timed-out waiting for %s" % EXE_BNET)
        state = STATE_RUNNING
      elif is_bnet_running:
          state = STATE_RUNNING


    elif state == STATE_LAUNCH_WOW:
      launch_wow()
      state = STATE_WAIT_WOW
      timer = current


    elif state == STATE_WAIT_WOW:
      if current >= timer + SECONDS_MAX_WAIT:
        print("Error timed-out waiting for %s" % PROCESS_WOW)
        state = STATE_LAUNCH_BNET
      elif is_wow_running:
          state = STATE_RUNNING


    elif state == STATE_IDLE:
      if is_logging or is_realm_que:
        sleep(SECONDS_SLEEP, "Waiting for login/queue...")
      else:
        state = STATE_RUNNING


    elif state == STATE_LOAD_REALM:
      if current >= timer:
        print("Error finding realm listing... Restarting...")
        state = STATE_RESTART
      else:
        load_realm()
        state = STATE_CHAR_SCREEN


    elif state == STATE_CHAR_SCREEN:
      if current >= timer:
        print("Error confirming character screen... Restarting...")
        state = STATE_RESTART
      elif is_char_screen:
        sleep(SECONDS_CHAR_SCREEN)
        state = STATE_RUNNING


    elif state == STATE_RESTART:
      if current >= timer:
        launch_wow()
        print("Testing")
        state = STATE_RUNNING
      elif is_char_screen or is_logging or is_realm_que or is_realm_list:
        state = STATE_RUNNING




    print(is_bnet_running, is_wow_running, is_char_screen, is_realm_que, is_logging, is_realm_list, state)


def sleep(count=1, msg=""):
  print("%s" % msg if msg else "Sleeping for %s seconds..." % count)
  time.sleep(count)

def get_is_bnet_running():
  return process_exists(PROCESS_BNET)

def get_is_wow_running():
  return process_exists(PROCESS_WOW)

def get_is_char_screen():
  return find_pattern(PAT_CHAR_SCREEN, .5)

def get_is_realm_que():
  return find_pattern(PAT_REALM_QUE, .3)

def get_is_logging():
  return find_pattern(PAT_LOGGING, .3)

def get_is_realm_list():
  return find_pattern(PAT_REALM_LISTING, .3)

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
  except:
    print("Error can't kill '%s'" % process)

def find_pattern(pattern, confidence=.7):
  try:
    return pyautogui.locateCenterOnScreen(pattern, grayscale=False, confidence=confidence)
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
    print("Killing rogue %s" % PROCESS_BNET)

  try:
    subprocess.Popen([EXE_BNET])
    return True
  except Exception as ex:
    print("Error launching %s" % EXE_BNET, ex)

  return False

def launch_wow():
  if get_is_wow_running():
    process_kill(PROCESS_WOW)
    print("Killing rogue %s" % PROCESS_WOW)
  # print("Launching Wow")
  # return True

  coords = find_pattern(PAT_BNET_PLAY)

  if coords:
    click(coords)


  # play_coords = None
  # start = time.time()
  # while not play_coords:
  #   if start + SECONDS_MAX_WAIT <= time.time():
  #     print("Error finding battlenet client... Restarting...")
  #     kill_process(BATTLE_NET_PROCESS)
  #     start_process(BATTLE_NET_EXE)
  #     start = time.time()
  #     continue
  #   play_coords = find_pattern(BATTLE_NET_PLAY_PAT)

  # click(play_coords)
  # print("Launching '%s'" % WOW_PROCESS)

  # is_wow_running = process_exists(WOW_PROCESS)
  # start = time.time()
  # while not is_wow_running:
  #   if start + SECONDS_MAX_WAIT <= time.time():
  #     print("Error launching wow... Restarting...")
  #     return False
  #   is_wow_running = process_exists(WOW_PROCESS)
  #   print("Wating for wow")

def load_realm():
  coords = find_pattern(PAT_REALM_LISTING)
  if coords:
    click([coords[0] + 30, coords[1] + 70])
    print("Logging into Realm")


if __name__ == "__main__":
  main()
