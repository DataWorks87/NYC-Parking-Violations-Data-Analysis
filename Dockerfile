FROM python:3.9

WORKDIR /app

COPY . .

COPY src/ /main.py

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]