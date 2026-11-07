FROM python:3.13-slim

WORKDIR /myfirstpipeline

COPY saludar.py .

CMD [ "python", "saludar.py" ]

