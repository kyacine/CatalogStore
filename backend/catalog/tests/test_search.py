from django.test import TestCase

from catalog.views import strip_accents


class StripAccentsTests(TestCase):
    def test_removes_accents(self):
        self.assertEqual(strip_accents("Détergent"), "detergent")

    def test_is_case_insensitive(self):
        self.assertEqual(strip_accents("ENCENS"), "encens")

    def test_handles_text_without_accents(self):
        self.assertEqual(strip_accents("savon"), "savon")

    def test_handles_empty_string(self):
        self.assertEqual(strip_accents(""), "")