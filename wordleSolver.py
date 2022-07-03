import json
import numpy as np
import random
from typing import Dict, Set, List

class WordleSolver:
    def __init__(self, words: List[str], answers: List[str]) -> None:
        self.guessedWords = list()

        self.greyLetters = set()
        self.yellowLetters = dict()
        self.greenLetters = dict()

        self.usedLetters = set()

        self.maxLetters = dict()
        self.minLetters = dict()

        self.answers = list(answers)
        self.allWords = list(words)
    
    def evaluateWord(self, word: str, answer: str) -> List[int]:
        wordUsedLetters = np.full(len(word), False)
        answerUsedLetters = np.full(len(word), False)

        evaluation = np.full(len(word), 0)

        for index, (wordLetter, answerLetter) in enumerate(zip(word, answer)):
            if(wordLetter == answerLetter):
                evaluation[index] = 2
                wordUsedLetters[index] = True
                answerUsedLetters[index] = True

        for i, (wordLetter, wordUsedLetter) in enumerate(zip(word, wordUsedLetters)):
            if(wordUsedLetter == False):
                for j, (answerLetter, answerUsedLetter) in enumerate(zip(answer, answerUsedLetters)):
                    if(answerUsedLetter == False and wordLetter == answerLetter):
                        evaluation[i] = 1
                        answerUsedLetters[j] = True
                        wordUsedLetters[i] = True     
                        break  

        return evaluation

    def validateWord(self, word: str) -> bool:        
        for letter in self.maxLetters:
            if(word.count(letter) > self.maxLetters[letter]):
                return False

        for letter in self.minLetters:
            if(word.count(letter) < self.minLetters[letter]):
                return False

        for letter in self.greyLetters:
            if(letter in word):
                return False

        for containedLetter in self.yellowLetters:
            if(containedLetter in word):
                positions = self.yellowLetters[containedLetter]
                for position in positions:
                    if(word[position] == containedLetter):
                        return False
            else:
                return False 

        for confirmedLetter in self.greenLetters:
            if(confirmedLetter in word):
                positions = self.greenLetters[confirmedLetter]
                for position in positions:
                    if(word[position] != confirmedLetter):
                        return False
            else:
                return False

        return True

    def eliminateWords(self) -> List[str]:
        validWords = list()

        for word in self.answers:
            if(word in self.guessedWords):
                continue

            if(self.validateWord(word)):
                validWords.append(word)

        self.answers = validWords

    def findMissingLetters(self) -> Set[str]:
        missingLetters = set()

        for word in self.answers:
            for letter in word:
                if(letter in missingLetters):
                    continue

                if(letter not in self.yellowLetters and letter not in self.greenLetters):
                    missingLetters.add(letter)

        return missingLetters

    def findBestWord(self) -> str:
        if(len(self.answers) == 1 or len(self.answers) == 2):
            return self.answers[0]

        possibleGuesses = list()
        missingLetters = self.findMissingLetters()

        for word in self.allWords:
            possibleGuess = False
            for letter in word:
                if(letter in missingLetters):
                    possibleGuess = True
                    continue
                
                if(letter in self.yellowLetters or letter in self.greenLetters):
                    possibleGuess = False
                    break

            if(possibleGuess):
                possibleGuesses.append(word)
        
        wordEvaluation = dict()
        for word in possibleGuesses:
            wordEvaluation[word] = 0
            for answer in self.answers:
                wordEvaluation[word] += sum(self.evaluateWord(word, answer))

        if(len(wordEvaluation) == 0):
            for word in self.answers:
                 wordEvaluation[word] = 0
                 for answer in self.answers:
                    wordEvaluation[word] += sum(self.evaluateWord(word, answer))    
            
        return max(wordEvaluation, key=wordEvaluation.get)

    def processWord(self, word: str, result: List[str]):
        self.guessedWords.append(word)

        letterCounts = dict()
        for letter in word:
            letterCounts[letter] = word.count(letter)

        for countLetter in letterCounts:
            if(letterCounts[countLetter] > 1):
                foundMax = False

                for wordLetter, letterResult, in zip(word, result):
                    if(wordLetter == countLetter and letterResult == "0"):
                        letterCount = 0

                        for otherLetter, otherResult in zip(word, result):
                            if(otherLetter == countLetter and (otherResult == "1" or otherResult== "2")):
                                letterCount += 1

                        self.maxLetters[countLetter] = letterCount
                        foundMax = True

                if(foundMax == False):
                    self.minLetters[countLetter] = letterCounts[countLetter]

        for letterIndex, (letter, letterResult) in enumerate(zip(word, result)):
            if(letterResult== "0"):
                if(letter not in self.maxLetters):
                    self.greyLetters.add(letter)
            elif(letterResult == "1"):
                if(letter in self.yellowLetters):
                    self.yellowLetters[letter].add(letterIndex)
                else:
                    self.yellowLetters[letter] = {letterIndex} 
            elif(letterResult == "2"):
                if(letter in self.greenLetters):
                    self.greenLetters[letter].add(letterIndex)
                else:
                    self.greenLetters[letter] = {letterIndex}

            self.usedLetters.add(letter)

        self.eliminateWords()

def main():
    words = []
    answers = []

    with open("five-letter-words.txt", 'r') as f:
        words = f.readlines()

    with open("possible-solutions.txt", 'r') as f:
        answers = f.readlines()

    for i in range(len(words)):
        words[i] = words[i].replace("\n", "").lower()

    for i in range(len(answers)):
        answers[i] = answers[i].replace("\n", "").lower()

    numOfGuesses = 0
    wordleSolver = WordleSolver(words, answers)
    while(True):
        guessedWord = str(input("What word was guessed? ")).lower()
        wordResult = str(input("What was the result? ")).split()

        numOfGuesses += 1

        wordleSolver.processWord(guessedWord, wordResult)

        if(wordResult.count("2") == 5):
            break

        print("Remaining words:")
        for word in wordleSolver.answers:
            print("- " + word)
        print()
        if(len(wordleSolver.answers) == 1):
            print("The answer is: " + wordleSolver.answers[0])
        elif(len(wordleSolver.answers) == 2):
            print("There are only two options remaining, pick one")
        else:
            print("Calculating best guess:")
            bestGuess =  wordleSolver.findBestWord()
            if(bestGuess == ""):
                print("No suggestions avaliable")
            else:
                print("- " + bestGuess)
                print()

    print()
    print("Number of guesses " + str(numOfGuesses))
    print("Guesses: ")
    for word in wordleSolver.guessedWords:
        print("- " + word)

if(__name__ == "__main__"):
    main()