import random
import numpy

class Team:
    score = 0

    def __init__(self, utilities, extreme_cases, name):
        self.utilities = utilities
        self.extreme_cases = extreme_cases
        self.def_strat_profile = [.5, .5]
        self.name = name

    def printUtilities(self, series_down, game, defense):
        print "This is down %d in series. There are %d downs left in the game." % (series_down, game.num_downs - game.overall_down)
        print "%d, %d | %d, %d" % (self.utilities[0][0][0], self.utilities[0][0][1], self.utilities[0][1][0], self.utilities[0][1][1])
        print "%d, %d | %d, %d" % (self.utilities[1][0][0], self.utilities[1][0][1], self.utilities[1][1][0], self.utilities[1][1][1])
        print "Defense's current strategy profile is " + str(defense.def_strat_profile)
        print "Offense has %d yards in series" % series_yardage
        print "Offense has %d yards to endzone" % overall_yardage
        nash = isNash(self)
        if len(nash) != 0:
            nash_str = []
            for nash_index in nash:
                if nash_index == [0, 0]:
                    nash_str.append("Pass-Defend Pass")
                elif nash_index == [0, 1]:
                    nash_str.append("Pass-Defend Run")
                elif nash_index == [1, 0]:
                    nash_str.append("Run-Defend Pass")
                elif nash_index == [1,1]:
                    nash_str.append("Run-Defend Run")
            print "Nash Equilibrium is: " + str(nash_index)
        else:
            print "No Nash Equilibrium"
        print "======================"

class Game:
    overall_down = 1
    team1_score = 0
    team2_score = 0

    def __init__(self, num_downs, endgame):
        self.num_downs = num_downs
        self.endgame = endgame
    
    def isEndgame(self):
        if self.overall_down >= self.num_downs - self.endgame:
            return True
        return False
    
def isNash(offense):
    outcomes_table = offense.utilities
    def_prefs = []
    off_prefs = []
    # Go by each row to see which strategy defense would prefer to do.

    i = 0
    for off_strategy in outcomes_table:
        if off_strategy[0][1] > off_strategy[1][1]:
            def_prefs.append([i, 0])
        elif off_strategy[0][1] < off_strategy[1][1]:
            def_prefs.append([i, 1])
        else:
            def_prefs.append([i, 0])
            def_prefs.append([i, 1])
        i += 1
    
    i = 0
    while i < 2:
        def_strategy = [outcomes_table[0][i], outcomes_table[1][i]]
        if def_strategy[0][0] > def_strategy[1][0]:
            off_prefs.append([0, i])
        elif def_strategy[0][0] < def_strategy[1][0]:
            off_prefs.append([1, i])
        else:
            off_prefs.append([0, i])
            off_prefs.append([1, i])
        i += 1
    
    nash = [value for value in off_prefs if value in def_prefs]
    return nash

def create_utilities(utility_pairs):
    pass_outcomes = [utility_pairs[0], utility_pairs[1]]
    run_outcomes = [utility_pairs[2], utility_pairs[3]]
    return [pass_outcomes, run_outcomes]

current_game = Game(200, 4)

series_down = 1
series_yardage = 10
overall_yardage = 80 #Assume that team starts at own 20-yd line, which is typical.
extreme_cases_utilities = [ [40, -40], [70, -70], [45, -45], [30, -30] ]
universal_extreme_cases = create_utilities(extreme_cases_utilities)

init_utilities = [ [2, -2], [7, -7], [9, -9], [4, -4] ]
# init_utilities = [ [2, -2], [4, -4], [7, -7], [6, -6] ]
init_outcomes = create_utilities(init_utilities)

team1 = Team(init_outcomes, universal_extreme_cases, "Team 1")

init_utilities = [ [3, -3], [12, -12], [14, -14], [7, -7] ]
init_outcomes = create_utilities(init_utilities)
team2 = Team(init_outcomes, universal_extreme_cases, "Team 2")

current_offense = team1
current_defense = team2


