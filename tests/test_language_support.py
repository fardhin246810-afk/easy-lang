import unittest

from language_support import (
    detect_nllb_language,
    get_language_labels,
    get_supported_language_codes,
)


class TokenizerStub:
    def get_vocab(self):
        return {
            "eng_Latn": 0,
            "hin_Deva": 1,
            "fra_Latn": 2,
            "ordinary_token": 3,
        }


class LanguageSupportTests(unittest.TestCase):
    def setUp(self):
        self.codes = get_supported_language_codes(TokenizerStub())

    def test_extracts_supported_language_codes(self):
        self.assertEqual(self.codes, ("eng_Latn", "fra_Latn", "hin_Deva"))

    def test_labels_include_language_and_script(self):
        labels = get_language_labels(self.codes)
        self.assertEqual(labels["eng_Latn"], "English (Latin, eng_Latn)")
        self.assertEqual(labels["hin_Deva"], "Hindi (Devanagari, hin_Deva)")

    def test_auto_detects_supported_languages(self):
        examples = (
            ("Good morning, how are you today?", "eng_Latn"),
            ("नमस्ते, आप कैसे हैं?", "hin_Deva"),
            ("Bonjour, comment allez-vous aujourd’hui?", "fra_Latn"),
        )
        for text, expected_code in examples:
            with self.subTest(expected_code=expected_code):
                self.assertEqual(detect_nllb_language(text, self.codes), expected_code)

    def test_short_text_requests_manual_language_selection(self):
        self.assertIsNone(detect_nllb_language("Hi", self.codes))


if __name__ == "__main__":
    unittest.main()
