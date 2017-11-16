# https://www.debian.org/releases/jessie/
FROM python:3.6.3-jessie

MAINTAINER Nikola Rankovic <kibernick@gmail.com>

# Install uWSGI
RUN pip install uwsgi

# Set up Nginx (+ utilities)
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y nginx vim supervisor mysql-client
# Make NGINX run in the foreground, otherwise the Docker build will fail!
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY deploy/nginx-app.conf /etc/nginx/sites-available/default
COPY deploy/supervisor-app.conf /etc/supervisor/conf.d/
# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
# Finished setting up Nginx

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
COPY requirements.txt /app/code/
RUN pip install -r /app/code/requirements.txt
COPY . /app/code/

EXPOSE 80 443 3306
CMD ["supervisord", "-n"]
