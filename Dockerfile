FROM python:3.7

ARG pypi_host=pypi.douban.com
ARG pypi_mirror=http://pypi.douban.com/simple

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PIP_INDEX_URL $pypi_mirror

RUN apt-get update

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --trusted-host ${pypi_host}

COPY app app
COPY migrations migrations
COPY runner.py runner.py
COPY start_server.sh start_server.sh

RUN chmod a+x start_server.sh

EXPOSE 5000
ENTRYPOINT [ "./start_server.sh" ]