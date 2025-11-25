from functools import lru_cache
from collections import deque
from typing import Dict, List, Tuple, Set, Deque, Literal

States = Dict[str, Dict[str, int]]
Transitions = Dict[str, List[str]]
ScoreOn = Literal["current", "entering"]

def next_yardline(current_yard: int, from_state: str, to_state: str) -> int | None:
    """
    Compute the new yard line when transitioning from `from_state` to `to_state`.

    Rules:
      - Start of a new drive: when we go from 'defense' or 'safety' to 'first down',
        the yard line is reset to 30.
      - Gaining a new first down on offense: any transition to 'first down'
        from a non-defense/non-safety offensive state reduces the yard line by 10.
        If the yard line is already <= 10, another first down is NOT allowed.
      - All other transitions leave the yard line unchanged.

    Args:
        current_yard: current yard line (e.g. 30, 20, 10, ...).
        from_state:   current state name.
        to_state:     successor state name.

    Returns:
        New yard line as an int, or None if this transition is illegal because
        we are too close to the goal to gain another first down.
    """
    # New drive after defense or safety: reset to 30
    if from_state in ("defense", "safety") and to_state == "first down":
        return 70

    # Offensive gain of a fresh first down
    if to_state == "first down" and from_state not in ("defense", "safety"):
        if current_yard <= 10:
            # Can't get another first down when already at or inside the 10
            return None
        return current_yard - 10

    # All other transitions keep the same yard line
    return current_yard


def best_score_and_plays(states: States, transitions: Transitions, start_state: str, start_time: int, score_on: ScoreOn = "current", start_yardline: int = 70) -> Tuple[float, float, List[str]]:
    """
    Returns (max_score, max_plays_for_that_score, play_sequence).
    score_on: "current" -> reward from current state; "entering" -> reward from next state
    """

    @lru_cache(maxsize=None)
    def dp(s: str, t: int, y: int) -> Tuple[float, float, List[str]]:
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

            # Compute new yard line; if None, this transition is illegal.
            new_y = next_yardline(y, s, nxt)
            if new_y is None:
                continue

            if score_on == "current":
                cand_score = reward_current
            elif score_on == "entering":
                cand_score = states[nxt]["score"]
            else:
                raise ValueError("score_on must be 'current' or 'entering'")

            child_score, child_plays, child_seq = dp(nxt, rem, new_y)
            if nxt == "first down" or nxt == "second down" or nxt == "third down" or nxt == "fourth down" or nxt == "extra point" or nxt == "2pt":
                child_plays += 1
            cand = (cand_score + child_score, child_plays, [s] + child_seq)

            # Lexicographic max: prioritize score, then plays
            if cand[:2] > best[:2]:
                best = cand

        if best == (float("-inf"), float("-inf"), []):
            best = (0, 0, [s])  # terminal state

        return best

    return dp(start_state, start_time, start_yardline)


def max_plays_only(states: States, transitions: Transitions, start_state: str, start_time: int, start_yardline: int = 70) -> int:
    """Returns the maximum number of plays reachable within time."""
    @lru_cache(maxsize=None)
    def dp_plays(s: str, t: int, y: int) -> int:
        cost = states[s]["timeleft"]
        if t < cost:
            return 0
        best = 0
        for nxt in transitions[s]:
            rem = t - cost
            if rem < 0:
                continue
            new_y = next_yardline(y, s, nxt)
            if new_y is None:
                # Illegal transition (too close to goal for another first down)
                continue
            if nxt == "first down" or nxt == "second down" or nxt == "third down" or nxt == "fourth down" or nxt == "extra point" or nxt == "2pt":
                cand = 1 + dp_plays(nxt, rem, new_y)
            else:
                cand = dp_plays(nxt, rem, new_y)
            if cand > best:
                best = cand
        return best

    return dp_plays(start_state, start_time, start_yardline)

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


def find_zero_score_path(states: States, transitions: Transitions, start_state: str, start_time:int, score_on: ScoreOn = "current", start_yardline: int = 70) -> Tuple[bool, List[str]]:
    """
    Returns (is_possible, path) where:
      - is_possible: True if there exists a complete play sequence whose final score is 0
      - path: one such sequence of states (if is_possible is True), otherwise []

    It respects the same timing model as best_score_and_plays:
      - At each step, you 'spend' states[s]["timeleft"] time.
      - If you don't have enough time to spend on a state, the game ends before that state.
    """

    # Each queue entry: (state, time_remaining, score_so_far, path_so_far)
    q: Deque[tuple[str, int, int, List[str], int]] = deque()
    q.append((start_state, start_time, 0, [], start_yardline))

    # To avoid revisiting the exact same (state, time, score) triple over and over
    visited = set()
    visited.add((start_state, start_time, 0, start_yardline))

    while q:
        s, t, score_so_far, path, y = q.popleft()
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
            new_y = next_yardline(y, s, nxt)
            if new_y is None:
                # Illegal transition (e.g., trying to get another first down inside the 10).
                continue
            if score_on == "entering":
                next_score = new_score + states[nxt]["score"]
            else:
                next_score = new_score

            key = (nxt, new_t, next_score, new_y)
            if key in visited:
                continue
            visited.add(key)
            q.append((nxt, new_t, next_score, new_path, new_y))

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

