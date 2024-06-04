FROM python:3.12.3-bookworm
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt