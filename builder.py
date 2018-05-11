# coding=utf-8
"""
A utility class for building SSML format text.
@author: user3301
@date: 2018-02-06
"""
import re

from six import string_types


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
        for word in words:
            self.content.append("<say-as interpret-as='spell-out'>" + self.escape(word) + "</say-as>")
            self.pause(delay)
        return self

    # ----------------------------------------------amazon effect ------------------------------------------------------

    # insert an amazon "whispered" effect tag
    # @param saying the raw text
    # @returns {self}
    def whispered(self, saying):
        self.present(saying, "The saying is null")
        self.content.append("<amazon:effect name='whispered'>" + self.escape(saying) + "</amazon:effect>")
        return self

    # TODO <amazon:effect vocal-tract-length> tag for timbre

    # insert an amazon "soft phonation" effect tag
    # @param saying the raw text
    # @returns {self}
    def softPhonation(self, saying):
        self.present(saying, "The saying is null")
        self.content.append("<amazon:effect phonation='soft'>" + self.escape(saying) + "</amazon:effect>")
        return self

    # insert an amazon "dynamic range compression(drc)" effect tag to enhance the volume of certain sounds in a conversation
    # @param saying the raw text
    # @returns {self}
    def drc(self, saying):
        self.present(saying, "The saying is null")
        self.content.append("<amazon:effect name='drc'>" + self.escape(saying) + "</amazon:effect>")
        return self

    # insert a mark tag, this tag provides the user with the ability to place a custom tag within the text. No action is
    # taken on the tag by Amazon Polly, but when SSML metadata is returned, the position of this tag will also be returned.
    # @param tag_name the custom tag
    # returns {self}
    # def mark(self, tag_name):
    #     self.present(tag_name, "Tag name is null")
    #     self.content.append("<mark name='%s'/>"% tag_name)
    #     return self

    # -----------------------------------------end of amazon effect------------------------------------------------------

    # insert an emphasis tag
    # @param saying the raw text
    # @param level the degree of emphasis that you want to place on the text
    # @returns {self}
    def emphasis(self, saying, level):
        self.present(saying, "The saying is null")
        if level.lower() not in ["strong", "moderate", "reduced"]:
            raise Exception("The level type is invalid")
        else:
            self.content.append("<emphasis level='%s'>" % level + self.escape(saying) + "</emphasis>")
        return self

    # insert an language tag
    # @param saying the raw text
    # @param accentType the accent voice attemptted to use
    # @returns {self}
    def lang(self, saying, accentType):
        langSet = {"da-DK", "nl-NL", "en-AU", "en-GB", "en-IN", "en-US", "en-GB-WLS", "fr-FR", "fr-CA", "de-DE",
                   "is-IS", "it-IT", "ja-JP", "ko-KR", "nb-NO", "pl-PL", "pt-BR", "pt-PT", "ro-RO", "ru-RU", "es-ES",
                   "es-US", "sv-SE", "tr-TR", "cy-GB"}
        self.present(saying, "The saying is null")
        if accentType not in langSet:
            raise Exception("The language type is invalid")
        else:
            self.content.append("<lang xml:lang='%s'>" % accentType + self.escape(saying) + "</lang>")
        return self

    # insert a phonetic tag for the indicated text to provide a phonetic pronunciation
    # @param word the indicated text
    # @param alphabet phoneme system used
    # @param ph indicates the phonetic symbols to be used for pronunciation
    # returns {self}
    def phoneme(self, word, alphabet, ph):
        self.present(word, "The word is null")
        if alphabet is "ipa":
            ipaPhonemes = {"b", "d", "d͡ʒ", "ð", "f", "g", "h", "j", "k", "l", "m", "n", "ŋ", "p", "ɹ", "s", "ʃ", "t", "t͡ʃ", "Θ", "v", "w", "z", "ʒ", "ə", "ɚ", "æ", "aɪ", "aʊ", "ɑ", "eɪ", "ɝ", "ɛ", "i:", "ɪ", "oʊ", "ɔ", "ɔɪ", "u", "ʊ", "ʌ", "\'", ",", "."}
            if set(ph).issubset(ipaPhonemes):
                phValue = ''.join(str(x) for x in ph)
                self.content.append("<phoneme alphabet='%s' ph='%s'>"%(alphabet, phValue) + self.escape(word) + "</phoneme>")
            else:
                raise Exception("The phonetic symbols is invalid")
        elif alphabet is "x-sampa":
            xsampaPhonemes = {"b", "d", "dZ", "D", "f", "g", "h", "j", "k", "l", "m", "n", "N", "p", "r\\", "s", "S", "t", "tS", "T", "v", "w", "z", "Z", "@", "@\'", "{", "aI", "aU", "A", "eI", "3\'", "E", "i", "I", "oU", "O", "OI", "u", "U", "V", "\"", "%", "."}
            if set(ph).issubset(xsampaPhonemes):
                phValue = ''.join(str(x) for x in ph)
                self.content.append("<phoneme alphabet='%s' ph='%s'>" % (alphabet, phValue) + self.escape(word) + "</phoneme>")
            else:
                raise Exception("The phonetic symbols is invalid")
        else:
            raise Exception("The alphabet standard is invalid")
        return self

    def prosody(self, word, attributes):
        self.present(word, "The word is null")

        validRates = {"x-slow", "slow", "medium", "fast", "x-fast"}
        validPitches = {"x-slow", "slow", "medium", "fast", "x-fast"}
        validVolumns = {"silent", "x-soft", "soft", "medium", "loud", "x-loud"}
    #TODO wip


    # This method escapes any special characters that will cause SSML to be invalid
    # @param word the word needs to be examed
    # returns {word} the replaced word string
    def escape(self, word):
        if isinstance(word, string_types):
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

    # convert SSML format string into XML format
    # returns {xml}
    def toXML(self):
        xml = "<?xml version='1.0'?>\n<speak version='1.1'\n xmlns='http://www.w3.org/2001/10/synthesis'\n xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'\n xsi:schemaLocation='http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis11/synthesis.xsd'\n xml:lang='en-US'>" + self.ssml(True) + "</speak>"
        return xml
