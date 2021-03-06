# Blackjack game made using Python and Tkinter #

## Instructions ##

* To run you must have Python 3.7 installed and key packages like tkinter installed
* You must run the Blackjack.py file in a python IDE or command line to start the game. 
* In order to create an executable file in Windows 8.1/10 or above without having to run Python all the time, run this command:
    * pyinstaller --onefile -w Blackjack.py
    * Two folders will be created: Build and dist. Remove the build folder and drag out the Blackjack.exe file from the dist folder to the main blackjack-game folder.

![Python Blackjack game](https://raw.githubusercontent.com/amj18/blackjack-game/master/screenshots/blackjackgui_01.PNG)

**Blackjack version 1.0 currently allows the following:**
* First to get a score of 21 wins.
* Card scoring system is as follows: "TWO":2, "THREE":3, "FOUR":4, "FIVE":5, "SIX":6, "SEVEN":7, "EIGHT":8, "NINE":9, "TEN":10, "JACK":10, "QUEEN":10, "KING":10, "ACE":1
* The value of the Ace can change between 1 and 11, and a special condition is implemented to allow correct calculation of these values.
* Player or Dealer automatically win or lose depending if they reach 21, exceed it, or have a larger/lower spread than the other.
* Player can hit the "Hit" button as many times as long as the value is below 21.
* The simple dealer NPC automatically wins or loses during their turn of hitting a card.
* The player can export all history of the game only after clicking the Deal button for the first time.

**The following edge cases have been accounted for and allow for a smooth and bug free gameplay:**
* Deal, Hit and Stand buttons are disabled until player inputs a valid bet size.
* If player inputs an invalid bet size, they will be prompted to correct it.
* Player is not able to change bet size or do a new deal while hitting or standing.
* If player loses all money, a new game prompt will reset the game, bank, and scores.

**Edge cases not accounted for**
* The player can potentially keep hitting cards which will go off the game screen if the total value is less than 21. Player must click "stand" to end the round.

Playing card images from momo-ozawa: https://github.com/momo-ozawa
