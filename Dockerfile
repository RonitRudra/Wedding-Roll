FROM python:3.6
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install -r /config/requirements.txt
ADD ./code/

