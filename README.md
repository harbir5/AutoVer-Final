Author: Harbir S. Dhillon
CS6315 Automated Verification
Fall 2025

FINAL PROJECT

DO NOT RUN FootballGame.py 
- Have commented it out just to be safe

Run FootballGame2.py to see results. 

(.venv) PS C:\Users\Owner\PycharmProjects\FootballGame> ruff check FootballGame2.py
All checks passed!
(.venv) PS C:\Users\Owner\PycharmProjects\FootballGame> radon cc FootballGame2.py -a
FootballGame2.py
    F 259:0 main - C
    F 85:0 find_zero_score_path - B
    F 196:0 run_avoiding_state - B
    F 146:0 zero_score_possible - B
    F 71:0 check_reachability - A
    F 4:0 best_score_and_plays - A
    F 49:0 max_plays_only - A

7 blocks (classes, functions, methods) analyzed.
Average complexity: B (6.857142857142857)

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
