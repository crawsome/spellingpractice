import pyttsx3
import random


# 2018 Colin Burke
# practice spelling with an assortment of features, and text-to-speech!


class spelling_game():
    def __init__(self):
        # init the engine
        self.engine = pyttsx3.init()
        self.original_rate = self.engine.getProperty('rate')
        self.rate = self.original_rate
        self.engine.setProperty('rate', self.rate - 50)

        # alternate voices
        self.voices = self.engine.getProperty('voices')
        self.voices_count = len(list(self.voices))
        self.voiceID = 0

        # our word
        self.word = ''
        self.obs_word = ''
        self.right = 0
        self.wrong = 0
        self.our_excuse = ''
        self.hintlevel = 2

        # setup our wordlist from file
        self.wordlist = []
        self.wordfile = open('words2.txt', 'r')
        for word in self.wordfile:
            self.wordlist.append(word.strip('\n').lower())

        # divide the wordlist into grades and add them to another list for indexing later
        self.gradeslist = []
        grade1_2 = [word.strip('\n').lower() for word in self.wordlist if (len(word) >= 2 and len(word) <= 4)]
        grade3_4 = [word.strip('\n').lower() for word in self.wordlist if (len(word) >= 4 and len(word) <= 5)]
        grade5_6 = [word.strip('\n').lower() for word in self.wordlist if (len(word) >= 5 and len(word) <= 6)]
        grade7_8 = [word.strip('\n').lower() for word in self.wordlist if (len(word) >= 6 and len(word) <= 7)]
        grade9_12 = [word.strip('\n').lower() for word in self.wordlist if (len(word) >= 8 and len(word) <= 9)]
        grade13_16 = [word.strip('\n').lower() for word in self.wordlist if len(word) >= 9]
        self.gradeslist.extend((grade1_2, grade3_4, grade5_6, grade7_8, grade9_12, grade13_16))

        # category names and excuses for getting it wrong
        self.gradenames = ['Kindergarten through 2nd grade. 2 to 4-letter words',
                           '3rd through 5th grade. 4 to 5-letter words',
                           '6th through 8th grade. 5 to 6-letter words', '9th through 12th grade. 6 to 7-letter words',
                           'College and beyond. 7 to 9-letter words',
                           'Challenge Mode for The mighty. 9 letters and above']
        self.excuses = [' I want a Hint',
                        'I need to hear it in a sentence',
                        'Word is not clear',
                        'Word is not a great spelling word, or an edge case',
                        'Word is obscene',
                        'Word read too slowly',
                        'Word is read too fast',
                        'I\'d like to hear it in a different voice']
        self.index_words = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth',
                            'tenth', 'eleventh', 'twelveth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth',
                            'seventeenth', 'eighteenth', 'ninteenth', 'twentyith']
        self.say_fast('Welcome to Spelling Practice!')
        self.say_fast('Please enter your name')
        self.name = input('Your name? ')
        self.say_slowly('Hi ' + self.name)

    def say_slowly(self, a_word):
        self.rate = 100
        self.engine.setProperty('rate', self.rate)
        self.engine.say(a_word)
        self.engine.runAndWait()

    def say_fast(self, a_word):
        self.engine.setProperty('rate', self.rate)
        self.engine.say(a_word)
        # optionally print the word, too
        # print('\n'+ a_word)
        self.engine.runAndWait()

    def say_slower(self, a_word):
        self.rate -= 20
        self.engine.setProperty('rate', self.rate)
        self.engine.say(a_word)
        self.engine.runAndWait()

    def say_faster(self, a_word):
        self.engine.setProperty('rate', self.rate - 100)
        self.engine.say(a_word)
        self.engine.runAndWait()

    def next_voice(self):
        self.say_fast('There are ' + str(self.voices_count) + ' voices available to use. Use next one?')
        self.engine.setProperty('voice', self.voices[self.voiceID])

    def set_voice(self):
        self.say_fast('There are ' + str(self.voices_count) + ' voices available to use. Which one will you use?')
        for index, voice in zip(range(self.voices_count), self.voices):
            print(str(index + 1) + '. ' + str(voice))
        self.engine.setProperty('voice', self.voiceID)

    def choose_level(self):
        for index, name in zip(range(len(self.gradenames)), self.gradenames):
            print(str(index + 1) + '. ' + str(name))
        self.say_fast('Which Area would you like to practice? ')
        levelchoice = input()
        self.say_fast('You chose selection ' + str(levelchoice) + '. ' + str(self.gradenames[int(levelchoice) - 1]))
        self.ourwords = self.gradeslist[int(levelchoice) - 1]

    def get_excuse(self):
        # get the excuse
        for index, excuse in zip(range(len(self.excuses)), self.excuses):
            print(str(index + 1) + '. ' + str(excuse))
        self.say_fast('Please enter the issue you had')
        self.our_excuse = input()
        # process the excuse
        self.say_fast('You said: ' + str(self.excuses[int(self.our_excuse) - 1]))
        excuse_functions = [self.hint, self.hear_in_sentence, self.exclude_word, self.say_slower, self.say_faster,
                            self.next_voice]
        excuse_functions[int(self.our_excuse) - 1]()
        # 1. I want a Hint - give hint
        # 2. I need to hear it in a sentence - Dictionary + sentences lookup
        # 3. Word is not clear -
        # 4. Word is not a great spelling word, or an edge case
        # 5. Word is obscene
        # 6. Word read too slowly
        # 7. Word is read too fast
        # 8. I'd like to hear it in a different voice

    # obscures a word with asterisks, used for a step-by-step hint method
    def hint(self):
        self.hintlevel += 1
        self.obs_word = ['*' for char in range(len(self.word))]
        for limit, letter in zip(range(self.hintlevel), self.word):
            self.say_fast(letter)

    def quiz_word(self):
        self.word = random.choice(self.ourwords)
        self.hintlevel = len(self.word) / 2 - 1
        correct = False
        while not correct:
            self.say_fast('Please spell the word.')
            self.say_slowly(self.word)
            self.say_fast('Enter r to hear again, or h for help, q to quit')
            attempt = str(input('Your answer: ')).lower()
            if attempt == 'r':
                self.say_fast('What was your issue?')
                self.get_excuse()
                continue
            elif attempt == 'q':
                self.say_fast('Thanks for playing. Good-Bye!')
                quit()
            elif attempt == 'h':
                self.hint()
            elif attempt == self.word:
                self.say_fast('Correct! Great Job!')
                correct = True
            else:
                self.say_fast('INCORRECT, TRY AGAIN?')
            print('Your answer : ' + repr(attempt))
            print('Right answer: ' + repr(self.word))

    def hear_in_sentence(self):
        pass

    def exclude_word(self):
        pass

    def new_word(self):
        pass

    def quiz_x_words(self):
        self.say_fast('How many words will be in your quiz?')