def play_strat(offense, defense, strat, nash_present):
    global series_yardage
    global overall_yardage
    global series_down

    successful_play = numpy.random.choice([0, 1], 1, p=[0.25, 0.75])

    # successful_play = bool(random.getrandbits(1))
    if successful_play == 1:
        movement = offense.utilities[strat[0]][strat[1]][0]
        series_yardage -= movement
        overall_yardage -= movement
        print "Ball is moved %d yards" % movement
    else:
        print "Ball fails to move"

    series_down += 1
    if series_yardage <= 0:
        series_down = 1
        series_yardage = 10
    current_game.overall_down += 1

    # Loop thru each offense strategy and either lessen utility if that was the one chosen, or increase otherwise.
    for i in range(0, 2):

        #chosen strategy
        if i == strat[0]:
            offense.utilities[i][0][0] -= 1
            offense.utilities[i][0][1] += 1

            offense.utilities[i][1][0] -= 1
            offense.utilities[i][1][1] += 1
        
        #not-chosen strategy
        else:
            offense.utilities[i][0][0] += 1
            offense.utilities[i][0][1] -= 1

            offense.utilities[i][1][0] += 1
            offense.utilities[i][1][1] -= 1
        
    # Check if shift in strategy is needed:
    nash = isNash(offense)

    #Exiting Nash. Def still leaning towards previously-Nash play, but now considerate of other play.
    if len(nash) == 0 and nash_present:
        # Previous def strat was defend pass
        if strat[1] == 0:
            defense.def_strat_profile = [.75, .25]
        #Previous def strat was defend run
        else:
            defense.def_strat_profile = [.25, .75]
    
    #Was in neutral, still in neutral. Shift strategy profile by 5 percent
    elif len(nash) == 0 and not nash_present:
        if defense.def_strat_profile[0] != 1.0 and defense.def_strat_profile[1] != 1.0:
            if strat[1] == 0:
                defense.def_strat_profile = [round(defense.def_strat_profile[0] + 0.05, 2), round(defense.def_strat_profile[1] - 0.05, 2)]
            else:
                defense.def_strat_profile = [round(defense.def_strat_profile[0] - 0.05, 2), round(defense.def_strat_profile[1] + 0.05, 2)]
        else:

            #Strat chooses defend-run, and profile is 100% defend-run anyways
            if (strat[0] == 0 and defense.def_strat_profile[0] == 1.0) or (strat[0] == 1 and defense.def_strat_profile[1] == 1.0):
                pass
            else:
                if strat[1] == 0:
                    defense.def_strat_profile = [0.05, 0.95]
                else: 
                    defense.def_strat_profile = [0.95, 0.05]

    
    #Entering/Remaining in Nash. Shift strategy fully to Nash play
    else:
        if nash[0][1] == 0:
            defense.def_strat_profile = [1.0, 0.0]
        else:
            defense.def_strat_profile = [0.0, 1.0]

    return
    
def switchPossession():
    global current_offense
    global current_defense
    tmp = current_defense
    current_defense = current_offense
    current_offense = tmp
    print "Teams switched"

# Start with a neutral scenario


