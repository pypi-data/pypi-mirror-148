import ast
import subprocess

import AppKit
import Quartz

from pywinctl import pointInRect, BaseWindow, Rect, Point, Size, Re, _WinWatchDog

WS = AppKit.NSWorkspace.sharedWorkspace()


def _getAllApps(userOnly: bool = True):

    matches = []
    for app in WS.runningApplications():
        if not userOnly or (userOnly and app.activationPolicy() == Quartz.NSApplicationActivationPolicyRegular):
            matches.append(app)
    return matches


def _getWindowTitles():
    # https://gist.github.com/qur2/5729056 - qur2
    cmd = """osascript -s s -e 'tell application "System Events"
                                    set winNames to {}
                                    try
                                        set winNames to {unix id, ({name, position, size} of (every window))} of (every process whose background only is false)
                                    end try
                                end tell
                                return winNames'"""
    ret = subprocess.check_output(cmd, shell=True).decode(encoding="utf-8").replace("\n", "").replace("{", "[").replace("}", "]")
    res = ast.literal_eval(ret)
    result = []
    for i, pID in enumerate(res[0]):
        item = res[1][0][i]
        j = 0
        for title in item:  # One-liner script is way faster, but produces complex data structures
            pos = res[1][1][i][j]
            size = res[1][2][i][j]
            result.append([pID, title, pos, size])
            j += 1
    return result


def getAllWindows():
    activeApps = _getAllApps()
    print(activeApps)
    print()
    titleList = _getWindowTitles()
    print(titleList)
    print()
    for item in titleList:
        pID = item[0]
        title = item[1]
        x = int(item[2][0])
        y = int(item[2][1])
        w = int(item[3][0])
        h = int(item[3][1])
        rect = Rect(x, y, x + w, y + h)
        for app in activeApps:
            if app.processIdentifier() == pID:
                print(app.localizedName(), title, rect)
                break


getAllWindows()
