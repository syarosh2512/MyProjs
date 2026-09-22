class WordSet:
    def __init__(self):
        self.words = set()

    def addText(self, text):
        text = self.cleanText(text)
        for word in text.split():
            self.words.add(word)

    def cleanText (self, text):
        text = text.replace('!', '|').replace('?', '|').replace('.', '').replace(',', '|').replace('|','')
        return text.lower()

wordSet = WordSet()

wordSet.addText('Hi I\'m Ryan! Here is a sentence I want to add!')
#wordSet.addText('I\'m going to add another sentence!')


print(wordSet.words)