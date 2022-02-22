from typing import Dict, Set, List
import json
def evaluateWord(word: str, answer: str) -> List[int]:
    wordUsedLetters = [False, False, False, False, False]
    answerUsedLetters = [False, False, False, False, False]

    evaluation = [0, 0, 0, 0, 0]

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

def validateWord(greyLetters: Set[str], yellowLetters: Dict[str, List[int]], greenLetters: Dict[str, List[int]], maxLetters: Dict[str, int], minLetters: Dict[str, int], word: str) -> bool:        
    for letter in maxLetters:
        if(word.count(letter) > maxLetters[letter]):
            return False

    for letter in minLetters:
        if(word.count(letter) < minLetters[letter]):
            return False

    for letter in greyLetters:
        if(letter in word):
            return False

    for containedLetter in yellowLetters:
        if(containedLetter in word):
            positions = yellowLetters[containedLetter]
            for position in positions:
                if(word[position] == containedLetter):
                    return False
        else:
            return False 

    for confirmedLetter in greenLetters:
        if(confirmedLetter in word):
            positions = greenLetters[confirmedLetter]
            for position in positions:
                if(word[position] != confirmedLetter):
                    return False
        else:
            return False

    return True

def eliminateWords(greyLetters: Set[str], yellowLetters: Dict[str, List[int]], greenLetters: Dict[str, List[int]], maxLetters: Dict[str, int], minLetters: Dict[str, int], wordsList) -> List[str]:
    validWords = []

    for word in wordsList:
        if(validateWord(greyLetters, yellowLetters, greenLetters, maxLetters, minLetters, word)):
            validWords.append(word)

    return validWords

def findBestWord(guessedWords: List[str], wordsList: List[str]) -> str:
    wordCount = 0
    wordEvaluation = dict()
    for word in wordsList:
        if(word not in guessedWords):
            wordEvaluation[word] = 0
            for answer in wordsList:
                wordEvaluation[word] += sum(evaluateWord(word, answer))

        wordCount += 1
        
    return max(wordEvaluation, key=wordEvaluation.get)

words = []

with open("five-letter-words.txt", 'r') as f:
    words = f.readlines()

for i in range(len(words)):
    words[i] = words[i].replace("\n", "").lower()

guessedWords = []
greyLetters = set()
yellowLetters = dict()
greenLetters = dict()

maxLetters = dict()
minLetters = dict()

wordsList = list(words)

numOfGuesses = 0

while(True):
    guessedWord = str(input("What word was guessed? "))
    wordResult = str(input("What was the result? ")).split()

    guessedWords.append(guessedWord)
    numOfGuesses += 1

    if(wordResult.count("2") == 5):
        break

    letterCounts = dict()
    for letter in guessedWord:
        letterCounts[letter] = guessedWord.count(letter)

    for letter in letterCounts:
        if(letterCounts[letter] > 1):
            foundMax = False
            for i in range(len(wordResult)):
                if(guessedWord[i] == letter and wordResult[i] == "0"):
                    letterCount = 0
                    for j in range(len(wordResult)):
                        if(guessedWord[j] == letter and (wordResult[j] == "1" or wordResult[j] == "2")):
                            letterCount += 1
                    maxLetters[letter] = letterCount
                    foundMax = True
            if(foundMax == False):
                minLetters[letter] = letterCounts[letter]

    for i in range(len(wordResult)):
        if(wordResult[i] == "0"):
            if(guessedWord[i] not in maxLetters):
                greyLetters.add(guessedWord[i])
        elif(wordResult[i] == "1"):
            if(guessedWord[i] in yellowLetters):
                yellowLetters[guessedWord[i]].add(i)
            else:
                yellowLetters[guessedWord[i]] = {i} 
        elif(wordResult[i] == "2"):
            if(guessedWord[i] in greenLetters):
                greenLetters[guessedWord[i]].add(i)
            else:
                greenLetters[guessedWord[i]] = {i}

    # print(greyLetters)
    # print(yellowLetters)
    # print(greenLetters)
    # print(maxLetters)
    
    wordsList = eliminateWords(greyLetters, yellowLetters, greenLetters, maxLetters, minLetters, wordsList)

    print("Remaining words:")
    for word in wordsList:
        print("- " + word)

    print("Best word: ")
    print("- " + findBestWord(guessedWords, wordsList))
    print()

print()
print("Number of guesses " + str(numOfGuesses))
print("Guesses: ")
for word in guessedWords:
    print("- " + word)