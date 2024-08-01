import itertools
import random
import math
from itertools import permutations, product
import copy
from colorama import Fore, Back, Style, init

#/opt/homebrew/bin/python3.10 CamelUpGame.py

from CamelUpPlayer import CamelUpPlayer

class CamelUpBoard:
    def __init__(self, camel_styles: list[str]):
        self.TRACK_POSITIONS = 16
        self.DICE_VALUES = [1,2,3]
        self.BETTING_TICKET_VALUES = [5, 3, 2, 2]

        self.camel_styles = camel_styles
        self.camel_colors= camel_styles.keys()
        self.track = self.starting_camel_positions()
        self.pyramid = set(self.camel_colors)
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = [] #preserves order

    def starting_camel_positions(self)->list[list[str]]:
        '''Places camels on the board at the beginning of the game
            TODO: randomize these positions

            Return
               list[list[str]] - a 2D list model of the Camel Up race track
        '''
        track = [[] for i in range(self.TRACK_POSITIONS)]
        for color in self.camel_colors:
            # track[0].append(color)
            track[random.randint(0,2)].append(color)
        
        return track
    
    
    def print(self, players: list[CamelUpPlayer]):
        '''Prints the current state of the Camel Up board, including:
            - Race track with current camel positions
            - Betting Tents displaying available betting tickets
            - Dice Tents displaying an ordered collection of rolled dice
            - Player information for both players
                - name
                - coins
                - betting tickets for the current leg of the race
        '''
        board_string = "\n"
         #Ticket Tents
        ticket_string = "Ticket Tents: "
        for ticket_color in self.ticket_tents:
            if len(self.ticket_tents[ticket_color]) > 0:
                next_ticket_value = str(self.ticket_tents[ticket_color][0])
            else:
                next_ticket_value = 'X'
            ticket_string+=self.camel_styles[ticket_color]+next_ticket_value+Style.RESET_ALL+" "
        board_string += ticket_string +"\t\t"

        #Dice Tents
        dice_string = "Dice Tents: "
        for die in self.dice_tents:
            dice_string+=self.camel_styles[die[0]]+str(die[1])+Style.RESET_ALL+" "

        for i in range (5-len(self.dice_tents)):
            dice_string+=Back.WHITE+" "+Style.RESET_ALL+" "
        
        #Camels and Race Track
        board_string += dice_string +"\n"
        for row in range(4, -1, -1):
            row_str = [" "]*16
            for i in range(len(self.track)):
                for camel_place, camel in enumerate(self.track[i]):
                    if camel_place == row:
                        row_str[i]=self.camel_styles[camel]+ camel +  Style.RESET_ALL 
            board_string += "🌴 "+str("   ".join(row_str))+" |🏁\n"
        board_string += "   "+"".join([str(i)+"   " for i in range(1, 10)])
        board_string += "".join([str(i)+"  " for i in range(10, 17)])+"\n"

        #Player Info
        player_string=""
        for player in players:
            player_string+=f"{player.name} has {player.money} coins."
            if len(player.bets)>0:
                bets_string = " ".join([self.camel_styles[bet[0]]+str(bet[1])+Style.RESET_ALL for bet in player.bets])
                player_string += f" Bets: {bets_string}"  
            player_string+="\t\t" 
        
        board_string+=player_string
        print(board_string+"\n")

    def reset_tents(self):
        '''Rests dice tents and ticket tents at the end of a leg
        '''
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = []

    def place_bet(self, color:str)->tuple[str, int]:
        '''Manages the board perspective when a player places a bet:
            - removes the top betting ticket (with highest value) from the appropriate Ticket Tent
            - returns the ticket

            Args
               color (str) - the color of the ticket on which a player would like to bet: 'r'
           
            Return
                tuple(str, int) - a tuple representation of a betting ticket: ('r', 5)
        '''
        tickets_left = self.ticket_tents[color]
        ticket = ()
        if len(tickets_left)>0:
            ticket =(color, tickets_left[0])
            self.ticket_tents[color] = tickets_left[1:]
        return ticket

    def move_camel(self, die:tuple[str, int], verbose=False):
        '''Updates the track according to the die color and value
           The camel of the appropriate color moves the apporpriate number of spaces, 
           along with all camels riding on top of that camel.

           Args
             die (tuple[str, int]) - A tuple representation of the die: ('g', 2)

           Return
             list[list[str]] - a 2D list model of the Camel Up race track
        '''
        if verbose: print("Current track state:", self.track)
        ### BEGIN SOLUTION
        if not die[0]:
            return self.track
        index = [i for i, pair in enumerate(self.track) if die[0] in pair][0]
        self.track[min(15, index+die[1])].extend(self.track[index][self.track[index].index(die[0]):])
        self.track[index] = self.track[index][0:self.track[index].index(die[0])]
        
        ### END SOLUTION
        if verbose: print("Updated track state:", self.track)
        return self.track
    def shake_pyramid(self)->tuple[str, int]:
        '''Manages all the steps (from the board persepctive) involved with shaking the pyramid, 
           which includes:
                - selecting a random color and dice value from the dice colors in the pyramid
                - removing the rolled dice from the pyramid
                - placing the rolled dice in the dice tents

            Return
                tuple[str, int] - A tuple representation of the rolled die
        '''
        rolled_die=("", 0)
        if len(self.pyramid) == 0:
            return rolled_die
        ### BEGIN SOLUTION

        roll = random.randint(1, 3)
        die = random.sample(self.pyramid, 1)[0]
        self.pyramid.remove(die)
        self.dice_tents.append((die, roll))
        return (die, roll)

        ### END SOLUTION

    def is_leg_finished(self)->bool:
        '''Determines whether the leg of a race is finished

           Return
             bool - True if all dice have been rolled, False otherwise
        '''
        ### BEGIN SOLUTION

        if len(self.pyramid) == 0: 
            return True
        return False

        ### END SOLUTION

    def get_rankings(self):
        '''Determines first and second place camels on the track
           
           Returns:
            tuple: a tuple of strings of (1st, 2nd) place camels: ('b', 'y') 
        '''
        rankings = ("", "")
        ### BEGIN SOLUTION
        
        # print(self.track)
        camels = [pos for pos in self.track if pos]
        first = camels[-1][-1]
        global second
        second = 0
        if len(camels[-1]) == 1:
            second = camels[-2][-1]
        else:   
            second = camels[-1][-2]
        rankings = (first, second)  

        ### END SOLUTION
        return rankings

    def get_all_dice_roll_sequences(self)-> set:
        '''
            Constructs a set of all possible roll sequences for the dice currently in the pyramid
            Note: Use itertools product function
        
            Return
               set[tuple[tuple[str, int]]] - A set of tuples representing all the ordered dice seqences 
                                             that could result from shaking all dice from the pyramid
        ''' 
        roll_space = set()
        ### BEGIN SOLUTION
        color_combos = itertools.permutations(self.pyramid)
        dice_combos = product([1,2,3], repeat=len(self.pyramid))
        all_combos = product(color_combos, dice_combos)

        new = []
        for combo in all_combos:
            sub = []
            for i in range(len(combo[0])): 
                sub.append((combo[0][i], combo[1][i]))
            new.append(tuple(sub))
        # print(new)


        roll_space = set(tuple(new))
                
        
        ### END SOLUTION
        return roll_space
    
    def run_enumerative_leg_analysis(self)->dict[str, tuple[float, float]]:
        '''Conducts an enumerative analysis of the probability that each camel will win either 1st or 
           2nd place in this leg of the race. The enumerative analysis counts 1st/2nd place finishes 
           via calculating the entire state space tree

           General Steps:
                1) Precalculate all possible dice sequences for the dice currently in the pyramid
                2) Move through each sequence of possible dice rolls to count the number of 1st/2nd places 
                   finishes for each camel
                3) Calculates the probability that each camel will come in 1st or 2nd based on the total 
                   number of 1st/2nd finishes out of the total number of dice sequences

                TODO: Add notes about using deepcopy to preserve state
           
           Returns: 
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will 
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        win_percents={color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION
        copy_track = copy.deepcopy(self.track)
        allRolls = self.get_all_dice_roll_sequences()
        for roll in allRolls:
            self.track = copy.deepcopy(copy_track)
            for move in roll:
                self.move_camel(move)
            win_percents[self.get_rankings()[0]] = (win_percents[self.get_rankings()[0]][0]+1, win_percents[self.get_rankings()[0]][1])
            win_percents[self.get_rankings()[1]] = (win_percents[self.get_rankings()[1]][0], win_percents[self.get_rankings()[1]][1]+1)
            
        for color in win_percents:
            win_percents[color] = (win_percents[color][0]/len(allRolls), win_percents[color][1]/len(allRolls))
        
        self.track = copy_track

        ### END SOLUTION
        return win_percents

    def run_experimental_leg_analysis(self, trials:int)->dict[str, tuple[float, float]]:
        '''Conducts an experimental analysis (ie. a random simulation) of the probability that each camel
            will win either 1st or 2nd place in this leg of the race. The experimenta analysis counts 
            1st/2nd place finishes bycounting outcomes from randomly shaking the pyramid over a given 
            number of trials.
           
           General Steps:
                1) Shake the pyramid enough times to randomly generate a dice sequence to finish the leg
                2) Count a 1st/2nd place finish for each camel
                3) Repeat steps #1 - #2 trials number of times
                3) Calculate the probability that each camel will come in 1st or 2nd based on the total 
                   number of 1st/2nd finishes out of the total number of trials

                TODO: Add notes about using deepcopy to preserve state

           Args
              trials (int): The number of random simulations to conduct

           Returns: 
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will 
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        win_percents={color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION
        copy_track = copy.deepcopy(self.track)
        copy_pyramid = copy.deepcopy(self.pyramid)
        for i in range(trials):
            self.track = copy.deepcopy(copy_track)
            pyramid = copy.deepcopy(copy_pyramid)
            while len(pyramid) > 0:
                 # roll = self.shake_pyramid()
                 die = random.sample(pyramid, 1)[0]
                 roll = random.randint(1,3)
                 pyramid.remove(die)
                 self.move_camel((die, roll))
            win_percents[self.get_rankings()[0]] = (win_percents[self.get_rankings()[0]][0]+1, win_percents[self.get_rankings()[0]][1])
            win_percents[self.get_rankings()[1]] = (win_percents[self.get_rankings()[1]][0], win_percents[self.get_rankings()[1]][1]+1)
            
            
        for color in win_percents:
            win_percents[color] = (win_percents[color][0]/trials, win_percents[color][1]/trials)
        
        self.track = copy_track
        self.pyramid = copy_pyramid

        ### END SOLUTION
        return win_percents
    
    
        # win_percents={color:(0, 0) for color in self.camel_colors}
        # ### BEGIN SOLUTION
        # dictWins = {color:0 for color in self.camel_colors}
        # dict2Wins = {color:0 for color in self.camel_colors}
        
        # oldTrack = copy.deepcopy(self.track)
        # newPyramid = copy.deepcopy(self.pyramid)
        # for i in range(trials): 
        #     for num in range(len(self.pyramid)):
        #         roll = random.randint(1, 3)
        #         die = newPyramid.pop()
        #         currRoll = (die, roll)
        #         self.move_camel(currRoll)
        #     ranking = self.get_rankings()
        #     dictWins[ranking[0]] += 1
        #     dict2Wins[ranking[1]] += 1
        
        # for color in self.camel_colors:
        #     win_percents[color] = dictWins[color] / trials 

        # ### END SOLUTION
        # self.track = oldTrack
        # return win_percents
   
if __name__ == "__main__":
    camel_styles= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    board = CamelUpBoard(camel_styles)
    p1 = CamelUpPlayer("p1")
    p2 = CamelUpPlayer("p2")
    board.print([p1, p2])
    die = ('b', 1)
    board.move_camel(die)
    # Roll 3 random dice
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    # rolled_die = board.shake_pyramid()
    # board.move_camel(rolled_die)
    board.print([p1, p2])
    #Probabilites
    all_possible_dice_sequences= board.get_all_dice_roll_sequences()
    # print(all_possible_dice_sequences)
    print(f"{len(all_possible_dice_sequences)} possible dice sequences for {len(board.pyramid)} dice in the pyramid:") 
    print("Enumerative Probabilities:", board.run_enumerative_leg_analysis())
    print("Experimental Probabilities:", board.run_experimental_leg_analysis(5000))
    print(board.get_rankings())
