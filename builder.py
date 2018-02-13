"""
A utility class for building SSML format text.
@author: user3301
@date: 2018-02-06
"""
import re


class Speech:

    # @constructor
    def __init__(self):
        self.content = []

    # This appends raw text into the <speak/> tag
    # @param saying The raw text insert into the speak tag.
    # returns {self} 
    def say(self, saying):
        self.present(saying, "The saying provided was null")
        self.content.append(self.escape(saying))
        return self

    # inserts a paragraph tag.
    # @param paragraph The paragraph of text to insert
    # @returns {self}
    def paragraph(self, paragraph):
        self.present(paragraph, "The paragraph was null")
        self.content.append("<p>" + self.escape(paragraph) + "</p>")
        return self

    # insert a sentence tag.
    # @param saying The sentence to insert
    # @returns {self}
    def sentence(self, saying):
        self.present(saying, "The sentence was null")
        self.content.append("<s>" + self.escape(saying) + "</s>")
        return self

    # insert a break tag.
    # @param duration the duration for the pause
    # @returns {self}
    def pause(self, duration):
        self.present(duration, "The duration was null")
        self.validateDuration(duration)
        self.content.append("<break time='" + duration + "'/>")
        return self

    # create break tag that will pause the audio based upon the strength level.
    # @param strength the strength level
    # @returns {self}
    def pauseByStrength(self, strength):
        self.present(strength, "the strength was null")
        strength = strength.lower().strip()
        if strength in ("none", "x-weak", "weak", "medium", "strong", "x-strong"):
            self.content.append("<break strength='" + strength + "'/>")
            return self
        else:
            raise ValueError("The strength was not valid.")

    # insert a say-as = spell-out tag
    # @param word the raw text insert into the say-as tag
    # @returns {self}
    def spell(self, word):
        self.present(word, "The word was null")
        self.content.append("<say-as interpret-as='spell-out'>" + self.escape(word) + "</say-as>")
        return self

    # insert a say-as = spell-out tag for every single word
    # @param words the raw text
    # @param delay the interval in each word
    # @returns {self}
    def spellSlowly(self, words, delay):
        self.present(words, "The word was null")
        self.validateDuration(delay)
        for word in words.split(''):
            self.content += "<say-as interpret-as='spell-out'>" + self.escape(word) + "</say-as>"
            self.pause(delay)
        return self

    # make this speech into ssml text

    # Validates that the provided value is not null or undefined. It will throw an exception if it's either.
    def present(self, value, msg):
        if value is None:
            raise Exception(msg)

    # construct an SSML format string
    # @param excludeSpeakTag boolean value to determine if root tag <speak/> is needed
    # @returns {string}
    def ssml(self, excludeSpeakTag):
        if excludeSpeakTag:
            return ' '.join(self.content)
        else:
            return '<speak>' + ' '.join(self.content) + '</speak>'

    # This method escapes any special characters that will cause SSML to be invalid
    def escape(self, word):
        if isinstance(word, basestring):
            word = word.replace('&', 'and')
            word = word.replace('<', '')
            word = word.replace('>', '')
            word = word.replace('\"', '')
            word = word.replace('\'', '')
            return word
        if isinstance(word, (int, float, complex, bool)):
            return word
        raise Exception("received invalid type")

    # check if the duration is in correct format (a positive number followed by 's' or 'ms') and in the legit
    # range (0ms - 10000ms)
    # @param duration The duration of a pause
    # @throws Exception  when the duration is not in the correct format or exceed the legit length
    def validateDuration(self, duration):
        pattern = "^(\d*\.?\d+)(s|ms)$"
        if re.match(pattern, duration):
            matcher = re.search(pattern, duration)
            pauseDuration = int(matcher.group(1))
            pauseType = matcher.group(2)
            if pauseType.lower() == 's' and pauseDuration > 10:
                raise Exception("The duration exceeds the maximum length.")
            elif pauseDuration > 10000:
                raise Exception("The duration exceeds the maximum length.")
        else:
            raise Exception("The format of the duration is incorrect.")
