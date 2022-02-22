# Wordle Solver

## About
### This is a simple wordle solver I created as a coding challenge. The evaluation for finding the best word works by iterating over each word and comparing it to every other word checking what the outcome of that word being the answer would be and summing that output array where it then picks the word with the highest overall sum.

## Instructions
* To run the solver run the wordleSolver.py file and make sure the words file is in the same folder
* The program will ask for the guess you made and the result
* The result is a string of numbers - 0 for grey, 1 for yellow, and 2 for green e.g. 0 1 1 0 2
* The best word will then appear and also the remaining words that could be the answer
* To stop the program enter 2 2 2 2 2 in the result and it will then give you a summary of your game
