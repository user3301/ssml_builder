"""Unit tests for SSML Builder."""

import unittest
from ssml_builder import Speech


class TestBuilder(unittest.TestCase):
    """Test cases for Speech SSML builder."""

    def test_010_Say(self) -> None:
        """Test the say method."""
        speech = Speech()
        speech.say("Hello,this is polly.")
        speech.say("Good to see you.")

        self.assertEqual(speech.content, ['Hello,this is polly.', 'Good to see you.'])
        self.assertEqual(speech.ssml(True), "Hello,this is polly. Good to see you.")
        self.assertEqual(speech.ssml(False), "<speak>Hello,this is polly. Good to see you.</speak>")

    def test_011_Say_Escape(self) -> None:
        """Test the say method with special characters that need escaping."""
        speech = Speech()
        speech.say("Hello, it's me & polly")

        self.assertEqual(speech.content, ["Hello, its me and polly"])

    def test_020_Paragraph(self) -> None:
        """Test the paragraph method."""
        speech = Speech()
        speech = speech.paragraph(
            "Paragraphs are commonly numbered using the decimal system, where (in books) the integral part of the decimal represents the number of the chapter and the fractional parts are arranged in each chapter in order of magnitude.")

        self.assertEqual(speech.content, [
            "<p>Paragraphs are commonly numbered using the decimal system, where (in books) the integral part of the decimal represents the number of the chapter and the fractional parts are arranged in each chapter in order of magnitude.</p>"])
        self.assertEqual(speech.ssml(False),
                         "<speak><p>Paragraphs are commonly numbered using the decimal system, where (in books) the integral part of the decimal represents the number of the chapter and the fractional parts are arranged in each chapter in order of magnitude.</p></speak>")

    def test_030_Sentence(self) -> None:
        """Test the sentence method."""
        speech = Speech()
        speech = speech.sentence(
            "A sentence is a set of words that is complete in itself, typically containing a subject and predicate")

        self.assertEqual(speech.content, [
            "<s>A sentence is a set of words that is complete in itself, typically containing a subject and predicate</s>"])

    def test_040_Pause(self) -> None:
        """Test the pause method."""
        speech = Speech()
        speech.say("Hello.")
        speech.pause("1s")

        self.assertEqual(speech.content, ["Hello.", "<break time='1s'/>"])

    def test_050_pauseByStrength(self) -> None:
        """Test the pauseByStrength method."""
        speech = Speech()
        speech.pauseByStrength("weak")

        self.assertEqual(speech.content, ["<break strength='weak'/>"])

    def test_060_spell(self) -> None:
        """Test the spell method."""
        speech = Speech()
        speech.spell("bye")

        self.assertEqual(speech.content, ["<say-as interpret-as='spell-out'>bye</say-as>"])

    def test_070_spellSlowly(self) -> None:
        """Test the spellSlowly method."""
        speech = Speech()
        speech.spellSlowly("Hi", "1s")

        self.assertEqual(speech.content, ["<say-as interpret-as='spell-out'>H</say-as>", "<break time='1s'/>",
                                          "<say-as interpret-as='spell-out'>i</say-as>", "<break time='1s'/>"])

    def test_080_whispered(self) -> None:
        """Test the whispered method."""
        speech = Speech()
        speech.whispered("tell you a secret")

        self.assertEqual(speech.content, ["<amazon:effect name='whispered'>tell you a secret</amazon:effect>"])

    def test_081_softPhonation(self) -> None:
        """Test the softPhonation method."""
        speech = Speech()
        speech.softPhonation("This is Matthew speaking in my softer voice")

        self.assertEqual(speech.content, ["<amazon:effect phonation='soft'>This is Matthew speaking in my softer "
                                          "voice</amazon:effect>"])

    def test_090_emphasis(self) -> None:
        """Test the emphasis method."""
        speech = Speech()
        speech.emphasis("really like", "strong")

        self.assertEqual(speech.content, ["<emphasis level='strong'>really like</emphasis>"])

    def test_100_lang(self) -> None:
        """Test the lang method."""
        speech = Speech()
        speech.lang("Je ne parle pas français", "fr-FR")

        self.assertEqual(speech.content, ["<lang xml:lang='fr-FR'>Je ne parle pas français</lang>"])

    def test_110_phoneme(self) -> None:
        """Test the phoneme method."""
        speech = Speech()
        speech.phoneme("pecan", "ipa", ["b", "d", "d͡ʒ"])

        self.assertEqual(speech.content, ["<phoneme alphabet='ipa' ph='bdd͡ʒ'>pecan</phoneme>"])

    def test_111_toXML(self) -> None:
        """Test the toXML method."""
        speech = Speech()
        speech.say("hello,").say("it's me & polly.").paragraph("Paragraphs are commonly numbered using the decimal system, where (in books) the integral part of the decimal represents the number of the chapter and the fractional parts are arranged in each chapter in order of magnitude.")

        print(speech.toXML())


if __name__ == "__main__":
    unittest.main()