while (current_game.overall_down < current_game.num_downs):
    # Understand if Nash present. If so, play that.
    while (series_down < 5):
        if (current_game.overall_down < current_game.num_downs):
            
            current_offense.printUtilities(series_down, current_game, current_defense)
            #Check if there is a Nash value. If there is, play that.
            any_nash = isNash(current_offense)
            if len(any_nash) != 0:
                chosen_strat = any_nash[0]
                print("Outcome is " + str(chosen_strat))
                print("======================")
                play_strat(current_offense, current_defense, chosen_strat, True)

            #No Nash present
            else:
                #Observe which strat defense is leaning towards
                current_strat_prof = current_defense.def_strat_profile
                
                #Leaning towards defend pass
                if current_strat_prof[0] > current_strat_prof[1]:
                    predicted_def_strat = 0
                
                #Leaning towards defend run
                elif current_strat_prof[0] < current_strat_prof[1]:
                    predicted_def_strat = 1
                
                #50/50
                else:
                    predicted_def_strat = -1
                
                #Offense wants to 1) Play less-predicted strat, or 2) Play to make that strat less-predicted for more success.
                #To-do: Must implement defense's chances of selecting into their actual selection. Right now, only hard-coded to play perfectly for offense once threshold is met.

                #If defense has a preference
                if predicted_def_strat != -1:

                    #If more-preferred strat is 60% or more, it is worth for offense to consider diverting.
                    if current_strat_prof[predicted_def_strat] >= .60:
                        off_decision = bool(random.getrandbits(1))
                        #If offense chooses to play against prediction
                        if off_decision:
                            chosen_strat = [1 - predicted_def_strat, predicted_def_strat]
                            def_smaller_strat = [1 - predicted_def_strat, 1 -predicted_def_strat]
                            strat_choices = [chosen_strat, def_smaller_strat]
                            actual_strat = numpy.random.choice( len(strat_choices), p = [current_strat_prof[predicted_def_strat], current_strat_prof[1 - predicted_def_strat]])
                            print("Offense tries to divert")
                            print("Outcome is " + str(strat_choices[actual_strat]))
                            print("======================")
                            play_strat(current_offense, current_defense, strat_choices[actual_strat], False)

                        else:
                            chosen_strat = [predicted_def_strat, predicted_def_strat]
                            def_smaller_strat = [predicted_def_strat, 1 - predicted_def_strat]
                            strat_choices = [chosen_strat, def_smaller_strat]
                            actual_strat = numpy.random.choice( len(strat_choices), p = [current_strat_prof[predicted_def_strat], current_strat_prof[1 - predicted_def_strat]])
                            print("Offense plays it safe")
                            print("Outcome is " + str(strat_choices[actual_strat]))
                            print("======================")
                            play_strat(current_offense, current_defense, strat_choices[actual_strat], False)
                    
                    #Has preference, but not a strong one yet. Work towards running play.
                    else:
                        if current_offense.utilities[0][1][0] > current_offense.utilities[1][0][0]:
                            #Work towards running play, in order to play pass later.
                            chosen_strat = [1, 1]
                            print("Offense is trying to build its reputation")
                            print("Outcome is " + str(chosen_strat))
                            print("======================")
                            play_strat(current_offense, current_defense, chosen_strat, False)
                        elif current_offense.utilities[0][1][0] < current_offense.utilities[1][0][0]:
                            chosen_strat = [0, 0]
                            print("Offense is trying to build its reputation")
                            print("Outcome is " + str(chosen_strat))
                            print("======================")
                            play_strat(current_offense, current_defense, chosen_strat, False)

                #Defense strat is 50/50 so build reputation towards highest utility.
                else:
                    if current_offense.utilities[0][1][0] > current_offense.utilities[1][0][0]:
                        #Work towards running play, in order to play pass later.
                        chosen_strat = [1, 1]
                        print("Offense is trying to build its reputation")
                        print("Outcome is " + str(chosen_strat))
                        print("======================")
                        play_strat(current_offense, current_defense, chosen_strat, False)
                    
                    elif current_offense.utilities[0][1][0] < current_offense.utilities[1][0][0]:
                        chosen_strat = [0, 0]
                        print("Offense is trying to build its reputation")
                        print("Outcome is " + str(chosen_strat))
                        print("======================")
                        play_strat(current_offense, current_defense, chosen_strat, False)
                    
                    else:
                        #A true 50/50.
                        off_decision = bool(random.getrandbits(1))
                        
                        if off_decision:
                            chosen_strat = [0, 0]
                        else:
                            chosen_strat = [1, 1]
                        
                        play_strat(current_offense, current_defense, chosen_strat, False)
            
            if overall_yardage <= 0:
                print "TOUCHDOWN for " + current_offense.name
                current_offense.score += 7
                break

        else:
            break
    #4th down passed.
    series_down = 1
    series_yardage = 10
    overall_yardage = 80
    switchPossession()


series_down = 999
current_offense.printUtilities(series_down, current_game, current_defense)
print "Score: " + str(current_offense.score) + " : " + str(current_defense.score)