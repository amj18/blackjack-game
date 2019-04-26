from CardAssets import CardLabel
from CardDeck import Deck, Hand, Chips
from tkinter import *
from tkinter import messagebox
import functools
import io
import logging
import shutil
import datetime

stream = io.StringIO()
handler = logging.StreamHandler(stream)
logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def calltracker(func):
    @functools.wraps(func)
    def wrapper(*args):
        wrapper.has_been_called = True
        return func(*args)
    wrapper.has_been_called = False
    return wrapper

def new_game():
    global frame_gameStats
    global frame_cardDisplay
    global frame_gameControls
    global frame_gameOutcomes
    global player_score_update
    global dealer_score_update
    global player_bank_update
    global round_number_update
    global in_play
    global dealer_label
    global player_label
    global outcome
    global round_number
    global bet_size
    global total_chips   
    global player_score
    global dealer_score
    global hit_button
    global stand_button
    global deal_button
    global entry_bet_size
    global submit_button
    global game_outcome_update
    
    if game_over.has_been_called == True:
        frame_gameControls.destroy()
        frame_gameStats.destroy()
        frame_cardDisplay.destroy()
        frame_gameOutcomes.destroy()

    in_play = False
    outcome = "Hit or stand?"
    player_score = 0
    dealer_score = 0
    total_chips = 1000
    total_chips = Chips(total_chips)
    bet_size = 0
    round_number = 0
    
    frame_gameStats = Frame(root)
    frame_gameStats.pack()
    player_score_update = Label(frame_gameStats, text="Player score {}".format(""))
    player_score_update.grid(row=0, column=0,padx=50)
    dealer_score_update = Label(frame_gameStats, text="Dealer score {}".format(""))
    dealer_score_update.grid(row=1, column=0,padx=10,pady=10)
    player_bank_update = Label(frame_gameStats, text="Player bank ${}".format(total_chips.total))
    player_bank_update.grid(row=0, column=5,padx=50)
    round_number_update = Label(frame_gameStats, text="Round number {}".format(""))
    round_number_update.grid(row=1, column=5,padx=10,pady=10)
    
    frame_cardDisplay = Frame(root)
    frame_cardDisplay.pack()
    CardLabel.load_images()
    
    dealer_label = [0]*7
    player_label = [0]*7
    
    Label(frame_cardDisplay, text="DEALER").grid(row=0, column=3)
    for card in range(7):       
        dealer_label[card] = CardLabel(frame_cardDisplay)
        dealer_label[card].grid(row=1, column=card, padx=10, pady=10)
        dealer_label[card].display("blank")    
    
    Label(frame_cardDisplay, text="PLAYER").grid(row=2, column=3)
    for card in range(7):
        player_label[card] = CardLabel(frame_cardDisplay)
        player_label[card].grid(row=3, column=card, pady=10)
        player_label[card].display("blank")        
    
    frame_gameControls = Frame(root)
    frame_gameControls.pack()
    Label(frame_gameControls, text="Enter bet size").grid(row=0, column=0,padx=10) # Will be greyed out after bet is in place
    entry_bet_size = Entry(frame_gameControls, width=24)
    entry_bet_size.grid(row=0, column = 1, columnspan=2,padx=10, pady=10)
    
    submit_button = Button(frame_gameControls, text="Submit", command = take_bet)
    submit_button.grid(row=0, column=3,padx=10, pady=10)
    deal_button = Button(frame_gameControls, text="Deal", state=DISABLED, command = deal)
    deal_button.grid(row=4, column=0,padx=10, pady=10)
    hit_button = Button(frame_gameControls, text="Hit", state=DISABLED, command = hit)
    hit_button.grid(row=4, column=1,padx=10, pady=10)
    stand_button = Button(frame_gameControls, text="Stand", state=DISABLED, command = stand)
    stand_button.grid(row=4, column=2,padx=10, pady=10)
    
    frame_gameOutcomes = Frame(root)
    frame_gameOutcomes.pack()
    game_outcome_update = Label(frame_gameOutcomes, wraplength=400,text="")
    game_outcome_update.grid(row=0,column=0)
    
    frame_gameStats.config(height=100, width=200)
    frame_gameControls.config(height=100, width=200)        
    
def reset():
    global dealer_hand, player_hand, dealer_label, player_label
    dealer_hand = []
    player_hand = []
    for card in range(7):       
        dealer_label[card].display("blank")  
        player_label[card].display("blank")
      
