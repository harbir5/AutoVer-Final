from functools import lru_cache
from collections import deque
from typing import Dict, List, Tuple, Set, Deque, Literal

States = Dict[str, Dict[str, int]]
Transitions = Dict[str, List[str]]
ScoreOn = Literal["current", "entering"]

def best_score_and_plays(states: States, transitions: Transitions, start_state: str, start_time: int, score_on: ScoreOn = "current",) -> Tuple[float, float, List[str]]:
    """
    Returns (max_score, max_plays_for_that_score, play_sequence).
    score_on: "current" -> reward from current state; "entering" -> reward from next state
    """

    @lru_cache(maxsize=None)
    def dp(s: str, t: int) -> Tuple[float, float, List[str]]:
        cost = states[s]["timeleft"]
        # Not enough time to 'spend' on this state -> no more plays
        if t < cost:
            return (0, 0, [])

        reward_current = states[s]["score"]
        best: tuple[float, float, List[str]] = (float("-inf"), float("-inf"), [])  # (score, plays, sequence)

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


def max_plays_only(states: States, transitions: Transitions, start_state: str, start_time: int) -> int:
    """Returns the maximum number of plays reachable within time."""
    @lru_cache(maxsize=None)
    def dp_plays(s: str, t: int) -> int:
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

def check_reachability(transitions: Transitions, initial_state: str, target_state: str) -> bool:
    """ Check reachability of a given state """
    visited = set()
    stack = [initial_state]
    while stack:
        state = stack.pop()
        if state == target_state:
            return True
        if state not in visited:
            visited.add(state)
            stack.extend(transitions.get(state, []))
    return False


def find_zero_score_path(states: States, transitions: Transitions, start_state: str, start_time:int, score_on: ScoreOn = "current") -> Tuple[bool, List[str]]:
    """
    Returns (is_possible, path) where:
      - is_possible: True if there exists a complete play sequence whose final score is 0
      - path: one such sequence of states (if is_possible is True), otherwise []

    It respects the same timing model as best_score_and_plays:
      - At each step, you 'spend' states[s]["timeleft"] time.
      - If you don't have enough time to spend on a state, the game ends before that state.
    """

    # Each queue entry: (state, time_remaining, score_so_far, path_so_far)
    q: Deque[tuple[str, int, int, List[str]]] = deque()
    q.append((start_state, start_time, 0, []))

    # To avoid revisiting the exact same (state, time, score) triple over and over
    visited = set()
    visited.add((start_state, start_time, 0))

    while q:
        s, t, score_so_far, path = q.popleft()
        cost = states[s]["timeleft"]

        # If we don't have enough time to 'play' this state, game ends before s
        if t < cost:
            # This is a terminal game; check if we ended with score 0
            if score_so_far == 0:
                return True, path  # path already represents the actual sequence played
            continue

        # We can play state s, update score according to the chosen scoring convention
        if score_on == "current":
            new_score = score_so_far + states[s]["score"]
        else:  # score_on == "entering"
            new_score = score_so_far

        new_t = t - cost
        new_path = path + [s]

        # If s has no outgoing transitions, the game ends here.
        if not transitions.get(s):
            if new_score == 0:
                return True, new_path
            continue

        # Otherwise, continue to successor states
        for nxt in transitions[s]:
            if score_on == "entering":
                next_score = new_score + states[nxt]["score"]
            else:
                next_score = new_score

            key = (nxt, new_t, next_score)
            if key in visited:
                continue
            visited.add(key)
            q.append((nxt, new_t, next_score, new_path))

    # If we exhaust the queue, no 0-score game is possible under this model
    return False, []

def zero_score_possible(states: States, transitions: Transitions, start_state: str, start_time: int) -> bool:
    """
    Returns True iff there exists a run starting at (start_state, start_time)
    that never visits a scoring state (score > 0) and can 'finish the game'
    (i.e., time runs out).

    Because all scores are >= 0 in this model, such a run implies final score = 0.
    """

    # Only states with score == 0 are allowed
    zero_states = {s for s, info in states.items() if info["score"] == 0}

    # If the start state itself scores, we’re done: 0 is impossible
    if start_state not in zero_states:
        return False

    # BFS over (state, time_left)
    q: Deque[tuple[str, int]] = deque()
    visited = set()          # to prevent infinite loops (state, time_left)
    q.append((start_state, start_time))
    visited.add((start_state, start_time))

    while q:
        s, t = q.popleft()
        cost = states[s]["timeleft"]

        # If we don't have enough time to 'spend' on this state,
        # the game effectively ends before playing it.
        # Invariant: we have only visited score==0 states so far.
        if t < cost:
            return True  # 0-score game is possible

        rem = t - cost

        # Explore successors but ONLY those that keep score == 0
        for nxt in transitions.get(s, []):
            if nxt not in zero_states:
                # This successor would score, so skip it in the 0-score search
                continue

            key = (nxt, rem)
            if key in visited:
                continue
            visited.add(key)
            q.append((nxt, rem))

    # Explored all zero-score-only runs and never managed to let time expire
    # without being forced into a scoring state.
    return False

