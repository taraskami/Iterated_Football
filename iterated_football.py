class Team:
    self.score = 0

    def __init__(self, utilities, extreme_cases):
        self.utilities = utilities
        self.extreme_cases = extreme_cases

class Game:
    self.overall_down = 0
    
    def __init__(self, num_downs, endgame):
        self.num_downs = num_downs
        self.endgame = endgame
    
    def isEndgame(self):
        if down >= num_downs - endgame:
            return True
        return False
    
def create_utilities(utility_pairs):
    pass_outcomes = [utility_pairs[0], utility_pairs[1]]
    run_outcomes = [utility_pairs[2], utility_pairs[3]]
    return [pass_outcomes, run_outcomes]


# Start with a neutral scenario
extreme_cases_utilities = [ [40, -40], [70, -70], [45, -45], [30, -30] ]
universal_extreme_cases = create_utilities(extreme_cases_utilities)

init_utilities = [ [6, -6], [15, -15], [11, -11], [4, -4] ]
init_outcomes = create_utilities(init_utilities)

team1 = Team(init_outcomes, universal_extreme_cases)

init_utilities = [ [3, -3], [12, -12], [14, -14], [7, -7] ]
init_outcomes = create_utilities(init_utilities)
team2 = Team(init_outcomes, universal_extreme_cases)

current_game = Game(100, 4)

series_down = 1