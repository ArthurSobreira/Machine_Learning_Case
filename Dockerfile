FROM python:3.11-slim

RUN apt-get update && \
  apt-get install -y openjdk-17-jre wget curl gcc g++ make && \
  apt-get clean 

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