def run_avoiding_state(states: States, transitions: Transitions, start_state: str, start_time: int, forbidden_state: str)-> Tuple[bool, List[str]]:
    """
    Returns (is_possible, path) where:
      - is_possible: True iff there exists a run that:
          * starts in start_state with start_time,
          * at each step pays states[s]["timeleft"],
          * never visits forbidden_state,
          * and ends with exactly 0 time remaining.
      - path: one such sequence of states (the states actually played), else [].
    """

    forbidden = {forbidden_state}

    # If the start state itself is forbidden, we can't avoid it.
    if start_state in forbidden:
        return False, []

    # Trivial case: no time at all; consider this a valid empty run if you want
    if start_time == 0:
        return True, []

    # Queue entries: (current_state, time_left, path_so_far)
    q: Deque[tuple[str, int, List[str]]] = deque()
    q.append((start_state, start_time, []))

    # Avoid revisiting same (state, time_left) pair
    visited = set()
    visited.add((start_state, start_time))

    while q:
        s, t, path = q.popleft()

        # If we ever *reach* the forbidden state, discard this branch
        if s in forbidden:
            continue

        cost = states[s]["timeleft"]
        if t < cost:
            # Can't afford to play this state, so this path doesn't give a valid run
            continue

        rem = t - cost
        new_path = path + [s]

        # If we've exactly used up all time, we found a good run
        if rem == 0:
            return True, new_path

        # Otherwise, keep exploring successors
        for nxt in transitions.get(s, []):
            if nxt in forbidden:
                continue  # don't even consider enqueuing the forbidden state

            key = (nxt, rem)
            if key in visited:
                continue
            visited.add(key)
            q.append((nxt, rem, new_path))

    # Explored all runs that avoid forbidden_state and never got rem == 0
    return False, []


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

    print("################################################")
    # Also get the play sequence
    best_score, plays_for_best, play_seq = best_score_and_plays(
        states, transitions, start_state, start_time, score_on="current"
    )
    print("Max score:", best_score)
    print("Plays for that score:", plays_for_best)
    print("Play sequence:", " → ".join(play_seq))

    print("################################################")
    longest = max_plays_only(states, transitions, start_state, start_time)
    print("Absolute max plays (ignore score):", longest)

    print("################################################")
    reachable = check_reachability(transitions, start_state, "first down") and check_reachability(transitions, start_state, "second down") and check_reachability(transitions, start_state, "third down") and check_reachability(transitions, start_state, "fourth down") and check_reachability(transitions, start_state, "touchdown") and check_reachability(transitions, start_state, "extra point") and check_reachability(transitions, start_state, "2pt") and check_reachability(transitions, start_state, "field goal") and check_reachability(transitions, start_state, "defense") and check_reachability(transitions, start_state, "safety")
    print("Reachability of all states:", reachable)

    print("################################################")
    possible, zero_path = find_zero_score_path(
        states, transitions, start_state, start_time, score_on="current"
    )
    if possible:
        print("A 0 score IS possible.")
        print("One such sequence of states:")
        print(" → ".join(zero_path))
    else:
        print("No 0-score outcome is possible in this model.")

    print("################################################")
    if zero_score_possible(states, transitions, start_state, start_time):
        print("A 0-score outcome is possible (by avoiding all scoring states).")
    else:
        print("A 0-score outcome is NOT possible in this model.")

    print("################################################")
    avoid_state = "fourth down"
    possible, path = run_avoiding_state(
        states, transitions, start_state, start_time, avoid_state
    )
    if possible:
        print(f"There IS a run that avoids '{avoid_state}' and ends at time 0.")
        print("One such run:")
        print(" → ".join(path))
    else:
        print(f"No run exists that avoids '{avoid_state}' and ends at time 0.")


if __name__ == "__main__":
    main()
