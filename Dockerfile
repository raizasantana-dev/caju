FROM python:3.13

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --root-user-action=ignore --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]