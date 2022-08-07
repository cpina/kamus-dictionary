FROM debian:bullseye-slim
ENV PYTHONBUFFERED 1
RUN mkdir /code
COPY requirements.txt entrypoint.sh /code/

RUN apt-get update && apt-get install --no-install-recommends --yes \
	python3-pip libmariadb-dev

RUN pip3 install -r /code/requirements.txt
WORKDIR /code/kamus
ENTRYPOINT ["/code/entrypoint.sh"]

