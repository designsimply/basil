FROM python:3

WORKDIR /opt/app
COPY . .

ENV PYTHONUNBUFFERED 1

# Install python packages
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip freeze

ENV PYTHONPATH '/opt/app/modules:/usr/local/lib/python3.7/site-packages'