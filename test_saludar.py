import pytest

import saludar


class TestSaludar:

    def test_saludo1(self):
        assert "Hola" == saludar.saludo1()

    def test_saludo2(self):
        assert "Buenos días" == saludar.saludo2()

    def test_saludo3(self):
        assert "Hola, ¿Qué tal?" == saludar.saludo3()


class TestSaludarSegunHora:

    @pytest.mark.parametrize("hora, esperado", [
        (0, "Buenos dias"),
        (6, "Buenos dias"),
        (12, "Buenos dias"),
        (13, "Buenas tardes"),
        (18, "Buenas tardes"),
        (20, "Buenas tardes"),
        (21, "Buenas noches"),
        (23, "Buenas noches"),
    ])
    def test_saludo_segun_hora(self, hora, esperado):
        assert esperado == saludar.saludar_segun_hora(hora)

    @pytest.mark.parametrize("hora", [-1, 24, 100])
    def test_hora_fuera_de_rango(self, hora):
        mensaje = "La hora debe ser entre las 0 y 23"
        with pytest.raises(ValueError, match=mensaje):
            saludar.saludar_segun_hora(hora)


class TestSaludarSegunIdioma:

    @pytest.mark.parametrize("idioma, esperado", [
        ("es", "Hola"),
        ("en", "Hello"),
        ("pt", "Oi"),
        ("hr", "Bok bok"),
    ])
    def test_saludo_segun_idioma(self, idioma, esperado):
        assert esperado == saludar.saludar_segun_idioma(idioma)

    @pytest.mark.parametrize("idioma", ["fr", "", "ES"])
    def test_idioma_no_soportado(self, idioma):
        with pytest.raises(ValueError, match="Idioma no soportado"):
            saludar.saludar_segun_idioma(idioma)
