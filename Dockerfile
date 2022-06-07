FROM python:3.9-slim

RUN apt install sqlite3

CMD ["echo", "python-sdk"]