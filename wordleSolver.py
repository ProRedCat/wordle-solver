import json
import numpy as np

from typing import Dict, Set, List

from pyparsing import Word

class WordleSolver:
    def __init__(self, words: List[str]) -> None:
        self.guessedWords = list()

        self.greyLetters = set()
        self.yellowLetters = dict()
        self.greenLetters = dict()

        self.usedLetters = set()

        self.maxLetters = dict()
        self.minLetters = dict()

        self.wordsList = list(words)
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

        for index, (wordLetter, wordUsedLetter) in enumerate(zip(word, wordUsedLetters)):
            if(wordUsedLetter == False):
                for answerLetter, answerUsedLetter in zip(answer, answerUsedLetters):
                    if(answerUsedLetter == False and wordLetter == answerLetter):
                        evaluation[index] = 1
                        answerUsedLetters[index] = True
                        wordUsedLetters[index] = True     
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

        for word in self.wordsList:
            if(self.validateWord(word)):
                validWords.append(word)

        self.wordsList = validWords

    # def findBestWord(self) -> str:
    #     wordCount = 0
    #     wordEvaluation = dict()
    #     for word in self.wordsList:
    #         if(word not in self.guessedWords):
    #             wordEvaluation[word] = 0
    #             for answer in self.wordsList:
    #                 wordEvaluation[word] += sum(self.evaluateWord(word, answer))

    #         wordCount += 1

    #     if(len(wordEvaluation) == 0):
    #         return ""    
            
    #     return max(wordEvaluation, key=wordEvaluation.get)

    def findMissingLetters(self) -> Set[str]:
        missingLetters = set()

        for word in self.wordsList:
            for letter in word:
                if(letter in missingLetters):
                    continue

                if(letter not in self.yellowLetters and letter not in self.greenLetters):
                    missingLetters.add(letter)

        return missingLetters

    def findBestWord(self) -> str:
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
            for answer in self.wordsList:
                wordEvaluation[word] += sum(self.evaluateWord(word, answer))

        if(len(wordEvaluation) == 0):
            return ""    
            
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
                    if(wordLetter == letter and letterResult == "0"):
                        letterCount = 0

                        for otherLetter, otherResult in zip(word, result):
                            if(otherLetter == letter and (otherResult == "1" or otherResult== "2")):
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

    with open("five-letter-words.txt", 'r') as f:
        words = f.readlines()

    for i in range(len(words)):
        words[i] = words[i].replace("\n", "").lower()

    wordleSolver = WordleSolver(words)

    numOfGuesses = 0
    while(True):
        guessedWord = str(input("What word was guessed? ")).lower()
        print(wordleSolver.evaluateWord(guessedWord, "balls"))
        wordResult = str(input("What was the result? ")).split()

        numOfGuesses += 1

        wordleSolver.processWord(guessedWord, wordResult)

        if(wordResult.count("2") == 5):
            break

        print("Remaining words:")
        for word in wordleSolver.wordsList:
            print("- " + word)
        print()
        if(len(wordleSolver.wordsList) == 1):
            print("The answer is: " + wordleSolver.wordsList[0])
        else:
            bestGuess =  wordleSolver.findBestWord()
            if(bestGuess == ""):
                print("No suggestions avaliable")
            else:
                print("Best guess: ")
                
                print("- " + bestGuess)
                print()

    print()
    print("Number of guesses " + str(numOfGuesses))
    print("Guesses: ")
    for word in wordleSolver.guessedWords:
        print("- " + word)

if(__name__ == "__main__"):
    main()