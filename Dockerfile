FROM python:3
RUN apt-get install -y openssl && \
apt-get update && \
apt-get install -y dnsutils && \
apt-get install -y net-tools
WORKDIR /usr/local/bin
COPY app.py .
CMD ["python","app.py"]