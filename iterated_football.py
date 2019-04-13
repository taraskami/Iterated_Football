class Team:
    score = 0

    def __init__(self, utilities, extreme_cases):
        self.utilities = utilities
        self.extreme_cases = extreme_cases

    def printUtilities(self, series_down, game):
        print "Down in series is %d. There are %d downs left in the game." % (series_down, game.num_downs - game.overall_down)
        print "%d, %d | %d, %d" % (self.utilities[0][0][0], self.utilities[0][0][1], self.utilities[0][1][0], self.utilities[0][1][1])
        print "%d, %d | %d, %d" % (self.utilities[1][0][0], self.utilities[1][0][1], self.utilities[1][1][0], self.utilities[1][1][1])
        print "Nash Equilibrium is: %s" % isNash(self)

class Game:
    overall_down = 1
    
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
        
        return str(nash_str)
    else:
        return "None"



    
def create_utilities(utility_pairs):
    pass_outcomes = [utility_pairs[0], utility_pairs[1]]
    run_outcomes = [utility_pairs[2], utility_pairs[3]]
    return [pass_outcomes, run_outcomes]


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

current_game = Game(100, 4)

series_down = 1
current_offense = team1

# while (current_game.overall_down <= current_game.num_downs):
current_offense.printUtilities(series_down, current_game)
