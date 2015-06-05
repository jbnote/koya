from resource_management import *
import os

config = Script.get_config()
configs = config['configurations']

app_root = config['configurations']['global']['app_root']
java64_home = config['hostLevelParams']['java_home']
app_user = config['configurations']['global']['app_user']
pid_file = config['configurations']['global']['pid_file']
app_log_dir = config['configurations']['global']['app_log_dir']
kafka_version = config['configurations']['global']['kafka_version']
xmx = configs['broker']['xmx_val']
xms = configs['broker']['xms_val']


conf_apache_dir = format("{app_root}/config")
conf_confluent_dir = format("{app_root}/etc/kafka")
conf_dir=conf_apache_dir if os.path.isdir(conf_apache_dir) else conf_confluent_dir
rest_conf_dir = format("{app_root}/etc/kafka-rest")

def enrich_dict(conf_dir, conf_file, conf_key):
    deffile=format("{conf_dir}/{conf_file}", conf_dir=conf_dir, conf_file=conf_file)
    default_config=dict(line.strip().split('=') for line in open(deffile) if not (line.startswith('#') or re.match(r'^\s*$', line)))
    default_config.update(configs[conf_key])
    return default_config

rich_config={}
def _enrich(conf_dir, endpoint):
    rich_config[endpoint] = enrich_dict(conf_dir, format("{endpoint}.properties"), endpoint)

def enrich(endpoint):
    _enrich(conf_dir, endpoint)

def enrich_rest(endpoint):
    _enrich(rest_conf_dir, endpoint)

map(enrich, ["consumer", "producer", "server"])
map(enrich_rest, ["kafka-rest"])

# For compatibility for now
broker_config=rich_config['server']