def run_avoiding_state(states: States, transitions: Transitions, start_state: str, start_time: int, forbidden_state: str, start_yardline: int = 70)-> Tuple[bool, List[str]]:
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
    q: Deque[tuple[str, int, List[str], int]] = deque()
    q.append((start_state, start_time, [], start_yardline))

    # Avoid revisiting same (state, time_left) pair
    visited = set()
    visited.add((start_state, start_time, start_yardline))

    while q:
        s, t, path, y = q.popleft()

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
            new_y = next_yardline(y, s, nxt)
            if new_y is None:
                # Illegal transition (yardline constraint).
                continue
            key = (nxt, rem, new_y)
            if key in visited:
                continue
            visited.add(key)
            q.append((nxt, rem, new_path, new_y))

    # Explored all runs that avoid forbidden_state and never got rem == 0
    return False, []

def has_positive_score_zero_time_cycle(states: States, transitions: Transitions) -> bool:
    """
        Detect whether the model contains any cycle that:
          - only visits states with timeleft == 0, and
          - has positive total score over the cycle.

        Such a cycle would imply that the offense can accumulate unbounded points
        without consuming any additional time, which is usually a modeling bug.

        Returns:
            True  if at least one positive-score, zero-time cycle exists.
            False otherwise.

        Side effect:
            If a positive cycle is found, prints the cycle and its total score.
        """
    zero_time_states = {s for s, info in states.items() if info["timeleft"] == 0}

    # DFS with path tracking and cumulative score
    visited: Set[str] = set()
    stack: Set[str] = set()

    def dfs(s: str, score_acc: int, path: List[str]) -> bool:
        visited.add(s)
        stack.add(s)
        path.append(s)

        for nxt in transitions.get(s, []):
            if nxt not in zero_time_states:
                continue
            new_score = score_acc + states[nxt]["score"]

            if nxt in stack:
                # Found a cycle: estimate score in this cycle by looking from first occurrence of nxt
                idx = path.index(nxt)
                cycle_states = path[idx:] + [nxt]
                cycle_score = sum(states[u]["score"] for u in cycle_states)
                if cycle_score > 0:
                    print("Positive-score zero-time cycle:", " -> ".join(cycle_states), "score:", cycle_score)
                    return True
            elif nxt not in visited:
                if dfs(nxt, new_score, path):
                    return True

        stack.remove(s)
        path.pop()
        return False

    for s in zero_time_states:
        if s not in visited:
            if dfs(s, states[s]["score"], []):
                return True

    return False

def check_monotone_in_time(states: States, transitions: Transitions, start_state: str,
                           max_time: int, score_on: ScoreOn = "current") -> bool:
    """
        Empirically check a monotonicity property of the model:

            As available time increases, the optimal achievable score starting
            from `start_state` should never strictly decrease.

        Returns:
            True  if all sampled times respect monotonicity (no decrease in score).
            False if any later time yields a strictly lower best score than an earlier time.
        """
    ok = True
    prev_score = None
    for t in range(0, max_time + 1, 30):  # step by 30 seconds, or smaller if you like
        score, plays, _ = best_score_and_plays(states, transitions, start_state, t, score_on)
        if prev_score is not None and score < prev_score:
            ok = False
        prev_score = score
    return ok

def find_exact_score_path(
    states: States,
    transitions: Transitions,
    start_state: str,
    start_time: int,
    target_score: int,
    score_on: ScoreOn = "current",
    start_yardline: int = 70,
) -> Tuple[bool, List[str]]:
    """
    Returns (is_possible, path) where:
      - is_possible: True if there exists a complete play sequence whose final
        score is exactly `target_score` within the given time budget.
      - path: one such sequence of states (if is_possible is True), otherwise [].

    Timing model (same as best_score_and_plays and find_zero_score_path):
      - Each time you 'play' a state s, you spend states[s]["timeleft"] time.
      - If you don't have enough time to spend on a state, the game ends
        before that state is played.
    """

    # Each queue entry: (state, time_remaining, score_so_far, path_so_far)
    q: Deque[tuple[str, int, int, List[str], int]] = deque()
    q.append((start_state, start_time, 0, [], start_yardline))

    # To avoid revisiting the exact same (state, time, score) triple
    visited = set()
    visited.add((start_state, start_time, 0, start_yardline))

    while q:
        s, t, score_so_far, path, y = q.popleft()
        cost = states[s]["timeleft"]

        # If we don't have enough time to 'play' this state, game ends before s
        if t < cost:
            # Terminal game; check if we ended with the desired score
            if score_so_far == target_score:
                return True, path  # path represents the sequence actually played
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
            if new_score == target_score:
                return True, new_path
            continue

        # Otherwise, continue to successor states
        for nxt in transitions[s]:
            new_y = next_yardline(y, s, nxt)
            if new_y is None:
                continue

            if score_on == "entering":
                next_score = new_score + states[nxt]["score"]
            else:
                next_score = new_score

            key = (nxt, new_t, next_score, new_y)
            if key in visited:
                continue
            visited.add(key)
            q.append((nxt, new_t, next_score, new_path, new_y))

    # Exhausted all possibilities; no path achieves exactly target_score
    return False, []

