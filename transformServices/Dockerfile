FROM alpine

RUN apk add --no-cache \
    python3 \
    bash \
    nginx \
    uwsgi \
    uwsgi-python3 \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache 

ENV PYTHONPATH "$PYTHONPATH:/app"


# Copy the Nginx global conf
COPY nginx.conf /etc/nginx/
# Copy the Flask Nginx site conf
COPY flask-site-nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Add app
COPY ./app /app

WORKDIR /app

RUN  pip3 install -r requirements.txt

CMD ["/usr/bin/supervisord"]
