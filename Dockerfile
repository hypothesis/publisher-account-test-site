FROM gliderlabs/alpine:3.4
MAINTAINER Hypothes.is Project and contributors

# Install system build and runtime dependencies.
RUN apk-install ca-certificates curl python py-pip

# Create the bouncer user, group, home directory and package directory.
RUN addgroup -S publisher \
  && adduser -S -G publisher -h /var/lib/publisher publisher
WORKDIR /var/lib/publisher

# Install dependencies
COPY . .
RUN pip install --no-cache-dir -U pip \
  && pip install --no-cache-dir -r requirements.txt

# Start the web server
USER publisher
ENV FLASK_APP app.py
CMD flask run --port $PORT --host 0.0.0.0
