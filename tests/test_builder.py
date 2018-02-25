import unittest
from builder import Speech


class Test_Builder(unittest.TestCase):

    def test_010_Say(self):
        speech = Speech()
        speech.say("Hello,this is polly.")
        speech.say("Good to see you.")

        self.assertEqual(speech.content, ['Hello,this is polly.', 'Good to see you.'])
        self.assertEqual(speech.ssml(True), "Hello,this is polly. Good to see you.")
        self.assertEqual(speech.ssml(False), "<speak>Hello,this is polly. Good to see you.</speak>")

    def test_011_Say_Escape(self):
        speech = Speech()
        speech.say("Hello, it's me & polly")

        self.assertEqual(speech.content, ["Hello, its me and polly"])

    def test_020_Paragraph(self):
        speech = Speech()
        speech = speech.paragraph("Paragraphs are commonly numbered using the decimal system, where (in books) the integral part of the decimal represents the number of the chapter and the fractional parts are arranged in each chapter in order of magnitude.")

        self.assertEqual(speech.content, ["<p>Paragraphs are commonly numbered using the decimal system, where (in books) the integral part of the decimal represents the number of the chapter and the fractional parts are arranged in each chapter in order of magnitude.</p>"])
        self.assertEqual(speech.ssml(False), "<speak><p>Paragraphs are commonly numbered using the decimal system, where (in books) the integral part of the decimal represents the number of the chapter and the fractional parts are arranged in each chapter in order of magnitude.</p></speak>")

    def test_030_Sentence(self):
        speech = Speech()
        speech = speech.sentence("A sentence is a set of words that is complete in itself, typically containing a subject and predicate")

        self.assertEqual(speech.content, ["<s>A sentence is a set of words that is complete in itself, typically containing a subject and predicate</s>"])

    def test_040_Pause(self):
        speech = Speech()
        speech.say("Hello.")
        speech.pause("1s")

        self.assertEqual(speech.content,["Hello.", "<break time='1s'/>"])

    def test_050_pauseByStrength(self):
        speech = Speech()
        speech.pauseByStrength("weak")

        self.assertEqual(speech.content, ["<break strength='weak'/>"])

    def test_060_spell(self):
        speech = Speech()
        speech.spell("bye")

        self.assertEqual(speech.content,["<say-as interpret-as='spell-out'>bye</say-as>"])

    def test_070_spellSlowly(self):
        speech = Speech()
        speech.spellSlowly("Hi","1s")

        self.assertEqual(speech.content, ["<say-as interpret-as='spell-out'>H</say-as>", "<break time='1s'/>", "<say-as interpret-as='spell-out'>i</say-as>", "<break time='1s'/>"])

if __name__ == "__main__":
    unittest.main()
