FROM debian:bullseye-slim
ENV PYTHONBUFFERED 1
RUN mkdir /code
COPY requirements.txt entrypoint.sh tools/wait-for-mysql.sh /code/

RUN apt-get update && apt-get install --no-install-recommends --yes \
	python3-pip \
	libmariadb-dev libpython3-dev gcc \
	mariadb-client # to check if mariadb server is available \
	curl bzip2
RUN pip3 install -r /code/requirements.txt
RUN apt-get purge -y libmariadbclient-dev libmariadb-dev-compat \
	gcc libpython3-dev && \
   apt-get autoremove -y && \
   apt-get clean
WORKDIR /code/kamus
ENTRYPOINT ["/code/entrypoint.sh"]

