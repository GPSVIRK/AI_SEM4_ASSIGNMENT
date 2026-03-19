import random as rnd

rnd.seed()

class CaptchaLogic:
    def __init__(self):
        self.DATA = {"apple":1, "car":0, "banana":1, "pineapple":1, "mango":1, "tire":0, "steering":0, "wheel":0}
        self.main_word , self.valid_words = randomised(self.DATA)
#str:key, if key1 == key2 then str1 and str2 are related

    def validate(self,selectedWords):#will use tkinter display, button select, submit calls this
        if (len(selectedWords) == 0) or (selectedWords[0] == ''):
            for word in self.valid_words:
                if self.DATA[word] == self.DATA[self.main_word]:
                    return False
        else:
            for word in selectedWords:
                if self.DATA[word] != self.DATA[self.main_word]:
                    return False

            for word in self.valid_words:
                if (self.DATA[word] == self.DATA[self.main_word]) and (word not in selectedWords):
                    return False

        return True

def randomised(DATA):#returns str list(str)
    words = list(DATA.keys())

    usedInd = list()

    while len(usedInd) < 4:
        ind = rnd.randrange(len(words))
        if ind not in usedInd:
            usedInd.append(ind)

    validWords = [words[usedInd[i]] for i in range(1,4)]
    mainWord = words[usedInd[0]]

    return mainWord, validWords
