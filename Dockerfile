FROM python:3.11-slim
WORKDIR /app
RUN pip install flask==2.3
COPY ./app.py /app
ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]