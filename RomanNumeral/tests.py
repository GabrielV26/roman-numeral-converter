from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .views import RomanConverter, RealConverter


class RomanConverterTests(SimpleTestCase):
    def test_converts_roman_to_number(self):
        cases = {"I": 1, "IV": 4, "IX": 9, "XLII": 42, "MCMXCIV": 1994, "MMMCMXCIX": 3999}
        for roman, expected in cases.items():
            with self.subTest(roman=roman):
                self.assertEqual(RomanConverter.roman_to_number(roman), expected)

    def test_accepts_lowercase_and_surrounding_whitespace(self):
        self.assertEqual(RomanConverter.roman_to_number("  xiv "), 14)

    def test_rejects_noncanonical_or_out_of_range_roman(self):
        for roman in ("", "IIII", "IC", "MMMM", "ABC", "VX", "I I"):
            with self.subTest(roman=roman):
                self.assertIsNone(RomanConverter.roman_to_number(roman))

    def test_converts_number_to_roman(self):
        self.assertEqual(RomanConverter.number_to_roman(2024), "MMXXIV")

    def test_rejects_invalid_integer_values(self):
        for value in (0, -1, 4000, 2.5, True, "12"):
            with self.subTest(value=value):
                self.assertIsNone(RomanConverter.number_to_roman(value))


class RealConverterTests(SimpleTestCase):
    def setUp(self):
        self.converter = RealConverter()

    def test_custom_dotted_conversion(self):
        self.assertEqual(self.converter.real_to_roman_real("25.25"), "XXV.XXV")
        self.assertEqual(self.converter.roman_real_to_real("XXV.XXV"), "25.25")

    def test_integer_and_zero_fraction_conversion(self):
        self.assertEqual(self.converter.real_to_roman_real("25.0"), "XXV")
        self.assertEqual(self.converter.roman_real_to_real("XXV"), "25")

    def test_rejects_invalid_inputs(self):
        for value in ("0", "-2", "4000", "1.4000", "1..2", "XX.0", "1,2", ""):
            with self.subTest(value=value):
                self.assertIsNone(self.converter.real_to_roman_real(value))
        for value in ("IC", "XX.", ".X", "X.Y", "I.IV.II", ""):
            with self.subTest(value=value):
                self.assertIsNone(self.converter.roman_real_to_real(value))


class ConverterViewTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_rejects_get_on_conversion_endpoint(self):
        response = self.client.get(reverse("converter"))
        self.assertEqual(response.status_code, 405)

    def test_rejects_invalid_post(self):
        response = self.client.post(reverse("converter"), {"data_type": "T", "value": "IIII"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("erro", response.json())

    def test_converts_valid_roman_post(self):
        response = self.client.post(reverse("converter"), {"data_type": "T", "value": "XIV"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resultado"], "Valor convertido: 14")

    def test_converts_valid_number_post(self):
        response = self.client.post(reverse("converter"), {"data_type": "F", "value": "14"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resultado"], "Valor convertido: XIV")
