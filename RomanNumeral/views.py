import re


class RomanConverter:
    """Convert standard Roman numerals in the range 1..3999."""

    ROMAN_NUMERALS = {
        "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000
    }
    ROMAN_NUMERAL_PATTERNS = (
        ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
        ("C", 100), ("XC", 90), ("L", 50), ("XL", 40),
        ("X", 10), ("IX", 9), ("V", 5), ("IV", 4), ("I", 1),
    )
    ROMAN_PATTERN = re.compile(
        r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    )

    @classmethod
    def is_valid_roman(cls, roman):
        if not isinstance(roman, str) or not roman:
            return False
        return cls.ROMAN_PATTERN.fullmatch(roman.strip().upper()) is not None and any(
            char in cls.ROMAN_NUMERALS for char in roman
        )

    @classmethod
    def roman_to_number(cls, roman_numeral):
        if not isinstance(roman_numeral, str):
            return None
        roman_numeral = roman_numeral.strip().upper()
        if not cls.is_valid_roman(roman_numeral):
            return None
        total = 0
        previous = 0
        for char in reversed(roman_numeral):
            value = cls.ROMAN_NUMERALS[char]
            total += -value if value < previous else value
            previous = max(previous, value)
        return total

    @classmethod
    def number_to_roman(cls, number):
        if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= 3999:
            return None
        result = []
        for numeral, value in cls.ROMAN_NUMERAL_PATTERNS:
            count, number = divmod(number, value)
            result.extend([numeral] * count)
        return "".join(result)


class RealConverter:
    """
    Convert the project's custom dotted notation, e.g. 25.25 <-> XXV.XXV.
    Each side is converted as an independent Roman numeral; this is not a
    standard Roman representation of decimal fractions.
    """

    def __init__(self):
        self.roman_converter = RomanConverter()

    def roman_real_to_real(self, value):
        if not isinstance(value, str):
            return None
        parts = value.strip().upper().split(".")
        if len(parts) > 2 or any(not part for part in parts):
            return None
        converted = [self.roman_converter.roman_to_number(part) for part in parts]
        if any(number is None for number in converted):
            return None
        return ".".join(str(number) for number in converted)

    def real_to_roman_real(self, value):
        text = str(value).strip()
        if not re.fullmatch(r"d+(?:.d+)?", text):
            return None
        parts = text.split(".")
        converted = []
        for part in parts:
            # A zero fractional component is represented by the integer part alone.
            number = int(part)
            if number == 0 and len(parts) == 2 and part == parts[-1]:
                return self.roman_converter.number_to_roman(int(parts[0]))
            roman = self.roman_converter.number_to_roman(number)
            if roman is None:
                return None
            converted.append(roman)
        return ".".join(converted)


from django.http import JsonResponse
from django.shortcuts import render
from .choices import DataTypeChoices
from .forms import DataInputForm


def index(request):
    return render(request, "index.html", {"form": DataInputForm()})


def converter(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido."}, status=405)

    form = DataInputForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"erro": "Informe um tipo de conversão e um valor válido."}, status=400)

    value = form.cleaned_data["value"]
    data_type = form.cleaned_data["data_type"]
    converter_service = RealConverter()

    if data_type == DataTypeChoices.TEXT:
        result = converter_service.roman_real_to_real(value)
    elif data_type == DataTypeChoices.FLOAT:
        result = converter_service.real_to_roman_real(value)
    else:
        result = None

    if result is None:
        return JsonResponse({"erro": "Entrada inválida. Confira o formato e os limites aceitos."}, status=400)

    return JsonResponse({"resultado": f"Valor convertido: {result}"})
