FROM php:8.1-apache

# Installation des extensions MySQL
RUN docker-php-ext-install pdo pdo_mysql

# Activation de mod_rewrite pour Apache
RUN a2enmod rewrite

# Copie des fichiers de l'application
COPY src/ /var/www/html/

# Droits sur le dossier
RUN chown -R www-data:www-data /var/www/html

