FROM python:slim-buster

RUN pip install requests tabulate
RUN apt-get update && apt-get install -y fping

WORKDIR /home/

ADD nordvpn_best.py /home/nordvpn_best.py

ENTRYPOINT [ "python", "nordvpn_best.py" ]
