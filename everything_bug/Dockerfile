FROM python:3.10

COPY requirements.txt /cloud/requirements.txt

#RUN pip3 install uv

RUN pip install --no-cache-dir --upgrade -r /cloud/requirements.txt

COPY ./cloud /app

CMD [ "uvicorn", "app/main:app", "--host", "0.0.0.0", "--port", "8000"]
