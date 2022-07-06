FROM python:3.7.9
LABEL maintainer "Miller <miller.puentes@gmail.com>"
WORKDIR /code
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ ./
ENV dash_port=80
ENV dash_debug="False"
EXPOSE 80
CMD ["python", "app.py"]