FROM debian:bullseye-slim
ENV PYTHONBUFFERED 1
RUN mkdir /code
COPY requirements.txt entrypoint.sh tools/wait-for-mysql.sh /code/

RUN apt-get update && apt-get install --no-install-recommends --yes \
	python3-pip \
	libmariadbclient-dev libmariadb-dev-compat libmariadb3 mariadb-client \
	gcc-7 gcc
RUN pip3 install -r /code/requirements.txt
RUN apt-get purge -y libmariadbclient-dev libmariadb-dev-compat \
	gcc-7 gcc libpython3.7-dev && \
   apt-get autoremove -y && \
   apt-get clean
WORKDIR /code/kamus
ENTRYPOINT ["/code/entrypoint.sh"]

