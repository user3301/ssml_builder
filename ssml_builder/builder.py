"""
A utility class for building SSML format text.

@author: user3301
@date: 2018-02-06
Updated: 2025 for Python 3.11+
"""

import re
from typing import Self


class Speech:
    """Speech Synthesis Markup Language (SSML) builder with fluent interface."""

    def __init__(self) -> None:
        """Initialize Speech builder with empty content list."""
        self.content: list[str] = []

    def say(self, saying: str) -> Self:
        """
        Append raw text into the <speak/> tag.

        Args:
            saying: The raw text to insert into the speak tag.

        Returns:
            Self for method chaining.
        """
        self._present(saying, "The saying provided was null")
        self.content.append(self._escape(saying))
        return self

    def paragraph(self, paragraph: str) -> Self:
        """
        Insert a paragraph tag.

        Args:
            paragraph: The paragraph of text to insert.

        Returns:
            Self for method chaining.
        """
        self._present(paragraph, "The paragraph was null")
        self.content.append(f"<p>{self._escape(paragraph)}</p>")
        return self

    def sentence(self, saying: str) -> Self:
        """
        Insert a sentence tag.

        Args:
            saying: The sentence to insert.

        Returns:
            Self for method chaining.
        """
        self._present(saying, "The sentence was null")
        self.content.append(f"<s>{self._escape(saying)}</s>")
        return self

    def pause(self, duration: str) -> Self:
        """
        Insert a break tag.

        Args:
            duration: The duration for the pause (e.g., '1s', '500ms').

        Returns:
            Self for method chaining.
        """
        self._present(duration, "The duration was null")
        self._validate_duration(duration)
        self.content.append(f"<break time='{duration}'/>")
        return self

    def pauseByStrength(self, strength: str) -> Self:
        """
        Create break tag that will pause the audio based upon the strength level.

        Args:
            strength: The strength level (none, x-weak, weak, medium, strong, x-strong).

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If the strength value is not valid.
        """
        self._present(strength, "The strength was null")
        strength = strength.lower().strip()
        if strength in ("none", "x-weak", "weak", "medium", "strong", "x-strong"):
            self.content.append(f"<break strength='{strength}'/>")
            return self
        else:
            raise ValueError("The strength was not valid.")

    def spell(self, word: str) -> Self:
        """
        Insert a say-as spell-out tag.

        Args:
            word: The raw text to insert into the say-as tag.

        Returns:
            Self for method chaining.
        """
        self._present(word, "The word was null")
        self.content.append(f"<say-as interpret-as='spell-out'>{self._escape(word)}</say-as>")
        return self

    def spellSlowly(self, words: str, delay: str) -> Self:
        """
        Insert a say-as spell-out tag for every single character.

        Args:
            words: The raw text to spell out.
            delay: The interval between each character.

        Returns:
            Self for method chaining.
        """
        self._present(words, "The word was null")
        self._validate_duration(delay)
        for word in words:
            self.content.append(f"<say-as interpret-as='spell-out'>{self._escape(word)}</say-as>")
            self.pause(delay)
        return self

    # Amazon Effect tags

    def whispered(self, saying: str) -> Self:
        """
        Insert an Amazon 'whispered' effect tag.

        Args:
            saying: The raw text.

        Returns:
            Self for method chaining.
        """
        self._present(saying, "The saying is null")
        self.content.append(f"<amazon:effect name='whispered'>{self._escape(saying)}</amazon:effect>")
        return self

    def softPhonation(self, saying: str) -> Self:
        """
        Insert an Amazon 'soft phonation' effect tag.

        Args:
            saying: The raw text.

        Returns:
            Self for method chaining.
        """
        self._present(saying, "The saying is null")
        self.content.append(f"<amazon:effect phonation='soft'>{self._escape(saying)}</amazon:effect>")
        return self

    def drc(self, saying: str) -> Self:
        """
        Insert an Amazon 'dynamic range compression (drc)' effect tag.

        Enhances the volume of certain sounds in a conversation.

        Args:
            saying: The raw text.

        Returns:
            Self for method chaining.
        """
        self._present(saying, "The saying is null")
        self.content.append(f"<amazon:effect name='drc'>{self._escape(saying)}</amazon:effect>")
        return self

    def emphasis(self, saying: str, level: str) -> Self:
        """
        Insert an emphasis tag.

        Args:
            saying: The raw text.
            level: The degree of emphasis (strong, moderate, reduced).

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If the level type is invalid.
        """
        self._present(saying, "The saying is null")
        if level.lower() not in ["strong", "moderate", "reduced"]:
            raise ValueError("The level type is invalid")
        self.content.append(f"<emphasis level='{level}'>{self._escape(saying)}</emphasis>")
        return self

    def lang(self, saying: str, accent_type: str) -> Self:
        """
        Insert a language tag.

        Args:
            saying: The raw text.
            accent_type: The accent voice to use (e.g., 'en-US', 'fr-FR').

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If the language type is invalid.
        """
        lang_set = {
            "da-DK", "nl-NL", "en-AU", "en-GB", "en-IN", "en-US", "en-GB-WLS",
            "fr-FR", "fr-CA", "de-DE", "is-IS", "it-IT", "ja-JP", "ko-KR",
            "nb-NO", "pl-PL", "pt-BR", "pt-PT", "ro-RO", "ru-RU", "es-ES",
            "es-US", "sv-SE", "tr-TR", "cy-GB"
        }
        self._present(saying, "The saying is null")
        if accent_type not in lang_set:
            raise ValueError("The language type is invalid")
        self.content.append(f"<lang xml:lang='{accent_type}'>{self._escape(saying)}</lang>")
        return self

    def phoneme(self, word: str, alphabet: str, ph: list[str]) -> Self:
        """
        Insert a phonetic tag for the indicated text to provide phonetic pronunciation.

        Args:
            word: The indicated text.
            alphabet: Phoneme system used ('ipa' or 'x-sampa').
            ph: The phonetic symbols to be used for pronunciation.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If the alphabet standard or phonetic symbols are invalid.
        """
        self._present(word, "The word is null")

        if alphabet == "ipa":
            ipa_phonemes = {
                "b", "d", "d͡ʒ", "ð", "f", "g", "h", "j", "k", "l", "m", "n", "ŋ",
                "p", "ɹ", "s", "ʃ", "t", "t͡ʃ", "Θ", "v", "w", "z", "ʒ", "ə", "ɚ",
                "æ", "aɪ", "aʊ", "ɑ", "eɪ", "ɝ", "ɛ", "i:", "ɪ", "oʊ", "ɔ", "ɔɪ",
                "u", "ʊ", "ʌ", "'", ",", "."
            }
            if not set(ph).issubset(ipa_phonemes):
                raise ValueError("The phonetic symbols are invalid")
            ph_value = ''.join(ph)
            self.content.append(
                f"<phoneme alphabet='{alphabet}' ph='{ph_value}'>{self._escape(word)}</phoneme>"
            )
        elif alphabet == "x-sampa":
            xsampa_phonemes = {
                "b", "d", "dZ", "D", "f", "g", "h", "j", "k", "l", "m", "n", "N",
                "p", "r\\", "s", "S", "t", "tS", "T", "v", "w", "z", "Z", "@",
                "@'", "{", "aI", "aU", "A", "eI", "3'", "E", "i", "I", "oU", "O",
                "OI", "u", "U", "V", '"', "%", "."
            }
            if not set(ph).issubset(xsampa_phonemes):
                raise ValueError("The phonetic symbols are invalid")
            ph_value = ''.join(ph)
            self.content.append(
                f"<phoneme alphabet='{alphabet}' ph='{ph_value}'>{self._escape(word)}</phoneme>"
            )
        else:
            raise ValueError("The alphabet standard is invalid")

        return self

    def prosody(self, word: str, attributes: dict[str, str]) -> Self:
        """
        Insert a prosody tag (work in progress).

        Args:
            word: The word to apply prosody to.
            attributes: Prosody attributes (rate, pitch, volume).

        Returns:
            Self for method chaining.
        """
        self._present(word, "The word is null")
        # TODO: Implementation in progress
        return self

    @staticmethod
    def _escape(word: str | int | float | complex | bool) -> str | int | float | complex | bool:
        """
        Escape any special characters that will cause SSML to be invalid.

        Args:
            word: The word that needs to be examined.

        Returns:
            The escaped word string or original number/boolean.

        Raises:
            ValueError: If received invalid type.
        """
        if isinstance(word, str):
            word = word.replace('&', 'and')
            word = word.replace('<', '')
            word = word.replace('>', '')
            word = word.replace('"', '')
            word = word.replace("'", '')
            return word
        if isinstance(word, (int, float, complex, bool)):
            return word
        raise ValueError("Received invalid type")

    @staticmethod
    def _validate_duration(duration: str) -> None:
        """
        Check if the duration is in correct format and within valid range.

        Format: positive number followed by 's' or 'ms'
        Range: 0ms - 10000ms (0s - 10s)

        Args:
            duration: The duration of a pause.

        Raises:
            ValueError: When the duration format is incorrect or exceeds maximum length.
        """
        pattern = r"^(\d*\.?\d+)(s|ms)$"
        if match := re.match(pattern, duration):
            pause_duration = float(match.group(1))
            pause_type = match.group(2)
            if pause_type.lower() == 's' and pause_duration > 10:
                raise ValueError("The duration exceeds the maximum length.")
            elif pause_duration > 10000:
                raise ValueError("The duration exceeds the maximum length.")
        else:
            raise ValueError("The format of the duration is incorrect.")

    @staticmethod
    def _present(value: str | None, msg: str) -> None:
        """
        Validate that the provided value is not None.

        Args:
            value: The value to check.
            msg: The error message if value is None.

        Raises:
            ValueError: If value is None.
        """
        if value is None:
            raise ValueError(msg)

    def ssml(self, exclude_speak_tag: bool) -> str:
        """
        Construct an SSML format string.

        Args:
            exclude_speak_tag: Whether to exclude the root <speak/> tag.

        Returns:
            The SSML formatted string.
        """
        if exclude_speak_tag:
            return ' '.join(self.content)
        else:
            return '<speak>' + ' '.join(self.content) + '</speak>'

    def toXML(self) -> str:
        """
        Convert SSML format string into XML format.

        Returns:
            The XML formatted string.
        """
        xml = (
            "<?xml version='1.0'?>\n"
            "<speak version='1.1'\n"
            " xmlns='http://www.w3.org/2001/10/synthesis'\n"
            " xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'\n"
            " xsi:schemaLocation='http://www.w3.org/2001/10/synthesis "
            "http://www.w3.org/TR/speech-synthesis11/synthesis.xsd'\n"
            f" xml:lang='en-US'>{self.ssml(True)}</speak>"
        )
        return xml
