# First Attempt: modeled after python handout given in class
# Tried to explore very possible state
# DON'T RUN - Can crash computer

'''
class FootballGame:
    def __init__(self, states, transitions, initial_state):
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state

    def simulate_games(self):
        stack = [self.initial_state]
        final_states = []
        while stack:
            cur_state = stack.pop()
            for key, value in cur_state.items():
                trans = self.transitions.get(key)
                for tran in trans:
                    new_state = {tran: {"score": cur_state[key]["score"] + self.states[key]["score"],
                                        "timeleft": cur_state[key]["timeleft"] - self.states[key]["timeleft"]}}
                    if new_state[tran]["timeleft"] > 0:
                        stack.append(new_state)
                    else:
                        final_states.append(new_state)
        print(len(final_states))
        scores = [list(d.values())[0]['score'] for d in final_states]
        print(max(scores))
        return final_states

def main():
    states = {"first down": {"score": 0, "timeleft": 25}, "second down": {"score": 0, "timeleft": 25}, "third down": {"score": 0, "timeleft": 25}, "fourth down": {"score": 0, "timeleft": 25}, "touchdown": {"score": 7, "timeleft": 0}, "field goal": {"score": 3, "timeleft": 0}, "defense": {"score": 0, "timeleft": 160}}
    transitions = {"first down": ["first down", "second down", "touchdown", "defense"], "second down": ["first down", "third down", "touchdown", "defense"], "third down": ["first down", "fourth down", "touchdown", "defense"], "fourth down": ["first down", "touchdown", "field goal", "defense"], "touchdown": ["defense"], "field goal": ["defense"], "defense": ["first down"]}
    initial_state = {"first down": {"score": 0, "timeleft": 1800}}

    game = FootballGame(states, transitions, initial_state)
    game.simulate_games()


if __name__ == "__main__":
    main()
'''