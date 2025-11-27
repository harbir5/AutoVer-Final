Author: Harbir S. Dhillon
CS6315 Automated Verification
Fall 2025

FINAL PROJECT

See AutoVer Final Paper for analysis

Run FootballGame2.py to see results. 

How to run static and dynamic analysis:

Static Tools: 
- ruff check FootballGame.py  (All checks passed!)
- mypy FootballGame.py     (Success: no issues found in 1 source file)
- radon cc FootballGame.py -a    (see results)

Dynamic Tools (run to see results or reference report:
- coverage run FootballGame.py -> coverage report -m                 
- python -m cProfile -s tottime FootballGame.py
- pyinstrument FootballGame.py     

