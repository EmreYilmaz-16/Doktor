#!/bin/sh

set -e

echo "Migrasyon kontrol ediliyor..."
python manage.py migrate --noinput

echo "Statik dosyalar toplanıyor..."
python manage.py collectstatic --noinput

echo "Varsayılan admin kullanıcısı oluşturuluyor..."
python manage.py create_default_admin

echo "Uygulama başlatılıyor..."
exec "$@"
