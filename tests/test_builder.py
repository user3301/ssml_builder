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


if __name__ == "__main__":
    unittest.main()
