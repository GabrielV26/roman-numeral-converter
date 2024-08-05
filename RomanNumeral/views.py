from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import DataInput
from .forms import DataInputForm
from .choices import DataTypeChoices
import requests
import json
import re


def index(request):
    form = DataInputForm()
    return render(request, 'index.html', {'form': form})


# Expressão regular para que aceita apenas números romanos
def is_valid_roman(roman):
    pattern = r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    return re.match(pattern, roman) is not None


# Converte numero romano para inteiro
def number_for_roman(roman_numeral):
    add_values = 0
    rem_values = 0
    old_value = 0

    roman_numbers = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    if is_valid_roman(roman_numeral.upper()):
        letter = reversed(list(roman_numeral))

        for char in letter:
            value = roman_numbers[char.upper()]

            if value > add_values or value == old_value:
                old_value = value
                add_values = add_values + value
            elif value < add_values:
                rem_values = rem_values + value

        roman_numeral = add_values - rem_values
        return roman_numeral


# Converte "real romano" para real
def number_for_roman_real(value_for_converted):
    result = ''
    if isinstance(value_for_converted, str):
        try:
            parte1, parte2 = value_for_converted.split(',', 1)
            result = 'R$' + str(number_for_roman(parte1)) + '.' + str(number_for_roman(parte2))
        except ValueError:
            result = 'R$' + str(number_for_roman(value_for_converted))

    return result


# Converte de inteiro para romano
def roman_for_number(number):
    roman_numbers = [
        ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40),
        ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1)
    ]

    roman_string = ""
    for numeral, value in roman_numbers:
        while number >= value:
            roman_string += numeral
            number -= value

    return roman_string


# Converte o numero "real romano" para numero real
def roman_for_number_real(value_for_converted):
    result = ''
    if isinstance(value_for_converted, float):
        text_convert = str(value_for_converted)
        parte1, parte2 = text_convert.split('.', 1)
        result = str(roman_for_number(int(parte1))) + '.' + str(roman_for_number(int(parte2)))
    else:
        roman_for_number(value_for_converted)
    return result


# View do formulário
def converter(request):
    if request.method == 'POST':
        form = DataInputForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            if isinstance(value, str):
                value = number_for_roman_real(value)
            else:
                value = roman_for_number_real(value)
            resultado = f"Valor convertido: {value}"
            return JsonResponse({'resultado': resultado})
        return JsonResponse({'erro': 'Dados inválidos.'}, status=400)
    return JsonResponse({'erro': 'Método não permitido.'}, status=405)

