FROM python:3.11-alpine

RUN apt-get update && \
  apt-get install -y openjdk-17-jre wget curl && \
  apt-get clean

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
