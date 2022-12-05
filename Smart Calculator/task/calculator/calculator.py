# write your code here
import re
import ast

from collections import defaultdict
all_vars = {}

def geef_nummer(nr: str) -> int:
    nr = str(nr)
    nr = nr.strip()
    nr = re.sub(r'\.0+$', '', nr)

    try:
        return all_vars[nr]
    except KeyError:
        return int(nr)

def oplossing(number1, teken, number2):

    if teken[0] in ["-", "+"]:
        if teken.count("-") % 2 == 0:
            teken = "+"
        else:
            teken = "-"

    if teken == "+":
        return geef_nummer(number1) + geef_nummer(number2)
    elif teken == "-":
        return geef_nummer(number1) - geef_nummer(number2)
    elif teken == "++":
        return geef_nummer(number1) ++ geef_nummer(number2)
    elif teken == "*":
        return geef_nummer(number1) * geef_nummer(number2)
    elif teken == "**":
        return geef_nummer(number1) ** geef_nummer(number2)
    elif teken == "/":
        return geef_nummer(number1) / geef_nummer(number2)
    else:
        raise InvalidExpression


def sort(numbers):
    lijst = []

    for number in numbers:
        if number.isalpha():
            lijst.append(number)

    return lijst

class NotAssignment(Exception):
    pass


def interpret_assignment():
    numbers_split = [x.strip() for x in numbers.split('=')]
    if len(numbers_split) == 1:
        raise NotAssignment

    if len(numbers_split) > 2:
        raise ValueError("Invalid assignment")

    if not numbers_split[1].isdigit() and numbers_split[1] not in all_vars:
        raise ValueError("Invalid assignment")

    if not numbers_split[0].isalpha():
        raise ValueError("Invalid identifier")

    try:
        all_vars[numbers_split[0]] = int(numbers_split[1])
    except ValueError:
        if numbers_split[1] not in all_vars:
            raise ValueError("Unknown variable")

        all_vars[numbers_split[0]] = all_vars[numbers_split[1]]


class NotSom(Exception):
    pass


class InvalidExpression(Exception):
    pass


def num_str_veranderen(num_str):
    haakjes = re.findall(r'\(([^()]+)\)', num_str)
    for haakje in haakjes:
        opplosen = str(interpret_som(haakje))

        num_str = num_str.replace("(" + haakje + ")", opplosen)

    return num_str


def interpret_som(num_str):
    if len(num_str) < 3:
        raise NotSom

    while num_str.find("(") != -1 and num_str.find(")") != -1:
        num_str = num_str_veranderen(num_str)

    if num_str.find("(") != -1 or num_str.find(")") != -1:
        raise InvalidExpression



    numbers = re.split(r'([-+*/^]+)', num_str)

    # return eval(num_str)

    lijst = []

    while True:
        if "*" not in numbers:
            break

        sterretje_plaats = numbers.index("*")
        rest_voor = numbers[sterretje_plaats-1]
        rest_achter = numbers[sterretje_plaats+1]

        result = oplossing(rest_voor, "*", rest_achter)
        numbers = numbers[:sterretje_plaats-1] + [result] + numbers[sterretje_plaats+2:]

    while True:
        if "/" not in numbers:
            break

        sterretje_plaats = numbers.index("/")
        rest_voor = numbers[sterretje_plaats-1]
        rest_achter = numbers[sterretje_plaats+1]

        result = oplossing(rest_voor, "/", rest_achter)
        numbers = numbers[:sterretje_plaats-1] + [result] + numbers[sterretje_plaats+2:]


    while len(numbers) != 1:
        eerste = numbers[:3]
        rest = numbers[3:]
        result = oplossing(*eerste)
        numbers = [result] + rest

    try:
        return int(numbers[0])
    except ValueError:
        raise NotSom


while True:
    numbers = input().strip()

    if len(numbers) == 0:
        continue

    if numbers == "/exit":
        print("Bye!")
        break

    if numbers == "/help":
        print("The program calculates the sum of numbers")
        continue

    if numbers.startswith("/"):
        print("Unknown command")
        continue

    try:
        interpret_assignment()
    except NotAssignment:
        try:
            print(interpret_som(numbers))
        except NotSom:
            if numbers in all_vars:
                print(all_vars[numbers])
            else:
                print("Unknown variable")
        except InvalidExpression:
            print("Invalid expression")
            continue

    except ValueError as ex:
        print(ex)
        continue

