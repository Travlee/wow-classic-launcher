#!/usr/bin/env python3

import pyautogui, os, psutil, sys, time, subprocess, cv2


REALM_PAT = "patterns/realm.png"
BATTLE_NET_PLAY_PAT = "patterns/battlenet-play.png"
BATTLE_NET_PROCESS = "Battle.net.exe"
BATTLE_NET_EXE = "C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe"
WOW_PROCESS = "Wow.exe"

def main():

  while True:

    launch_battlenet()
    launch_wow()
    click_realm()
    # stay_active()


def launch_battlenet():
  if process_exists(BATTLE_NET_PROCESS) is False:
    print("Launching '%s'" % BATTLE_NET_PROCESS)
    return start_process(BATTLE_NET_EXE)


def launch_wow():
  if process_exists(WOW_PROCESS) is False and process_exists(BATTLE_NET_PROCESS):
    print("Launching '%s'" % WOW_PROCESS)
    coords = find_pattern(BATTLE_NET_PLAY_PAT)
    if coords:
      click(coords)
      return
    else:
      print("...Can't find Battlenet client")


def click_realm():
  if process_exists(BATTLE_NET_PROCESS) and process_exists(WOW_PROCESS):
    coords = find_pattern(REALM_PAT)
    if coords:
      click([coords[0] + 30, coords[1] + 70])


def find_pattern(pattern):
  try:
    # return pyautogui.locateOnScreen(pattern, grayscale=False, confidence=.7)
    return pyautogui.locateCenterOnScreen(pattern, grayscale=False, confidence=.7)
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


if __name__ == "__main__":
  main()
