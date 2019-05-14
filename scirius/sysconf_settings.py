"""
Override settings for scirius project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

SHAREDSTATE_DIR = '/var/lib/scirius/'
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/scirius/'

GIT_SOURCES_BASE_DIRECTORY = os.path.join(SHAREDSTATE_DIR, 'git-sources')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p8o5%vq))8h2li08c%k3id(wwo*u(^dbdmx2tv#t(tb2pr9@n-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SHAREDSTATE_DIR, 'db.sqlite3'),
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Suricata binary
SURICATA_BINARY = "suricata"

SURICATA_NAME_IS_HOSTNAME = False

# Do we have the doc
SCIRIUS_HAS_DOC = True

# Sources update
DEFAULT_SOURCE_INDEX_URL = "https://www.openinfosecfoundation.org/rules/index.yaml"

# Elastic search

USE_ELASTICSEARCH = True
#ELASTICSEARCH_ADDRESS = "127.0.0.1:9200"
ELASTICSEARCH_ADDRESS = "localhost:9200"
# You can use a star to avoid timestamping expansion for example 'logstash-*'
ELASTICSEARCH_LOGSTASH_INDEX = "logstash-"
# You can change following value if you have different indexes for stats and alerts
ELASTICSEARCH_LOGSTASH_ALERT_INDEX = ELASTICSEARCH_LOGSTASH_INDEX
# use hourly, daily to indicate the logstash index building recurrence
ELASTICSEARCH_LOGSTASH_TIMESTAMPING = "daily"
# Extension used for complete field (usually "raw" or "keyword")
ELASTICSEARCH_KEYWORD = "raw"
# Hostname field (usually "hostname" or "host")
ELASTICSEARCH_HOSTNAME = "host"

# Kibana
USE_KIBANA = False
# Use django as a reverse proxy for kibana request
# This will allow you to use scirius authentication to control
# access to Kibana
KIBANA_PROXY = False
# Kibana URL
KIBANA_URL = "http://localhost:9292"
# Kibana index name
KIBANA_INDEX = "kibana-int"
# Number of dashboards to display
KIBANA_DASHBOARDS_COUNT = 20
# Path to Kibana's dashboards installation
KIBANA_DASHBOARDS_PATH = '/opt/kibana-dashboards/'
KIBANA6_DASHBOARDS_PATH = '/opt/kibana6-dashboards/'

USE_EVEBOX = False
EVEBOX_ADDRESS = "evebox:5636"

# Suricata is configured to write stats to EVE
USE_SURICATA_STATS = True
# Logstash is generating metrics on eve events
USE_LOGSTASH_STATS = True

# Set value to path to suricata unix socket to use suricatasc
# based info
SURICATA_UNIX_SOCKET = None
# SURICATA_UNIX_SOCKET = "/var/run/suricata/suricata-command.socket"

# Influxdb
USE_INFLUXDB = False
INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_USER = "grafana"
INFLUXDB_PASSWORD = "grafana"
INFLUXDB_DATABASE = "scirius"

# Moloch
USE_MOLOCH = False
MOLOCH_URL = "https://localhost:8005"

# Proxy parameters
# Set USE_PROXY to True to use a proxy to fetch ruleset update.
# PROXY_PARAMS contains the proxy parameters.
# If user is set in PROXY_PARAMS then basic authentication will
# be used.
USE_PROXY = False
PROXY_PARAMS = { 'http': "http://proxy:3128", 'https': "http://proxy:3128" }
# For basic authentication you can use
# PROXY_PARAMS = { 'http': "http://user:pass@proxy:3128", 'https': "http://user:pass@proxy:3128" }

