# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 16:16:30 2014
1.1: add graph
@author: Jboeye
"""
import os
import csv
os.system("mode con: cols=120 lines=20") #set console width and heigth

import ctypes
import platform
if platform.system() == 'windows':
    ctypes.windll.kernel32.SetConsoleTitleA("Mens, erger je niet.")

try:    #check if visual library is installed
    import pylab as plt
    import random as rnd
except ImportError:
    visuals = False
else:
    visuals = True
    plt.ion()
    

class Player:
    '''Holds the unique properties of each player'''
    def __init__(self):
        self.score = 0
        self.name = None
        self.nickname = None
        self.lastname = None
        self.colour = None
        self.victories = 0 #the number of victories a player has accumulated over games
        
class Game:
    '''The main class, regulates everything'''
    def __init__(self):
        self.reset_game()
        
    def prepare_game(self):
        '''Preparing the game by setting up the 
        number of players and their names'''
        self.clear_screen()
        while True:
            try:
                n_players=int(raw_input('How many players?  \n: '))
                if n_players>1:
                    break
                else:
                    print "Number must be higher than 1.\n"
            except ValueError:
                print "Not a number.\n"
        
        with open('players.csv') as f:
            reader = csv.DictReader(f)
            player_sel_list = []
            for row in reader:
                player_sel = Player()
                player_sel.name = row['name']
                player_sel.lastname = row['lastname']
                player_sel.nickname = row['nickname']
                player_sel_list.append(player_sel)
        
        for p in xrange(n_players):
            new_player = Player()
            while True:
                self.clear_screen()
                print 'select player or create new player'
                for player_sel in player_sel_list:
                    print str(player_sel_list.index(player_sel)) + " " + player_sel.name + " " + player_sel.lastname
                print str(len(player_sel_list)) + " add new player"
                try:
                    name_test = raw_input('\nSelect option: ')
                    print(name_test)
                    name_sel=int(name_test)
                    print name_sel
                    if name_sel>=0 and name_sel < len(player_sel_list):
                        name = player_sel_list[name_sel].name
                        if name not in self.name_list:
                            print(name)
                            self.name_list.append(name)
                            self.clear_screen()
                            break
                        else:
                            print "Name already taken.\n"
                        break
                    elif name_sel == len(player_sel_list):
                        name=str(raw_input('Player %s name?  \n: '%(str(p+1))))
                        if len(name)>0:
                            if name not in self.name_list:
                                self.name_list.append(name)
                                self.clear_screen()
                                break
                            else:
                                print "Name already taken.\n"
                        else:
                            print "Name too short.\n"
                    else:
                        print "option not valid"
                except ValueError:
                    print "Not a number.\n"
            new_player.name = name
            self.players.append(new_player)
        self.reset_score_history()
        
    def reset_score_history(self):
        '''Reset history and give players colours'''
        self.score_history=[[0] for i in xrange(len(self.players))]            
        colour_list = ['red','green','blue','cyan','magenta','yellow','black']
        for index,player in enumerate(self.players): 
            if index<7:
                player.colour = colour_list[index]
            else:
                r = lambda: rnd.randint(0,255) #select a random colour for players past player 7
                for player in self.players:            
                    player.colour = '#%02X%02X%02X' % (r(),r(),r())        
            
    def reset_scores_and_restart(self):
        '''Change the order so that the winner goes first'''
        self.players.sort(key=lambda player: player.score, reverse=True)   
        #Reset scores to zero
        self.reset_score_history()
        for player in self.players:
            player.score = 0
        self.start_game()
            
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
            
    def reset_game(self):
        self.players = []
        self.name_list = []
        self.prepare_game()
        self.start_game()        
    
    def give_advice(self,player):
        '''advice players on what to throw to finish or hit other player'''
        target_list = [] #list of players with a higher score
        special_target_list = [] #list of players with a lower score who you can hit by passing 321
        for competitor in self.players:
            if player.name != competitor.name: 
                if competitor.score > player.score:
                    target_list.append(competitor)
                if (((321-competitor.score)+(321-player.score))<=180) and (321-competitor.score<60):
                    special_target_list.append(competitor)
        print '%s, your current score is %s. \n\nTo finish you need %s points.\n'%(player.name, 
                                                                               str(player.score),
                                                                               str(321 - player.score))
        
        if len(target_list) == 0:
            print 'You are in first place, run for your life.\n'
        else:
            for target in target_list:
                print 'To get %s, score %s points.\n'%(target.name, str(target.score - player.score))
        if len(special_target_list)>0:
            print 'OR\n'
            for target in special_target_list:
                score_to_get = (321-target.score)+(321-player.score)
                print 'To get %s, score %s points.\n'%(target.name, str(score_to_get))
                
    def check_equal_scores(self,player):
        for competitor in self.players:
            if ((competitor.name != player.name)
            and (player.score > 0)
            and (player.score == competitor.score)):
                print "%s, you set %s's score to zero.\n"%(player.name,competitor.name)
                
    def set_competitor_to_zero(self,player):
        for index,competitor in enumerate(self.players):
            if ((competitor.name != player.name)
            and (player.score > 0)
            and (player.score == competitor.score)):
                competitor.score = 0
                self.score_history[index][-1] = 0
            
    def standings(self,round_n,final):
        scores = []
        for player in self.players:
            scores.append(player.score)
        scores = sorted(scores)[::-1]
        position = 1
        positions = []
        sorted_players = []
        for score in scores:
            for player in self.players:
                if player.score == score:
                    sorted_players.append(player)
                    positions.append(position)
            position += 1
            if len(sorted_players) == len(self.players):
                break
        self.clear_screen()
        if final:
            print 'Final standings:'
        else:
            print 'Standings, round = %s:'%(round_n)
        print '#'*16*len(self.players)
        for posit in positions:
            print posit ,'\t'*2,
        print ''
        for player in sorted_players:
            if len(player.name)>2: 
                print player.name,'(%s)'%(player.victories) ,'\t',
            else: #add a tab if the player name is very short
                print player.name,'(%s)'%(player.victories) ,'\t'*2,
        print ''
        for score in scores:
            print score ,'\t'*2,
        print ''
        print '#'*16*len(self.players),'\n'
        #response = None
#        while True:
#            response=str(raw_input('\nPress enter to continue'))
#            if response != None:
#                break
        if final:
            print '\n%s WINS!!!\n'%(sorted_players[0].name)
            sorted_players[0].victories+=1
            
    def draw_graph(self):
        plt.clf()
        plt.xlim(0, 10)
        plt.ylim(0, 321)
        for index,player in enumerate(self.players):
            plt.plot(self.score_history[index],player.colour,label=player.name,linewidth=2.0)
        plt.legend(loc='upper left')
        plt.draw()
        plt.pause(.0001) 
        
    def set_scores_manually(self):
        for index, player in enumerate(self.players):
            self.clear_screen()
            try:
                new_score = int(raw_input("The current score for %s is %s \nAdd new score or press enter \n:"%(player.name,player.score)))
                if new_score > 321:
                    player.score = 321 - (new_score)%321
                else:
                    player.score = (new_score)%321
                self.score_history[index][-1]=player.score
                self.clear_screen()
            except ValueError:
                self.clear_screen()
                    
            
        
    def start_game(self):
        round_n = 1
        winner = Player()
        if visuals:
            self.draw_graph()
        while (winner.name == None) and (round_n<11):
            for index, player in enumerate(self.players):
                self.clear_screen()
                #print 'Current player =', player.name ,"\n"
                while True:
                    try:
                        self.standings(round_n,final=False)
                        self.give_advice(player)
                        old_score = player.score
                        input_given = raw_input("Add score for %s \n:"%(player.name))
                        if str(input_given) == 'x':
                            self.set_scores_manually()
                        else:
                            subscore=int(input_given)
                            print ''
                            if player.score + subscore == 321:
                                player.score += subscore
                                winner = player
                                break
                            else:
                                if player.score + subscore > 321:
                                    player.score = 321 - (player.score + subscore)%321
                                else:
                                    player.score += subscore   
                                self.clear_screen() 
                                self.check_equal_scores(player)  
                            print '%s, your new score = %s\n'%(player.name,str(player.score))
                            end_turn_decision = str(raw_input("To go to next player, press enter. \nTo cancel score addition press 'c'. \nTo manually correct scores press 'x'. \nTo submit other score for same player, press 's'.\n:"))
                            self.clear_screen()                        
                            if end_turn_decision == 'c':
                                player.score = old_score                            
                                print '%s, your score was reset to %s.\n'%(player.name,str(player.score))
                            elif end_turn_decision == 'x': 
                                self.set_competitor_to_zero(player)
                                self.set_scores_manually()
                                if visuals:
                                    self.draw_graph()
                            else:                            
                                self.set_competitor_to_zero(player)
                                if end_turn_decision != 's': #break if no other score is added
                                    self.score_history[index].append(player.score)
                                    if visuals:
                                        self.draw_graph()                                
                                    break
                          

                    except ValueError:
                        self.clear_screen()       
                if winner.name != None:
                    break
            if winner.name == None:
#                if round_n<10:
#                    self.clear_screen()
#                    self.standings(round_n)
                round_n += 1
        self.clear_screen()
        if winner.name == None:
            self.standings(round_n,final=True)
        else:
            self.standings(round_n,final=False)
            winner.victories += 1
            print '%s WINS!!!\n'%(winner.name)
        restart = str(raw_input("To start new game, press 'n'\nTo restart identical (reordered) game, press 'r' \nTo quit, press enter\n: "))
        if restart == 'n':
            self.reset_game()
        elif restart == 'r':
            self.reset_scores_and_restart()
if __name__ == '__main__':                
    GAME = Game()
    print 'Game finished, goodbye.'
