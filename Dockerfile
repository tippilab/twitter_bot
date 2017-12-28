FROM python:3

ADD twitterbot.py /
ADD requirements.txt /
RUN pip install -r requirements.txt

CMD [ "python", "./twitterbot.py" ]