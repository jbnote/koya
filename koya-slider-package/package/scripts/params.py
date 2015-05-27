from resource_management import *

config = Script.get_config()


app_root = config['configurations']['global']['app_root']
java64_home = config['hostLevelParams']['java_home']
app_user = config['configurations']['global']['app_user']
pid_file = config['configurations']['global']['pid_file']
app_log_dir = config['configurations']['global']['app_log_dir']
kafka_version = config['configurations']['global']['kafka_version']

conf_dir = format("{app_root}/config")
added_server_config=config['configurations']['server']
server_config=dict(line.strip().split('=') for line in open(format("{conf_dir}/server.properties")) if not (line.startswith('#') or re.match(r'^\s*$', line)))
server_config.update(added_server_config)
server_prop=server_config['content']
del server_config['content']

componentName = config['componentName']
