# Use the official PHP image with Apache
FROM php:8.2-apache

# Set local language to UTF-8
RUN apt-get update && apt-get install -y locales && locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

# Configure Apache
RUN echo "AddDefaultCharset UTF-8" >> /etc/apache2/conf-enabled/charset.conf

# Set the working directory to the Apache default root
WORKDIR /var/www/html

# Copy the PHP script
COPY index.php .

# Expose port 80
EXPOSE 80
