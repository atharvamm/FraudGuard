FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y gcc libc6-dev

RUN mkdir fraud

WORKDIR /fraud

COPY . /fraud

RUN pip install --no-cache-dir -r /fraud/deps/requirements.txt

RUN rm -rf fraud/deps

CMD ["python", "run.py"]
