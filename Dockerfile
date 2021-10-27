FROM python:3.8.12
COPY requirements.txt /app/requirements.txt
COPY src /app/src
COPY data /app/data
COPY setup.py /app
COPY gunicorn.sh /app
RUN pip3 install -r /app/requirements.txt
WORKDIR /app
RUN pip install -e .
EXPOSE 5000
ENTRYPOINT ["./gunicorn.sh"]
#CMD ["gunicorn","-b","0.0.0.0:5000", "urlsafe:app"]
