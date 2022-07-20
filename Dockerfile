FROM python:3.10-slim-buster
RUN useradd -m app
USER app
WORKDIR /home/app/app
COPY . .
RUN pip install --user -r requirements.txt
CMD [ "python", "main.py" ]
