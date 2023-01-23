"""
    @Author: Seakmeng Hor
    @Date: 1/23/2023
    @Description: About A Python script developed to simplify the process of logging into Jx Online with multiple accounts.
"""

import os
import time
import pyautogui
import pandas as pd

global game_paths

# Path to the game executable files.
with open("Data\path.csv", "r") as f:
    # get second line
    game_paths = f.readlines()[1]

# Asset
nokor_chey = "Asset\chey.jpg"
nokor_oudong = "Asset\oudong.jpg"
nokor_reach = "Asset\Reach.jpg"

# locate on screen asset
start_btn = "Asset\start.png"
select_server = "Asset\select-server.jpg"
confirm_btn = "Asset\confirm.png"
check_fill = "Asset\check_fill.jpg"


class GameOpener:
    def __init__(self, username, password, norkor):
        self.path = game_paths
        self.username = username
        self.password = password

        # define norkor
        if norkor == "chey":
            self.norkor = nokor_chey
        elif norkor == "oudong":
            self.norkor = nokor_oudong
        elif norkor == "reach":
            self.norkor = nokor_reach

    def open_game(self):
        print("\nOpening game for {user}...".format(user=self.username))

        os.startfile(self.path)

        for i in range(5):
            print("Starting in {time} {sec}...".format(
                time=5 - i, sec="second." if 5 - i == 1 else "seconds"))
            time.sleep(5)

        # locate on screen and click once
        # on start btn
        print("Scanning for start button...")
        self.locate_and_click(start_btn)

        # on select server
        print("Scanning for select server button...")
        self.locate_and_click(select_server)

        # on server
        print("Scanning for server button...")
        self.locate_and_click(self.norkor)

        # on confirm
        print("Scanning for confirm button...")
        self.locate_and_click(confirm_btn)

        # check available fill
        print("Scanning for fill button...")
        self.fill_info()

        # on confirm
        print("Scanning for confirm button...")
        self.locate_and_click(confirm_btn)

        print("Done! Logging in...\n")

    def locate_and_click(self, btn):
        try:
            while True:
                if pyautogui.locateCenterOnScreen(btn, confidence=0.7) is not None:
                    break
            pyautogui.click(pyautogui.locateCenterOnScreen(btn, confidence=0.7))
        except Exception as e:
            print(e)
            time.sleep(5)
            exit()

    def fill_info(self):
        while True:
            if pyautogui.locateCenterOnScreen(check_fill, confidence=0.7) is not None:
                pyautogui.typewrite(self.username)
                pyautogui.press("tab")
                pyautogui.typewrite(self.password)
                break

    def get_credential(self):
        # get credentials from csv file and store in list of class using pandas
        self.credential = pd.read_csv("Data\\account.csv")
        self.credential = self.credential.values.tolist()
        self.credential = [GameOpener(i[0], i[1], i[2])
                           for i in self.credential]

    def main(self):
        # get credentials for each game.
        self.get_credential(self)

        # Open each game in a separate window and login automatically
        for i in range(len(self.credential)):
            self.credential[i].open_game()
            if (i != len(self.credential) - 1):
                print("\nStarting another game in 5 seconds...\n")
            else:
                print("\nAll accounts has been logged in\n")


if __name__ == "__main__":
    GameOpener.main(GameOpener)
