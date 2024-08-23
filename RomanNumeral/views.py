from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import DataInput
from .forms import DataInputForm
from .choices import DataTypeChoices
import requests
import json
import re


class RomanConverter:
    ROMAN_NUMERALS = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }

    ROMAN_NUMERAL_PATTERNS = [
        ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90),
        ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1)
    ]

    @staticmethod
    def is_valid_roman(roman):
        # Padrão para validar números romanos até 3999
        pattern = r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
        return re.match(pattern, roman) is not None

    def roman_to_number(self, roman_numeral):
        if not self.is_valid_roman(roman_numeral.upper()):
            return None

        add_values = 0
        rem_values = 0
        old_value = 0

        for char in reversed(roman_numeral):
            value = self.ROMAN_NUMERALS[char.upper()]

            if value > add_values or value == old_value:
                old_value = value
                add_values += value
            elif value < add_values:
                rem_values += value

        return add_values - rem_values

    def number_to_roman(self, number):
        if number <= -1 or number > 3999:
            return None

        roman_string = ""
        for numeral, value in self.ROMAN_NUMERAL_PATTERNS:
            while number >= value:
                roman_string += numeral
                number -= value

        return roman_string


class RealConverter:
    def __init__(self):
        self.roman_converter = RomanConverter()

    def roman_real_to_real(self, value_for_converted):
        if isinstance(value_for_converted, str):
            try:
                parte1, parte2 = value_for_converted.split('.', 1)
                num_part1 = self.roman_converter.roman_to_number(parte1)
                num_part2 = self.roman_converter.roman_to_number(parte2)
                if num_part1 is None or num_part2 is None:
                    return None
                return f"{num_part1}.{num_part2}"
            except ValueError:
                return f"{self.roman_converter.roman_to_number(value_for_converted)}"
        return None

    def real_to_roman_real(self, value_for_converted):
        if value_for_converted <= 0:
            return None
        if isinstance(value_for_converted, float):
            text_convert = str(value_for_converted)
            parte1, parte2 = text_convert.split('.', 1)
            if parte2 == '0':
                return f"{self.roman_converter.number_to_roman(int(parte1))}"
            else:
                return f"{self.roman_converter.number_to_roman(int(parte1))}.{self.roman_converter.number_to_roman(int(parte2))}"
        else:
            return self.roman_converter.number_to_roman(value_for_converted)


def index(request):
    form = DataInputForm()
    return render(request, 'index.html', {'form': form})


def converter(request):
    if request.method == 'POST':
        form = DataInputForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            print(value)
            real_converter = RealConverter()
            if isinstance(value, str):
                value = real_converter.roman_real_to_real(value)
            else:
                value = real_converter.real_to_roman_real(value)
            if value is None or value == "None":
                return JsonResponse({'erro': 'Entrada inválida.'}, status=400)
            return JsonResponse({'resultado': f"Valor convertido: {value}"})
        return JsonResponse({'erro': 'Dados inválidos.'}, status=400)
    return JsonResponse({'erro': 'Método não permitido.'}, status=405)