def new_deal():
    global unshuffled, deck, player_score, dealer_score, round_number, bet_size, total_chips, outcome, game_outcome_update, in_play, player_hand, dealer_hand, player_label, dealer_label   
     
    unshuffled = Deck()
    deck = Deck()
    deck.shuffle()    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())   
    
    dealer_label[0].display('back', unshuffled.get_id(dealer_hand.get_hand()[0]))
    dealer_label[1].display('front', unshuffled.get_id(dealer_hand.get_hand()[1]))
    player_label[0].display('front', unshuffled.get_id(player_hand.get_hand()[0]))
    player_label[1].display('front', unshuffled.get_id(player_hand.get_hand()[1]))
    
    hit_button.configure(state=NORMAL)
    stand_button.configure(state=NORMAL)

def deal():
    global player_score, dealer_score, round_number, bet_size, total_chips, outcome, game_outcome_update, in_play, player_hand, dealer_hand, player_label, dealer_label, button_state
    reset()
    new_deal()        
    in_play = True        
    button_state = "Cards dealt..."
    game_outcome_update.config(text=button_state)
    deal_button.configure(state=DISABLED)
    file.entryconfig(0, state=NORMAL) # activates export drop down submenu
    
def new_bet_state():
    deal_button.configure(state=DISABLED)
    hit_button.configure(state=DISABLED)
    stand_button.configure(state=DISABLED)
    submit_button.configure(state=NORMAL)
    entry_bet_size.config(state=NORMAL)
    entry_bet_size.delete(0, END)      

def hit():
    global deck, player_score, dealer_score, round_number, bet_size, total_chips, outcome, game_outcome_update, in_play, player_hand, dealer_hand, player_label, dealer_label, button_state
    
    in_play = True
    card_index = len(player_hand.get_hand())
    player_hand.add_card(deck.deal_card())
    player_label[card_index].display('front', unshuffled.get_id(player_hand.get_hand()[-1]))    
    button_state = "Hit..."
    game_outcome_update.config(text=button_state)       
    while in_play:        
        if player_hand.get_value() <= 21:
            in_play = False 
        elif player_hand.get_value() > 21:
            dealer_label[0].display('front', unshuffled.get_id(dealer_hand.get_hand()[0]))
            dealer_score += 1
            update_stats()          
            in_play = False            
            new_bet_state()
            if total_chips.total == 0:     
                game_over()                
            else:
                outcome = "PLAYER BUSTED. DEALER WINS. NEW DEAL?"
                game_outcome_update.config(text=outcome)    
    export_results()

def update_stats():
    global player_score, dealer_score, round_number, player_bank_update
    player_score_update.config(text = 'Player score {}'.format(player_score))
    dealer_score_update.config(text = 'Dealer score {}'.format(dealer_score))
    round_number_update.config(text = 'Round number {}'.format(round_number))    
    
def reveal_all_cards(card_size):
    for i in range(card_size-1):
        dealer_label[i].display('front', unshuffled.get_id(dealer_hand.get_hand()[i]))       

def export_button():
    handler.flush()
    with open("results.txt", "w") as fd:
        stream.seek(0)
        shutil.copyfileobj(stream, fd)

def export_results():    
    logger.info(datetime.datetime.now())
    logger.info('Round number {}'.format(round_number))  
    logger.info(button_state)    
    logger.info('Bet size ${}'.format(total_chips.bet)) 
    logger.info("Dealer {}".format(dealer_hand))
    logger.info("Player {}".format(player_hand))
    logger.info("Player hand value {}".format(player_hand.get_value()))
    logger.info("Dealer hand value {}".format(dealer_hand.get_value()))
    logger.info('Player score {}'.format(player_score))
    logger.info('Dealer score {}'.format(dealer_score))         
    logger.info('Player bank ${}'.format(total_chips.total)) 
    logger.info('#---------------------#')   
    
