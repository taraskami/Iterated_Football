class Team:
    score = 0

    def __init__(self, utilities, extreme_cases):
        self.utilities = utilities
        self.extreme_cases = extreme_cases
        self.def_strat_profile = [.5, .5]

    def printUtilities(self, series_down, game):
        print "Down in series is %d. There are %d downs left in the game." % (series_down, game.num_downs - game.overall_down)
        print "%d, %d | %d, %d" % (self.utilities[0][0][0], self.utilities[0][0][1], self.utilities[0][1][0], self.utilities[0][1][1])
        print "%d, %d | %d, %d" % (self.utilities[1][0][0], self.utilities[1][0][1], self.utilities[1][1][0], self.utilities[1][1][1])
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

class Game:
    overall_down = 1
    team1_score = 0
    team2_score = 0

    def __init__(self, num_downs, endgame):
        self.num_downs = num_downs
        self.endgame = endgame
    
    def isEndgame(self):
        if down >= num_downs - endgame:
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

def play_strat(offense, defense, strat, nash_present):
    movement = offense.utilities[strat[0]][strat[1]][0]
    series_yardage -= movement
    overall_yardage -= movement
    series_down += 1
    current_game.overall_down += 1

    # Loop thru each offense strategy and either lessen utility if that was the one chosen, or increase otherwise.
    for i in range[0:1]:

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

    #Exiting Nash. Def still leaning towards previously-Nash play, but not considerate of other option.
    if len(nash) == 0 and nash_present:
        # Previous def strat was defend pass
        if strat[1] == 0:
            defense.def_strat_profile = [.75, .25]
        #Previous def strat was defend run
        else:
            defense.def_strat_profile = [.25, .75]
    
    #Was in neutral, still in neutral. Shift strategy profile by 5 percent
    elif len(nash) == 0 and not nash_present:
        if strat[1] == 0:
            orig_def_strat_profile = defense.def_strat_profile
            defense.def_strat_profile = [orig_def_strat_profile[0] + 0.05, orig_def_strat_profile[1] - 0.05]
        else:
            orig_def_strat_profile = defense.def_strat_profile
            defense.def_strat_profile = [orig_def_strat_profile[0] - 0.05, orig_def_strat_profile[1] + 0.05]
    
    #Entering/Still in Nash. Shift strategy fully to Nash play
    else:
        if nash[0][1] == 0:
            defense.def_strat_profile = [1.0, 0.0]
        else:
            defense.def_strat_profile = [0.0, 1.0]
    
    

# Start with a neutral scenario
extreme_cases_utilities = [ [40, -40], [70, -70], [45, -45], [30, -30] ]
universal_extreme_cases = create_utilities(extreme_cases_utilities)

init_utilities = [ [6, -6], [15, -15], [11, -11], [4, -4] ]
# init_utilities = [ [2, -2], [4, -4], [7, -7], [6, -6] ]
init_outcomes = create_utilities(init_utilities)

team1 = Team(init_outcomes, universal_extreme_cases)

init_utilities = [ [3, -3], [12, -12], [14, -14], [7, -7] ]
init_outcomes = create_utilities(init_utilities)
team2 = Team(init_outcomes, universal_extreme_cases)

current_game = Game(50, 4)

series_down = 1
series_yardage = 10
overall_yardage = 80 #Assume that team starts at own 20-yd line, which is typical.

current_offense = team1
current_defense = team2

current_offense.printUtilities(series_down, current_game)

# while (current_game.overall_down <= current_game.num_downs):
current_offense.printUtilities(series_down, current_game)
# Understand if Nash present. If so, play that.
# while (series_down < 4):
any_nash = isNash(current_offense)
if len(any_nash) != 0:
    chosen_strat = any_nash[0]
    # offense, defense, strat, nash_present
    play_strat(current_offense, current_defense, chosen_strat, True)
    series_down += 1
    current_game.overall_down += 1

#No Nash present
else:
    #Observe which strat defense is leaning towards

    #Leaning towards defend pass
    current_strat_prof = current_defense.def_strat_profile
    if current_strat_prof[0] > current_strat_prof[1]:
        predicted_def_strat = 0
    
    #Leaning towards defend run
    elif current_defense.def_strat_profile[0] < current_defense.def_strat_profile[1]:
        predicted_def_strat = 1
    
    #50/50
    else:
        predicted_def_strat = -1
    
    #Offense wants to 1) Play less-predicted strat, or 2) Play to make that strat less-predicted for more success.
    if predicted_def_strat != -1:
        #If less-preferred strat is 35% or more, it is worth playing.
        if current_strat_prof[predicted_def_strat] >= .60:
            off_decision = bool(random.getrandbits(1))

            #If offense chooses to play against prediction
            if off_decision:
                chosen_strat = [1 - predicted_def_strat, predicted_def_strat]
                play_strat(current_offense, current_defense, chosen_strat, False)
                series_down += 1
                current_game.overall_down += 1
    else:
        