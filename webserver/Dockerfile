FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/webserver:/opt/webserver/apps:/usr/local/lib/python3.7/site-packages'

WORKDIR /opt/webserver

RUN pip install -U pip
COPY requirements.txt .
COPY requirements_freeze.txt .

# # for dev environment
# RUN pip install -r requirements.txt
# RUN pip freeze
# RUN pip freeze > /tmp/updated_requirements_freeze.txt
# RUN diff /tmp/updated_requirements_freeze.txt requirements_freeze.txt

# for stage & prod environment
RUN pip install -r requirements_freeze.txt

COPY . .
