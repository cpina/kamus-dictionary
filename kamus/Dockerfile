FROM debian:bullseye-slim
ENV PYTHONBUFFERED 1
RUN mkdir /code

RUN apt-get -y update && apt-get -y dist-upgrade && \
	apt-get install --no-install-recommends --yes \
	python3-pip \
	libmariadb-dev libpython3-dev gcc \
	mariadb-client \
	curl bzip2
COPY requirements.txt /code/
RUN pip3 install -r /code/requirements.txt
RUN apt-get purge -y libmariadbclient-dev libmariadb-dev-compat \
	gcc libpython3-dev && \
   apt-get autoremove -y && \
   apt-get clean

COPY entrypoint.sh tools/wait-for-mysql.sh /code/

WORKDIR /code/kamus
ENTRYPOINT ["/code/entrypoint.sh"]

