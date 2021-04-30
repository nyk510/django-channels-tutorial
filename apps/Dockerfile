FROM python:3

ARG USER_NAME=django
ARG USER_PASSWORD=hogehoge
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN groupadd -g 1000 developer &&\
  useradd -g developer -G sudo -m -s /bin/bash ${USER_NAME} &&\
  echo "${USER_NAME}:${USER_PASSWORD}" | chpasswd

WORKDIR /var/www/django
RUN chown -R django /var/www/django
USER ${USER_NAME}
ADD ./requirements.txt /var/www/django/requirements.txt
ENV VENV_PATH=/home/django/django-venv

RUN python -m venv ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:${PATH}"
RUN pip install -U pip &&\
  pip install -U -r requirements.txt
