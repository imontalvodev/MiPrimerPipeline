# MiPrimerPipeline

[![CI/CD](https://github.com/imontalvodev/MiPrimerPipeline/actions/workflows/main.yml/badge.svg)](https://github.com/imontalvodev/MiPrimerPipeline/actions/workflows/main.yml)

Pipeline de CI/CD con **GitHub Actions** para una pequeña aplicación Python que genera saludos. Práctica del módulo 2 del máster (DevOps). Parte de un primer pipeline en CircleCI y lo amplía con más pruebas, matriz de versiones de Python y despliegue de una imagen Docker.

## La aplicación

[saludar.py](saludar.py) ofrece tres funcionalidades:

| Función | Qué hace |
|---|---|
| `saludo1()`, `saludo2()`, `saludo3()` | Devuelven un saludo fijo |
| `saludar_segun_hora(hora)` | Saludo según la hora (0-23). Lanza `ValueError` fuera de rango |
| `saludar_segun_idioma(idioma)` | Saludo en `es`, `en`, `pt` o `hr`. Lanza `ValueError` si no está soportado |

Los tests están en [test_saludar.py](test_saludar.py) (pytest, parametrizados).

## Ejecución en local

Requiere Python 3.11 o superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python saludar.py        # ejecutar la app
pytest -v                # tests
pytest --cov=saludar --cov-report=term-missing --cov-fail-under=80   # tests con cobertura
flake8 --exclude=.venv --statistics                                  # estilo
bandit -r saludar.py                                                 # seguridad
```

## Pipeline

Definido en [.github/workflows/main.yml](.github/workflows/main.yml). Se dispara con `push` y `pull_request` hacia `main`.

```
lint ──────┐
matrix_tests ──┼──> docker   (solo push a main)
security ──┘
```

| Job | Qué comprueba | Herramienta |
|---|---|---|
| `lint` | Estilo y errores de sintaxis (PEP 8) | flake8 |
| `matrix_tests` | Tests en Python 3.11, 3.12, 3.13 y 3.14, con cobertura mínima del 80 % | pytest, pytest-cov |
| `security` | Patrones inseguros en el código (SAST) | bandit |
| `docker` | Construye y publica la imagen en Docker Hub | docker/build-push-action |

Decisiones de diseño:

- Los tres primeros jobs corren **en paralelo**. Solo `docker` espera a que todos pasen (`needs`).
- La **matriz** solo se aplica a los tests: lint y bandit analizan texto y su resultado no depende de la versión de Python.
- `docker` solo se ejecuta en un `push` a `main`. En un pull request se omite, así nunca se publica una imagen sin revisar.
- El bloque `if __name__ == "__main__"` se excluye de la cobertura con `# pragma: no cover`: es entrada interactiva, no lógica.
- El aviso `B311` de bandit (`random`) se marca con `# nosec B311`: aquí `random` solo elige un saludo y no tiene uso criptográfico.
- Caché de dependencias pip activada con `cache: pip` en `actions/setup-python`.

## Despliegue (CD) con Docker

La imagen se construye con el [Dockerfile](Dockerfile) (base `python:3.13-slim`) y se publica en Docker Hub:

```bash
docker pull imontalvodev/mi-primer-pipeline:latest
docker run -it imontalvodev/mi-primer-pipeline:latest
```

Se usa `-it` porque la aplicación pide datos por teclado.

### Secrets necesarios

En *Settings > Secrets and variables > Actions > Repository secrets*:

| Secret | Contenido |
|---|---|
| `DOCKER_LOGIN` | Usuario de Docker Hub |
| `DOCKER_PWD` | Access token de Docker Hub con permisos de lectura y escritura |

## Estructura

```
.
├── .github/workflows/main.yml   # pipeline de GitHub Actions
├── circleci/config.yml          # pipeline original de CircleCI (referencia)
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── saludar.py
└── test_saludar.py
```
