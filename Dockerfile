FROM python:slim-buster

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y fping

WORKDIR /home/
COPY nordvpn_best.py /home/nordvpn_best.py
ENTRYPOINT [ "python", "nordvpn_best.py" ]
