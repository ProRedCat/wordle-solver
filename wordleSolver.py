import json
import numpy as np

from typing import Dict, Set, List

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
    
    def evaluateWord(self, word: str, answer: str) -> List[int]:
        wordUsedLetters = np.full(len(word), False)
        answerUsedLetters = np.full(len(word), False)

        evaluation = np.full(len(word), 0)

        for i in range(len(word)):
            if(word[i] == answer[i]):
                evaluation[i] = 2
                wordUsedLetters[i] = True
                answerUsedLetters[i] = True

        for i in range(len(word)):
            if(wordUsedLetters[i] == False):
                for j in range(len(answer)):
                    if(answerUsedLetters[j] == False and word[i] == answer[j]):
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

        for word in self.wordsList:
            if(self.validateWord(word)):
                validWords.append(word)

        self.wordsList = validWords

    def findBestWord(self) -> str:
        wordCount = 0
        wordEvaluation = dict()
        for word in self.wordsList:
            if(word not in self.guessedWords):
                wordEvaluation[word] = 0
                for answer in self.wordsList:
                    wordEvaluation[word] += sum(self.evaluateWord(word, answer))

            wordCount += 1

        if(len(wordEvaluation) == 0):
            return ""    
            
        return max(wordEvaluation, key=wordEvaluation.get)

    def processWord(self, word: str, result: List[str]):
        self.guessedWords.append(word)

        letterCounts = dict()
        for letter in word:
            letterCounts[letter] = word.count(letter)

        for letter in letterCounts:
            if(letterCounts[letter] > 1):
                foundMax = False
                for i in range(len(result)):
                    if(word[i] == letter and result[i] == "0"):
                        letterCount = 0
                        for j in range(len(result)):
                            if(word[j] == letter and (result[j] == "1" or result[j] == "2")):
                                letterCount += 1
                        self.maxLetters[letter] = letterCount
                        foundMax = True
                if(foundMax == False):
                    self.minLetters[letter] = letterCounts[letter]

        for i in range(len(result)):
            if(result[i] == "0"):
                if(word[i] not in self.maxLetters):
                    self.greyLetters.add(word[i])
            elif(result[i] == "1"):
                if(word[i] in self.yellowLetters):
                    self.yellowLetters[word[i]].add(i)
                else:
                    self.yellowLetters[word[i]] = {i} 
            elif(result[i] == "2"):
                if(word[i] in self.greenLetters):
                    self.greenLetters[word[i]].add(i)
                else:
                    self.greenLetters[word[i]] = {i}
            self.usedLetters.add(word[i])

        self.eliminateWords()

words = []

with open("five-letter-words.txt", 'r') as f:
    words = f.readlines()

for i in range(len(words)):
    words[i] = words[i].replace("\n", "").lower()

wordleSolver = WordleSolver(words)

numOfGuesses = 0

while(True):
    guessedWord = str(input("What word was guessed? ")).lower()
    wordResult = str(input("What was the result? ")).split()

    numOfGuesses += 1

    if(wordResult.count("2") == 5):
        break

    wordleSolver.processWord(guessedWord, wordResult)


    print("Remaining words:")
    for word in wordleSolver.wordsList:
        print("- " + word)
    print()
    if(len(wordleSolver.wordsList) == 1):
        print("The answer is: " + wordleSolver.wordsList[0])
    else:
        print("Best guess: ")
        print("- " + wordleSolver.findBestWord())
        print()

print()
print("Number of guesses " + str(numOfGuesses))
print("Guesses: ")
for word in wordleSolver.guessedWords:
    print("- " + word)