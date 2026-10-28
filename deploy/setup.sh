#!/usr/bin/env bash
set -euo pipefail
cd /srv/funmig

echo "==> swap + packages"
if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  echo "/swapfile none swap sw 0 0" >> /etc/fstab
fi
echo "https://repo.hmirror.ir/debian" > /etc/apt/mirrors/debian.list
cat > /etc/pip.conf <<PIP
[global]
index-url = https://package-mirror.liara.ir/repository/pypi/simple
extra-index-url = https://mirror-pypi.runflare.com/simple
timeout = 60
retries = 10
PIP
export DEBIAN_FRONTEND=noninteractive
apt-get update
for pk in rsync sqlite3 curl nginx python3.13-venv python3-venv; do
  systemd-run --wait --pipe --quiet -p MemoryMax=2G -p MemorySwapMax=0 -E DEBIAN_FRONTEND=noninteractive apt-get install -y -q "$pk"
done

echo "==> funmig (funmig.com / social.funmig.com)"
cd /srv/funmig/funmig
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt
set -a; . ./.env; set +a
.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput

echo "==> FUNMIGAI (ai.funmig.com)"
cd /srv/funmig/FUNMIGAI
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt gunicorn
.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput

echo "==> mirror (mirror.funmig.com)"
mkdir -p /srv/mirror-data/repositories
cd /srv/funmig/mirror
if [ ! -f .env ]; then
  cat > .env <<ENV
MIRROR_DOMAIN=mirror.funmig.com
DJANGO_ALLOWED_HOSTS=mirror.funmig.com,localhost,127.0.0.1
DJANGO_SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_urlsafe(50))')
DJANGO_DEBUG=false
MIRROR_STORAGE_ROOT=/srv/mirror-data
MIRROR_REPOSITORY_ROOT=/srv/mirror-data/repositories
GIT_REPOSITORY_ROOT=/srv/mirror-data/git
TOTAL_STORAGE_LIMIT_GB=180
PYPI_STORAGE_LIMIT_GB=100
NPM_STORAGE_LIMIT_GB=60
TEMP_STORAGE_LIMIT_GB=10
MIN_FREE_DISK_GB=20
PYPI_UPSTREAM=https://pypi.org
UPSTREAM_MODE=auto
ENV
  chmod 600 .env
fi
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt packaging
set -a; . ./.env; set +a
.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput

echo "==> permissions"
mkdir -p /var/www/.gunicorn
chown -R www-data:www-data /srv/funmig /srv/mirror-data /var/www/.gunicorn

echo "==> systemd services"
cp /srv/funmig/deploy/*.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now funmig funmigai funmig-mirror
systemctl restart funmig funmigai funmig-mirror

echo "==> nginx"
cp /srv/funmig/deploy/funmig.nginx /etc/nginx/sites-available/funmig
ln -sf /etc/nginx/sites-available/funmig /etc/nginx/sites-enabled/funmig
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl enable nginx
systemctl reload nginx || systemctl restart nginx

sleep 3
echo "==> test"
for h in funmig.com social.funmig.com prof.funmig.com ai.funmig.com mirror.funmig.com; do
  printf "%-22s %s\n" "$h" "$(curl -s -o /dev/null -w '%{http_code}' -H "Host: $h" -H 'X-Forwarded-Proto: https' http://127.0.0.1/)"
done
systemctl --no-pager --lines=0 status funmig funmigai funmig-mirror nginx | grep -E "●|Active"
echo "DONE"
