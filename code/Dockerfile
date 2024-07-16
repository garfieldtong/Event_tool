FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

#RUN pip3 install uv

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/ /code/app/

# Expose the port on which the application will run
# EXPOSE 8000

CMD ["fastapi", "run", "app/updated.py", "--host", "0.0.0.0"]
