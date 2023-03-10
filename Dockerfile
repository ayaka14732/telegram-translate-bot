FROM archlinux:latest
RUN pacman -Syu --noconfirm gcc python python-pip python-wheel && pacman -Sc --noconfirm && useradd -m appuser
USER appuser
WORKDIR /home/appuser/app
COPY . .
RUN pip install --user setuptools
RUN pip install --user -r requirements.txt
CMD [ "python", "main.py" ]
