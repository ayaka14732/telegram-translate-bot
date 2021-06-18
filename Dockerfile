FROM python:3.9-buster
RUN useradd -m trans
USER trans
WORKDIR /home/trans/app
COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt
COPY . .
CMD [ "python", "main.py" ]