def find_terminal_states(states: States, transitions: Transitions) -> Set[str]:
    """ Terminal states are those with no outgoing transitions. """
    terminals: Set[str] = set()
    for s in states.keys():
        if not transitions.get(s):
            terminals.add(s)
    return terminals


def can_finish_from_state(
    states: States,
    transitions: Transitions,
    start_state: str,
    start_time: int,
    terminal_states: Set[str] | None = None,
    start_yardline: int = 30,
) -> bool:
    """
    Returns True iff there exists some run starting from (start_state, start_time)
    that can 'finish the game', where finishing means:

      - we reach a state with time_left == 0, OR
      - we reach one of the given terminal_states (e.g., touchdown, etc.)

    BFS over (state, time_left) pairs, using the same time model as the rest
    of the file: to 'play' a state s you must pay states[s]["timeleft"] time.
    """

    if terminal_states is None:
        terminal_states = find_terminal_states(states, transitions)

    # Each queue entry: (state, time_remaining)
    q: Deque[tuple[str, int, int]] = deque()
    visited: Set[tuple[str, int, int]] = set()

    q.append((start_state, start_time, start_yardline))
    visited.add((start_state, start_time, start_yardline))

    while q:
        s, t, y = q.popleft()

        # Reaching time 0 or a terminal state counts as a successful finish
        if t == 0 or s in terminal_states:
            return True

        cost = states[s]["timeleft"]

        # Not enough time to 'play' s again and s is not terminal:
        # this is a stuck partial game, so we do not expand further.
        if cost > t:
            continue

        new_t = t - cost
        for nxt in transitions.get(s, []):
            new_y = next_yardline(y, s, nxt)
            if new_y is None:
                continue
            state_time = (nxt, new_t, new_y)
            if state_time not in visited:
                visited.add(state_time)
                q.append(state_time)

    # We exhausted all possibilities without ever hitting time 0 or a terminal state.
    return False


def find_bad_dead_end_states(
    states: States,
    transitions: Transitions,
    representative_time: int,
) -> Set[str]:
    """
    For each state s, check whether there exists ANY run starting from (s, representative_time)
    that can finish the game (time=0 or terminal state).

    If not, s is considered a 'bad dead-end' for that time budget.
    """
    terminal_states = find_terminal_states(states, transitions)
    bad: Set[str] = set()

    for s in states.keys():
        if not can_finish_from_state(states, transitions, s, representative_time, terminal_states):
            bad.add(s)

    return bad



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
        "defense":     {"score": 0, "timeleft": 180},
        "safety":      {"score": 2, "timeleft": 0}
    }
    transitions = {
        "first down":  ["first down", "second down", "touchdown", "defense"],
        "second down": ["first down", "third down", "touchdown", "defense"],
        "third down":  ["first down", "fourth down", "touchdown", "defense"],
        "fourth down": ["first down", "touchdown", "field goal", "defense"],
        "touchdown":   ["extra point", "2pt", "defense"],
        "extra point": ["defense"],
        "2pt":         ["defense"],
        "field goal":  ["defense"],
        "defense":     ["first down", "safety", "touchdown"],
        "safety":      ["first down"]
    }

    start_state = "first down"
    start_time = 3600

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

    print("################################################")
    has_cycle = has_positive_score_zero_time_cycle(states, transitions)
    if has_cycle:
        print("No cycle of zero-time states that yields positive net points which would mean infinite score in zero time.")
    else:
        print("No zero-time/+ score cycle")

    print("################################################")

    time_worse = check_monotone_in_time(states, transitions, start_state, start_time)
    if time_worse:
        print("More time doesn't decrease score")
    else:
        print("Uh-oh - more time could decrease score")

    print("################################################")
    target = 2
    possible, path = find_exact_score_path(states, transitions, start_state, start_time, target)
    if possible:
        print(f"Exactly {target} points IS reachable.")
        print("One such sequence:")
        print(" → ".join(path))
    else:
        print(f"Exactly {target} points is NOT reachable in this model.")

    print("################################################")
    bad_dead_ends = find_bad_dead_end_states(states, transitions, start_time)
    if bad_dead_ends:
        print("States that behave as BAD dead-ends (cannot finish the game from them):")
        for s in sorted(bad_dead_ends):
            print(f"  - {s}")
    else:
        print("No bad dead-end states: from every state we can finish the game.")

    print("################################################")
    reach_state= "defense"
    possible, _ = run_avoiding_state(states, transitions, start_state, start_time, reach_state)
    if not possible:
        print(f"Any full run must eventually reach {reach_state} (inevitable).")
    else:
        print(f"Any full run doesn't necessarily need to reach {reach_state}")


if __name__ == "__main__":
    main()
