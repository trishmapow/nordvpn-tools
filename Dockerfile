FROM python:slim-buster

RUN pip install requests tabulate

WORKDIR /home/

ADD nordvpn_best.py /home/nordvpn_best.py

ENTRYPOINT [ "python", "nordvpn_best.py" ]
