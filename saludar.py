import random

SALUDOS = {"es": "Hola", "en": "Hello", "pt": "Oi", "hr": "Bok bok"}


def saludo1():
    return "Hola"


def saludo2():
    return "Buenos días"


def saludo3():
    return "Hola, ¿Qué tal?"


def saludar_segun_hora(hora: int) -> str:
    saludo = ""
    if not 0 <= hora <= 23:
        raise ValueError("La hora debe ser entre las 0 y 23")
    if hora <= 12:
        saludo = "Buenos dias"
    if hora >= 13 and hora <= 20:
        saludo = "Buenas tardes"
    if hora >= 21:
        saludo = "Buenas noches"
    return saludo


def saludar_segun_idioma(idioma: str) -> str:
    if idioma not in SALUDOS:
        raise ValueError("Idioma no soportado")
    return SALUDOS[idioma]


if __name__ == "__main__":
    saludo = random.randint(0, 2)

    if saludo == 0:
        print(saludo1())
    elif saludo == 1:
        print(saludo2())
    elif saludo == 2:
        print(saludo3())
    else:
        print("Adios")

    hora = int(input("Ingrese hora (0-23): "))
    try:
        print(saludar_segun_hora(hora))
    except ValueError as e:
        print(e)

    try:
        idioma = input("Ingrese idioma (es, en, pt, hr): ")
        print(saludar_segun_idioma(idioma))
    except ValueError as e:
        print(e)
