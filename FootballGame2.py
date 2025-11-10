from functools import lru_cache

def best_score_and_plays(states, transitions, start_state, start_time, score_on="current"):
    """
    Returns (max_score, max_plays_for_that_score, play_sequence).
    score_on: "current" -> reward from current state; "entering" -> reward from next state
    """

    @lru_cache(maxsize=None)
    def dp(s, t):
        cost = states[s]["timeleft"]
        # Not enough time to 'spend' on this state -> no more plays
        if t < cost:
            return (0, 0, [])

        reward_current = states[s]["score"]
        best = (float("-inf"), float("-inf"), [])  # (score, plays, sequence)

        for nxt in transitions[s]:
            rem = t - cost
            if rem < 0:
                continue

            if score_on == "current":
                cand_score = reward_current
            elif score_on == "entering":
                cand_score = states[nxt]["score"]
            else:
                raise ValueError("score_on must be 'current' or 'entering'")

            child_score, child_plays, child_seq = dp(nxt, rem)
            if nxt == "first down" or nxt == "second down" or nxt == "third down" or nxt == "fourth down" or nxt == "extra point" or nxt == "2pt":
                child_plays += 1
            cand = (cand_score + child_score, child_plays, [s] + child_seq)

            # Lexicographic max: prioritize score, then plays
            if cand[:2] > best[:2]:
                best = cand

        if best == (float("-inf"), float("-inf"), []):
            best = (0, 0, [s])  # terminal state

        return best

    return dp(start_state, start_time)


def max_plays_only(states, transitions, start_state, start_time):
    """Returns the maximum number of plays reachable within time."""
    @lru_cache(maxsize=None)
    def dp_plays(s, t):
        cost = states[s]["timeleft"]
        if t < cost:
            return 0
        best = 0
        for nxt in transitions[s]:
            rem = t - cost
            if rem < 0:
                continue
            if nxt == "first down" or nxt == "second down" or nxt == "third down" or nxt == "fourth down" or nxt == "extra point" or nxt == "2pt":
                cand = 1 + dp_plays(nxt, rem)
            else:
                cand = dp_plays(nxt, rem)
            if cand > best:
                best = cand
        return best

    return dp_plays(start_state, start_time)


def main():
    states = {
        "first down":  {"score": 0, "timeleft": 30},
        "second down": {"score": 0, "timeleft": 30},
        "third down":  {"score": 0, "timeleft": 30},
        "fourth down": {"score": 0, "timeleft": 30},
        "touchdown":   {"score": 6, "timeleft": 0},
        "extra point": {"score": 1, "timeleft": 0},
        "2pt":         {"score": 2, "timeleft": 0},
        "field goal":  {"score": 3, "timeleft": 0},
        "defense":     {"score": 0, "timeleft": 0},
        "safety":      {"score": 2, "timeleft": 0}
    }
    transitions = {
        "first down":  ["first down", "second down", "touchdown", "defense"],
        "second down": ["first down", "third down", "touchdown", "defense"],
        "third down":  ["first down", "fourth down", "touchdown", "defense"],
        "fourth down": ["first down", "touchdown", "field goal", "defense"],
        "touchdown":   ["extra point", "2pt"],
        "extra point": ["defense"],
        "2pt":         ["defense"],
        "field goal":  ["defense"],
        "defense":     ["first down", "safety"],
        "safety":      ["first down"]
    }

    start_state = "first down"
    start_time = 1800

    # Also get the play sequence
    best_score, plays_for_best, play_seq = best_score_and_plays(
        states, transitions, start_state, start_time, score_on="current"
    )
    print("Max score:", best_score)
    print("Plays for that score:", plays_for_best)
    print("Play sequence:", " → ".join(play_seq))

    longest = max_plays_only(states, transitions, start_state, start_time)
    print("Absolute max plays (ignore score):", longest)


if __name__ == "__main__":
    main()
