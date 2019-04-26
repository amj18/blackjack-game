from tkinter import *
from random import randint
import os

class CardLabel(Label):
    """
    A CardLabel is a Tk Label that displays an image of a playing card
    """
    
    def __init__(self, parent):
        """The default image for a new label is the back of a card"""
        Label.__init__(self, parent, image=CardLabel.back_image)
    
    image_directory = "./cardimages/"
	#image_directory = os.getcwd()
    
    @staticmethod
    def getImgList():
        CardLabel.imageList = [CardLabel.image_directory + "card{}.gif".format(i) for i in range(52)]
    
    @staticmethod
    def load_images():
        """Get the card images from files, save them in a list (a class variable)"""        
        CardLabel.images = [PhotoImage(file=CardLabel.image_directory + "card{}.gif".format(i)) for i in range(52)]
        CardLabel.back_image = PhotoImage(file=CardLabel.image_directory + "back-blue.gif")
        CardLabel.blank_image = PhotoImage(file=CardLabel.image_directory + "blank.gif")
    
    def display(self, side='back', id=0):
        """
        Change the label to show a new side of a card. If showing the
        front side the id parameter specifies which image is chosen (otherwise
        that parameter is ignored).
        """
        if side == 'back':
            self.configure(image=CardLabel.back_image) # configure shows image on the Tk screen
        elif side == 'front':
            self.configure(image=CardLabel.images[id])
        else: # if blank entered
            self.configure(image=CardLabel.blank_image)   