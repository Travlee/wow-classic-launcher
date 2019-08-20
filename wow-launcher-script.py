#!/usr/bin/env python3

import pyautogui, os, psutil, sys, time, subprocess, cv2, signal


PAT_REALM_LISTING = "patterns/realm.png"
PAT_REALM_QUE = "patterns/realm-que-pat.png"
PAT_LOGGING_QUE = "patterns/logging-pat.png"
BATTLE_NET_PLAY_PAT = "patterns/battlenet-play.png"
PAT_CHAR_SCREEN = "patterns/character-screen.png"
BATTLE_NET_PROCESS = "Battle.net.exe"
BATTLE_NET_EXE = "C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe"
WOW_PROCESS = "Wow.exe"
SECONDS_MAX_WAIT = 10
SECONDS_SLEEP = 5
# SECONDS_SLEEP = 60

STATE_INIT = 0
STATE_RUNNING = 1
STATE_WAITING = 2

def main():

  # state = STATE_INIT

  start = time.time()
  while True:
    # click_realm()
    # coords = find_pattern("patterns/realm-que-pat.png", .2)
    # coords = find_pattern(PAT_CHAR_SCREEN, .2)
    # coords = find_pattern(PAT_LOGGING_QUE, .3)
    # coords = find_pattern(PAT_REALM_QUE, .3)
    # print(coords)
    # if coords:
    #   pyautogui.moveTo(coords)


    # ? WOW PROCESS NOT FOUND; LAUNCH
    if not process_exists(WOW_PROCESS) and launch_wow():
      continue

    if should_wait():
      print("Waiting...")
      time.sleep(SECONDS_SLEEP)
      continue

    # coords = None
    # start = time.time()
    # while not coords:
    #   if start + SECONDS_MAX_WAIT <= time.time():
    #   coords = find_pattern(PAT_REALM_LISTING)

    coords = find_pattern(PAT_REALM_LISTING)
    if not coords and time.time() >= start + SECONDS_MAX_WAIT:
      print("Error finding realm listing... Restarting...")
      kill_process(WOW_PROCESS)
      launch_wow()
      start = time.time()
      continue
    elif coords:
      click([coords[0] + 30, coords[1] + 70])
      print("Logging into realm...")


    time.sleep(1)


def should_wait():
  start = time.time()
  while time.time() <= start + SECONDS_MAX_WAIT:

    # ? AT CHARACTER SCREEN, LOGGNG INTO REALM OR IN QUEUE
    # ? Sleep for a bit then check for a change...
    is_char_screen = find_pattern(PAT_CHAR_SCREEN, .6)
    is_logging = find_pattern(PAT_LOGGING_QUE, .3)
    is_realm_que = find_pattern(PAT_REALM_QUE, .3)

    if is_char_screen or is_logging or is_realm_que:
      return True

  return False


def launch_wow():
  if not process_exists(BATTLE_NET_PROCESS) and not process_exists(WOW_PROCESS):
    start_process(BATTLE_NET_EXE)
    print("Launching '%s'" % BATTLE_NET_PROCESS)

  play_coords = None
  start = time.time()
  while not play_coords:
    if start + SECONDS_MAX_WAIT <= time.time():
      print("Error finding battlenet client... Restarting...")
      kill_process(BATTLE_NET_PROCESS)
      start_process(BATTLE_NET_EXE)
      start = time.time()
      continue
    play_coords = find_pattern(BATTLE_NET_PLAY_PAT)

  click(play_coords)
  print("Launching '%s'" % WOW_PROCESS)

  is_wow_running = process_exists(WOW_PROCESS)
  start = time.time()
  while not is_wow_running:
    if start + SECONDS_MAX_WAIT <= time.time():
      print("Error launching wow... Restarting...")
      return False
    is_wow_running = process_exists(WOW_PROCESS)
    print("Wating for wow")

  return True


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


def start_process(process, args = ""):
  try:
    subprocess.Popen([process, args])
  except Exception as ex:
    print("Error launching %s" % process)
  else:
    return True
  return False


def kill_process(process):
  try:
    os.system("taskkill /f /im " + process + " >NUL")
  except:
    print("Error can't kill '%s'" % process)
    sys.exit(1)


def process_exists(process):
  try:
    if psutil.pid_exists(process):
      return process
  except:
    for proc in psutil.process_iter():
      try:
        if proc.name() == process:
          return proc.pid
      except:
        sys.exit(1)
  return False


def printr(string):
  print("timehere: %s" % string)

if __name__ == "__main__":
  main()
