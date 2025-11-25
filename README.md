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

coverage 
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
FootballGame.py     344     49    86%   64, 73-76, 88, 106, 132, 163, 169, 176-178, 187, 198, 214, 248, 265, 269, 284, 289, 349-354, 357, 366, 387, 435, 442-444, 453, 464, 471, 495, 529, 548, 609, 615, 627, 632, 642, 652, 657-659, 669
-----------------------------------------------
TOTAL               344     49    86%

 6834301 function calls (6350129 primitive calls) in 6.052 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
476236/122    2.457    0.000    2.608    0.021 FootballGame.py:51(dp)
        1    1.272    1.272    1.616    1.616 FootballGame.py:391(find_exact_score_path)
        1    1.079    1.079    1.401    1.401 FootballGame.py:135(find_zero_score_path)
  3212905    0.401    0.000    0.401    0.000 FootballGame.py:9(next_yardline)
        1    0.191    0.191    6.051    6.051 FootballGame.py:554(main)
   809696    0.162    0.000    0.162    0.000 {method 'add' of 'set' objects}
   756907    0.118    0.000    0.118    0.000 {method 'get' of 'dict' objects}
   809641    0.114    0.000    0.114    0.000 {method 'append' of 'collections.deque' objects}
       10    0.113    0.011    0.178    0.018 FootballGame.py:475(can_finish_from_state)
   756917    0.097    0.000    0.097    0.000 {method 'popleft' of 'collections.deque' objects}
   8058/1    0.022    0.000    0.025    0.025 FootballGame.py:97(dp_plays)
        2    0.013    0.006    0.019    0.009 FootballGame.py:250(run_avoiding_state)
       30    0.004    0.000    0.004    0.000 {built-in method builtins.print}
        1    0.004    0.004    0.182    0.182 FootballGame.py:532(find_bad_dead_end_states)
      122    0.001    0.000    2.612    0.021 FootballGame.py:45(best_score_and_plays)
        1    0.001    0.001    0.001    0.001 FootballGame.py:200(zero_score_possible)
      262    0.001    0.000    0.001    0.000 typing.py:426(inner)
      998    0.001    0.000    0.001    0.000 {built-in method builtins.getattr}
      123    0.001    0.000    0.002    0.000 functools.py:36(update_wrapper)
      123    0.001    0.000    0.002    0.000 functools.py:544(decorating_function)
        1    0.000    0.000    0.000    0.000 typing.py:3794(__getattr__)
      738    0.000    0.000    0.000    0.000 {built-in method builtins.setattr}
      123    0.000    0.000    0.000    0.000 functools.py:504(lru_cache)
       65    0.000    0.000    0.000    0.000 typing.py:1294(_is_dunder)
        1    0.000    0.000    2.561    2.561 FootballGame.py:370(check_monotone_in_time)
      262    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
      123    0.000    0.000    0.000    0.000 {method 'update' of 'dict' objects}
      130    0.000    0.000    0.000    0.000 typing.py:1443(__hash__)
        1    0.000    0.000    6.052    6.052 FootballGame.py:1(<module>)
       10    0.000    0.000    0.000    0.000 FootballGame.py:121(check_reachability)
       55    0.000    0.000    0.000    0.000 typing.py:1368(__setattr__)
      123    0.000    0.000    0.000    0.000 {built-in method builtins.callable}
       15    0.000    0.000    0.000    0.000 typing.py:173(_type_check)
        9    0.000    0.000    0.000    0.000 typing.py:1423(__init__)
        4    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
      130    0.000    0.000    0.000    0.000 {built-in method builtins.hash}
        1    0.000    0.000    0.000    0.000 FootballGame.py:315(has_positive_score_zero_time_cycle)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        5    0.000    0.000    0.000    0.000 typing.py:1634(__getitem__)
        9    0.000    0.000    0.000    0.000 typing.py:260(_collect_type_parameters)
      5/4    0.000    0.000    0.000    0.000 FootballGame.py:337(dfs)
        1    0.000    0.000    0.000    0.000 FootballGame.py:466(find_terminal_states)
      101    0.000    0.000    0.000    0.000 {method 'pop' of 'list' objects}
       65    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        1    0.000    0.000    6.052    6.052 {built-in method builtins.exec}
        7    0.000    0.000    0.000    0.000 typing.py:1658(copy_with)
       13    0.000    0.000    0.000    0.000 typing.py:1639(<genexpr>)
       10    0.000    0.000    0.000    0.000 typing.py:1358(__getattr__)
       41    0.000    0.000    0.000    0.000 typing.py:1437(__eq__)
        9    0.000    0.000    0.000    0.000 typing.py:1307(__init__)
        1    0.000    0.000    0.000    0.000 typing.py:812(Literal)
        1    0.000    0.000    0.025    0.025 FootballGame.py:95(max_plays_only)
       47    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
        2    0.000    0.000    0.000    0.000 typing.py:1748(__getitem__)
       45    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}
        1    0.000    0.000    0.000    0.000 typing.py:753(Union)
        8    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
       15    0.000    0.000    0.000    0.000 typing.py:164(_type_convert)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1390(_handle_fromlist)
        7    0.000    0.000    0.000    0.000 typing.py:1122(_is_unpacked_typevartuple)
        1    0.000    0.000    0.000    0.000 typing.py:395(_flatten_literal_params)
       26    0.000    0.000    0.000    0.000 typing.py:1427(<genexpr>)
        1    0.000    0.000    0.000    0.000 typing.py:379(_remove_dups_flatten)
        1    0.000    0.000    0.000    0.000 typing.py:580(__getitem__)
        7    0.000    0.000    0.000    0.000 typing.py:1757(<genexpr>)
        2    0.000    0.000    0.000    0.000 typing.py:351(_deduplicate)
        2    0.000    0.000    0.000    0.000 {built-in method fromkeys}
        9    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 typing.py:574(__getitem__)
        9    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        5    0.000    0.000    0.000    0.000 {method 'remove' of 'set' objects}
        3    0.000    0.000    0.000    0.000 typing.py:840(<genexpr>)
        3    0.000    0.000    0.000    0.000 typing.py:789(<genexpr>)
        2    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        3    0.000    0.000    0.000    0.000 typing.py:1803(<genexpr>)
        1    0.000    0.000    0.000    0.000 typing.py:1446(__or__)
        2    0.000    0.000    0.000    0.000 {method 'keys' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 typing.py:1802(_value_and_type_iter)

(.venv) PS C:\Users\Owner\PycharmProjects\FootballGame>  pyinstrument --load-prev 2025-11-25T09-53-50

  _     ._   __/__   _ _  _  _ _/_   Recorded: 09:53:50  Samples:  5030
 /_//_/// /_\ / //_// / //_'/ //     Duration: 6.377     CPU time: 6.328
/   _/                      v5.1.1

Program: FootballGame.py

6.370 <module>  FootballGame.py:1
└─ 6.370 main  FootballGame.py:554
   ├─ 2.788 check_monotone_in_time  FootballGame.py:370
   │  └─ 2.788 best_score_and_plays  FootballGame.py:45
   │     └─ 2.779 dp  FootballGame.py:51
   │        └─ 2.777 dp  FootballGame.py:51
   │           └─ 2.776 dp  FootballGame.py:51
   │              └─ 2.772 dp  FootballGame.py:51
   │                 └─ 2.764 dp  FootballGame.py:51
   │                    └─ 2.746 dp  FootballGame.py:51
   │                       └─ 2.722 dp  FootballGame.py:51
   │                          └─ 2.696 dp  FootballGame.py:51
   │                             └─ 2.658 dp  FootballGame.py:51
   │                                └─ 2.616 dp  FootballGame.py:51
   │                                   └─ 2.570 dp  FootballGame.py:51
   │                                      └─ 2.523 dp  FootballGame.py:51
   │                                         └─ 2.475 dp  FootballGame.py:51
   │                                            └─ 2.415 dp  FootballGame.py:51
   │                                               └─ 2.374 dp  FootballGame.py:51
   │                                                  └─ 2.332 dp  FootballGame.py:51
   │                                                     └─ 2.288 dp  FootballGame.py:51
   │                                                        └─ 2.235 dp  FootballGame.py:51
   │                                                           └─ 2.184 dp  FootballGame.py:51
   │                                                              └─ 2.155 dp  FootballGame.py:51
   │                                                                 └─ 2.109 dp  FootballGame.py:51
   │                                                                    └─ 2.064 dp  FootballGame.py:51
   │                                                                       └─ 2.022 dp  FootballGame.py:51
   │                                                                          └─ 1.984 dp  FootballGame.py:51
   │                                                                             └─ 1.952 dp  FootballGame.py:51
   │                                                                                └─ 1.914 dp  FootballGame.py:51
   │                                                                                   └─ 1.870 dp  FootballGame.py:51
   │                                                                                      └─ 1.814 dp  FootballGame.py:51
   │                                                                                         └─ 1.772 dp  FootballGame.py:51
   │                                                                                            └─ 1.730 dp  FootballGame.py:51
   │                                                                                               └─ 1.699 dp  FootballGame.py:51
   │                                                                                                  └─ 1.662 dp  FootballGame.py:51
   │                                                                                                     └─ 1.622 dp  FootballGame.py:51
   │                                                                                                        └─ 1.591 dp  FootballGame.py:51
   │                                                                                                           └─ 1.555 dp  FootballGame.py:51
   │                                                                                                              └─ 1.522 dp  FootballGame.py:51
   │                                                                                                                 └─ 1.478 dp  FootballGame.py:51
   │                                                                                                                    └─ 1.441 dp  FootballGame.py:51
   │                                                                                                                       └─ 1.411 dp  FootballGame.py:51
   │                                                                                                                          └─ 1.381 dp  FootballGame.py:51
   │                                                                                                                             └─ 1.358 dp  FootballGame.py:51
   │                                                                                                                                └─ 1.317 dp  FootballGame.py:51
   │                                                                                                                                   └─ 1.297 dp  FootballGame.py:51
   │                                                                                                                                      └─ 1.267 dp  FootballGame.py:51        
   │                                                                                                                                         └─ 1.240 dp  FootballGame.py:51     
   │                                                                                                                                            └─ 1.215 dp  FootballGame.py:51  
   │                                                                                                                                               └─ 1.190 dp  FootballGame.py:51
   │                                                                                                                                                  └─ 1.167 dp  FootballGame.py:51
   │                                                                                                                                                     └─ 1.142 dp  FootballGame.py:51
   │                                                                                                                                                        ├─ 1.005 dp  FootballGame.py:51
   │                                                                                                                                                        │  ├─ 0.898 dp  FootballGame.py:51
   │                                                                                                                                                        │  │  └─ 0.837 dp  FootballGame.py:51
   │                                                                                                                                                        │  │     └─ 0.809 dp  FootballGame.py:51
   │                                                                                                                                                        │  │        └─ 0.788 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           ├─ 0.688 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │  └─ 0.670 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │     └─ 0.639 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │        └─ 0.621 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │           └─ 0.604 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │              └─ 0.587 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                 └─ 0.571 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                    └─ 0.551 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                       └─ 0.530 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                          └─ 0.509 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                             └─ 0.481 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                └─ 0.467 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                   └─ 0.452 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                      └─ 0.427 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                         └─ 0.409 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                            └─ 0.395 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                               └─ 0.383 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                  └─ 0.367 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                     └─ 0.351 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                        └─ 0.332 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                           └─ 0.323 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                              └─ 0.301 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                 └─ 0.286 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                    └─ 0.278 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                       └─ 0.267 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                          └─ 0.249 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                             └─ 0.235 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                └─ 0.227 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                   └─ 0.220 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                      └─ 0.205 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                         └─ 0.193 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                            └─ 0.187 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                               └─ 0.181 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                                  └─ 0.173 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           │                                                                                                     └─ 0.170 dp  FootballGame.py:51
   │                                                                                                                                                        │  │           └─ 0.097 [self]  FootballGame.py
   │                                                                                                                                                        │  └─ 0.107 [self]  FootballGame.py
   │                                                                                                                                                        └─ 0.136 [self]  FootballGame.py
   ├─ 1.714 find_exact_score_path  FootballGame.py:391
   │  ├─ 1.384 [self]  FootballGame.py
   │  ├─ 0.113 next_yardline  FootballGame.py:9
   │  └─ 0.065 set.add  <built-in>
   ├─ 1.399 find_zero_score_path  FootballGame.py:135
   │  ├─ 1.096 [self]  FootballGame.py
   │  ├─ 0.106 next_yardline  FootballGame.py:9
   │  └─ 0.085 set.add  <built-in>
   ├─ 0.195 [self]  FootballGame.py
   └─ 0.180 find_bad_dead_end_states  FootballGame.py:532
      └─ 0.174 can_finish_from_state  FootballGame.py:475
