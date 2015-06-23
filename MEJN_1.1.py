# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 16:16:30 2014
1.1: add graph
@author: Jboeye
"""
import os
import ctypes

ctypes.windll.kernel32.SetConsoleTitleA("Mens, erger je niet.")

class Player:
    def __init__(self):
        self.score = 0
        self.name = None
        
class Game:
    def __init__(self):
        self.reset_game()
        
    def prepare_game(self):
        self.clear_screen()
        self.history = {}
        while True:
            try:
                n_players=int(raw_input('How many players?  \n: '))
                if n_players>1:
                    break
                else:
                    print "Number must be higher than 1.\n"
            except ValueError:
                print "Not a number.\n"
                
        for p in xrange(n_players):
            new_player = Player()
            self.clear_screen()
            while True:
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
            new_player.name = name
            self.players.append(new_player)
            self.history[name] = [[],[]]
            
    def reset_scores_and_restart(self):
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
        target_list = []
        special_target_list = []
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
        for competitor in self.players:
            if ((competitor.name != player.name)
            and (player.score > 0)
            and (player.score == competitor.score)):
                competitor.score = 0
            
    def standings(self,round_n):
        scores = []
        for player in self.players:
            scores.append(player.score)
        scores = sorted(scores)[::-1]
        position = 1
        positions = []
        scored_players = 0
        sorted_players = []
        for score in scores:
            for player in self.players:
                if player.score == score:
                    sorted_players.append(player.name)
                    positions.append(position)
                    scored_players += 1
            position += 1
            if len(sorted_players) == len(self.players):
                break
        self.clear_screen()
        print 'Standings, round = %s:'%(round_n)
        print '#'*42
        for posit in positions:
            print posit ,'\t',
        print ''
        for name in sorted_players:
            print name ,'\t',
        print ''
        for score in scores:
            print score ,'\t',
        print ''
        print '#'*42,'\n'
        #response = None
#        while True:
#            response=str(raw_input('\nPress enter to continue'))
#            if response != None:
#                break

     
        
        
    def final_standings(self):
        scores = []
        for player in self.players:
            scores.append(player.score)
        scores = sorted(scores)[::-1]
        position = 1
        positions = []
        scored_players = 0
        sorted_players = []
        for score in scores:
            for player in self.players:
                if player.score == score:
                    sorted_players.append(player.name)
                    positions.append(position)
                    scored_players += 1
            position += 1
            if len(sorted_players) == len(self.players):
                break
        self.clear_screen()
        print 'Final standings:'
        print '#'*42
        for posit in positions:
            print posit ,'\t',
        print ''
        for name in sorted_players:
            print name ,'\t',
        print ''
        for score in scores:
            print score ,'\t',
        print ''   
        print '#'*42,'\n'
        
        print '\n%s WINS!!!\n'%(sorted_players[0])

    
    def start_game(self):
        round_n = 1
        winner = None
        while (winner == None) and (round_n<11):
            for player in self.players:
                self.clear_screen()
                #print 'Current player =', player.name ,"\n"
                while True:
                    try:
                        self.standings(round_n)
                        self.give_advice(player)
                        old_score = player.score
                        subscore=int(raw_input('Add score for %s  \n:'%(player.name)))
                        print ''
                        if player.score + subscore == 321:
                            player.score += subscore
                            winner = player.name
                            break
                        else:
                            if player.score + subscore > 321:
                                player.score = 321 - (player.score + subscore)%321
                            else:
                                player.score += subscore   
                            self.clear_screen() 
                            self.check_equal_scores(player)                            
                        print '%s, your new score = %s\n'%(player.name,str(player.score))
                        end_turn_decision = str(raw_input("To go to next player, press enter.  \nTo cancel score addition press 'c'. \nTo submit other score for same player, press 's'.\n:"))
                        self.clear_screen()                        
                        if end_turn_decision == 'c':
                            player.score = old_score                            
                            print '%s, your score was reset to %s.\n'%(player.name,str(player.score))
                        elif end_turn_decision == 's':
                            self.set_competitor_to_zero(player)
                        else:
                            self.set_competitor_to_zero(player)
                            break

                    except ValueError:
                        self.clear_screen()       
                if winner != None:
                    break
            if winner == None:
#                if round_n<10:
#                    self.clear_screen()
#                    self.standings(round_n)
                round_n += 1
        self.clear_screen()
        if winner == None:
            self.final_standings()
        else:
            self.standings(round_n)
            print '%s WINS!!!\n'%(winner)
        restart = str(raw_input("To start new game, press 'n'\nTo restart identical game, press 'r' \nTo quit, press enter\n: "))
        if restart == 'n':
            self.reset_game()
        elif restart == 'r':
            self.reset_scores_and_restart()
if __name__ == '__main__':                
    GAME = Game()
    print 'Game finished, goodbye.'