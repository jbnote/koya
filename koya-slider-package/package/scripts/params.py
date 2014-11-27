from resource_management import *

config = Script.get_config()


app_root = config['configurations']['global']['app_root']
java64_home = config['hostLevelParams']['java_home']
app_user = config['configurations']['global']['app_user']
pid_file = config['configurations']['global']['pid_file']
app_log_dir = config['configurations']['global']['app_log_dir']
kafka_version = config['configurations']['global']['kafka_version']

componentName = config['componentName']


componentConfig = config['configurations']['BROKER-COMMON']
componentConfig.update(config['configurations'][componentName])