def stand():
    global deck, player_score, dealer_score, round_number, bet_size, total_chips, outcome, game_outcome_update, in_play, player_hand, dealer_hand, player_label, dealer_label, card_index, button_state 
    in_play = False
    card_index = len(dealer_hand.get_hand())
    dealer_label[card_index-1].display('back', unshuffled.get_id(dealer_hand.get_hand()[-1]))  
    if dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())        
    card_index = len(dealer_hand.get_hand())
    dealer_label[card_index-1].display('front', unshuffled.get_id(dealer_hand.get_hand()[-1]))  
    
    button_state = "Stand..."
    game_outcome_update.config(text=button_state)       
    
    if dealer_hand.get_value() > 21: 
        reveal_all_cards(len(dealer_hand.get_hand()))
        outcome = "DEALER BUSTED. PLAYER WINS. NEW DEAL?"
        game_outcome_update.config(text=outcome)        
        player_score+=1        
        new_bet_state()
        total_chips.win_bet()
        player_bank_update.config(text = 'Player bank ${}'.format(total_chips.total))  
        update_stats()        
    else:
        reveal_all_cards(len(dealer_hand.get_hand()))
        if dealer_hand.get_value() >= player_hand.get_value() or player_hand.get_value() > 21:
            if total_chips.total == 0:
                dealer_score += 1            
                new_bet_state()
                update_stats()                
                game_over()
            else:
                outcome = "DEALER WINS. NEW DEAL?"                    
                game_outcome_update.config(text=outcome)
                dealer_score += 1            
                new_bet_state()
                update_stats()
        else:
            outcome = "PLAYER WINS. NEW DEAL?"
            game_outcome_update.config(text=outcome)            
            player_score += 1            
            new_bet_state()
            total_chips.win_bet()
            player_bank_update.config(text = 'Player bank ${}'.format(total_chips.total))
            update_stats()
    
    export_results()

@calltracker
def game_over():
    """ Destroys all game controls and adds new reset game button """
    global total_chips 
    if total_chips.total == 0:
        outcome = "YOU ARE BROKE! GAME OVER!"
        game_outcome_update.config(text=outcome)
           
        slaves = frame_gameControls.grid_slaves()
        for i in slaves:
            i.destroy()
        reset_button = Button(frame_gameControls, text="New game", command = new_game)
        reset_button.grid(row = 0, column = 1, padx = 10, pady = 10)
    
def helpManual():
    messagebox.showinfo(title="Manual", message="""
                        
    1) First to 21 wins.
    2) Card scoring system is as follows: "TWO":2, "THREE":3, "FOUR":4, "FIVE":5, "SIX":6, "SEVEN":7, "EIGHT":8, "NINE":9, "TEN":10, "JACK":10, "QUEEN":10, "KING":10, "ACE":1
    3) The value of the ACE can change between 1 and 11.
    
    """)

def take_bet():
    """
    This function takes a bet within a predefined integer region.
    """
    global player_score, dealer_score, bet_size, total_chips, round_number, game_outcome_update, submit_button, player_bank_update, round_number_update, entry_bet_size, deal_button
#    total_chips = Chips(2000)
#    print(total_chips.total)
#    global round_number
#    print(total_chips.total)
    USER_PROMPT = True
    while USER_PROMPT:
        try:        
            bet_size = int(entry_bet_size.get())
            if bet_size > 0 and bet_size <= total_chips.total:
                USER_PROMPT = False
                total_chips.bet = bet_size
                game_outcome_update.config(text="Bet size is ${}".format(total_chips.bet))
                deal_button.configure(state=NORMAL)
                entry_bet_size.configure(state=DISABLED)        
                submit_button.configure(state=DISABLED)
                player_bank_update.config(text = 'Player bank ${}'.format(total_chips.lose_bet()))
                round_number +=1            
                round_number_update.config(text = 'Round number {}'.format(round_number))
            else:
                messagebox.showwarning(title="INVALID INPUT", message = "Please enter a number between 0 and {}".format(total_chips.total)) 
                entry_bet_size.delete(0, END)
                USER_PROMPT = False
        except:
            messagebox.showwarning(title="INVALID INPUT", message = "Please enter a number between 0 and {}".format(total_chips.total)) 
            entry_bet_size.delete(0, END)   
            USER_PROMPT = False 

def quit_button(master):
    return root.destroy

if __name__.endswith('__main__'):
    root = Tk()
    root.option_add("*tearOff", False) #disables dashed lines in drop down menus
    root.title("Blackjack v1.0")
    root.geometry("720x480+50+100")
    root.resizable(False, False)
    menubar = Menu(root)
    root.config(menu=menubar)
    file = Menu(menubar)
    help_ = Menu(menubar)
    menubar.add_cascade(menu=file, label="File")
    menubar.add_cascade(menu=help_, label="Help")    
    file.add_command(label = "Export results", command = export_button, state=DISABLED)
    file.add_command(label = "Quit Game", command = quit_button(root))
    help_.add_command(label = "Manual", command = helpManual)    
    new_game()
    root.mainloop()