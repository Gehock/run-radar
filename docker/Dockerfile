FROM apluslms/service-base:django-1.9

# Set container related configuration via environment variables
ENV CONTAINER_TYPE="radar" \
    RADAR_LOCAL_SETTINGS="/srv/radar-cont-settings.py" \
    RADAR_SECRET_KEY_FILE="/local/radar/secret_key.py"

ARG BRANCH=container
RUN : \
 && apt_install \
      curl \
      # python3-lxml \
      # python3-lz4 \
      # python3-pillow \
\
  # create user
 && adduser --system --no-create-home --disabled-password --gecos "A+ radar service,,," --home /srv/radar --ingroup nogroup radar \
\
 && :

COPY rootfs /
COPY radar /srv/radar
WORKDIR /srv/radar
RUN : \
 && chown radar.nogroup /srv/radar \
 && cd /srv/radar \
  # clone and prebuild .pyc files
#  && git clone --quiet --single-branch --branch $BRANCH https://github.com/gehock/radar.git . \
#  && (echo "On branch $(git rev-parse --abbrev-ref HEAD) | $(git describe)"; echo; git log -n5) > GIT \
 && rm -rf .git \
 && :
RUN : \
 && python3 -m compileall -q . \
\
 && :
RUN : \
  # install requirements, remove the file, remove unrequired locales and tests
 && pip_install -r requirements.txt \
 && rm requirements.txt \
 && :
RUN : \
 && find /usr/local/lib/python* -type d -regex '.*/locale/[a-z_A-Z]+' -not -regex '.*/\(en\|fi\|sv\)' -print0 | xargs -0 rm -rf \
 && find /usr/local/lib/python* -type d -name 'tests' -print0 | xargs -0 rm -rf \
 && :

# RUN mkdir -p /local/radar
RUN : \
  # preprocess
 && export \
    RADAR_SECRET_KEY="-" \
    RADAR_BASE_URL="-" \
    RADAR_CACHES="{\"default\": {\"BACKEND\": \"django.core.cache.backends.dummy.DummyCache\"}}" \
 && create-db.sh radar radar django-migrate.sh \
 && :


WORKDIR /srv/radar
RUN pip_install debugpy
RUN apt_install htop netcat vim curl wget less
# the pypi version doesn't support celery>=5
RUN pip_install git+https://github.com/mher/flower#egg=flower
# RUN apt_install memcached
EXPOSE 8001
EXPOSE 5555
RUN mkdir -p /var/celery/results \
 && chown radar:nogroup /var/celery/results
RUN mkdir -p /var/celery/results \
 && chown radar:nogroup /var/celery/results
# CMD [ "python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "manage.py", "runserver", "0.0.0.0:8001" ]
CMD [ "python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "manage.py", "runserver", "0.0.0.0:8001" ]
