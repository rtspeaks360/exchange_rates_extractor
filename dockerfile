FROM python:3

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /usr/src/app

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

ENTRYPOINT ["python"]
CMD ["main.py", "--run_as", "dashboard"]