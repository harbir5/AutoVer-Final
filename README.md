Author: Harbir S. Dhillon
CS6315 Automated Verification
Fall 2025

FINAL PROJECT

Run FootballGame2.py to see results. 

(.venv) PS C:\Users\Owner\PycharmProjects\FootballGame> ruff check FootballGame2.py
All checks passed!

What it does for this file:

-Flag unreachable code, unused imports (e.g. if any creep in), unused variables.
-Point out duplicated logic (like repeated string comparisons for down names).
-Suggest cleaner / more idiomatic patterns (e.g., using a set for {"first down", "second down", ...}).
-Catch things like possible KeyError on transitions.get(state) when None is used.


(.venv) PS C:\Users\Owner\PycharmProjects\FootballGame> radon cc FootballGame.py -a
FootballGame.py
    F 554:0 main - C
    F 135:0 find_zero_score_path - C
    F 250:0 run_avoiding_state - C
    F 391:0 find_exact_score_path - C
    F 200:0 zero_score_possible - B
    F 475:0 can_finish_from_state - B
    F 9:0 next_yardline - B
    F 315:0 has_positive_score_zero_time_cycle - B
    F 121:0 check_reachability - A
    F 370:0 check_monotone_in_time - A
    F 466:0 find_terminal_states - A
    F 532:0 find_bad_dead_end_states - A
    F 45:0 best_score_and_plays - A
    F 95:0 max_plays_only - A

14 blocks (classes, functions, methods) analyzed.
Average complexity: B (7.0)


It can give cyclomatic complexity for functions

(.venv) PS C:\Users\Owner\PycharmProjects\FootballGame> mypy FootballGame2.py
FootballGame2.py:23: error: Need type annotation for "best"  [var-annotated]
FootballGame2.py:49: error: Incompatible return value type (got "tuple[float, float, list[Any]]", expected "tuple[int, int, list[str]]")  [return-value]
FootballGame2.py:86: error: Argument 1 to "extend" of "list" has incompatible type "list[str] | None"; expected "Iterable[str]"  [arg-type]
FootballGame2.py:102: error: Need type annotation for "q"  [var-annotated]
FootballGame2.py:168: error: Need type annotation for "q"  [var-annotated]
FootballGame2.py:223: error: Need type annotation for "q"  [var-annotated]
Found 6 errors in 1 file (checked 1 source file)

(.venv) PS C:\Users\Owner\PycharmProjects\FootballGame> mypy FootballGame2.py
Success: no issues found in 1 source file

It is a type checked: 
-Ensure states and transitions are always used with the right key/value types.
-Catch cases where a function might return different shapes of tuples.
-Verify that functions like best_score_and_plays, find_zero_score_path, etc., always return what their docstrings promise.