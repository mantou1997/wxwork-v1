FROM registry.gz.cvte.cn/infra/centos8-python-django:latest

COPY . .

EXPOSE 8000

RUN bash runtime/assemble
