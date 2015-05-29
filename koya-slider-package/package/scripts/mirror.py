import logging
import sys
import os
import inspect
import pprint
import util
from resource_management import *

logger = logging.getLogger()

class MirrorMaker(Script):
  def install(self, env):
    self.install_packages(env)

  def configure(self, env):
    import params
    env.set_params(params)

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)

    # update the broker properties for different brokers
    confs={}
    for endpoint in ["consumer", "producer"]:
      conf=format("{params.conf_dir}/{endpoint}.slider.properties")
      confs[endpoint] = conf
      PropertiesFile(conf,
                     properties = params.rich_config[endpoint],
                     owner=params.app_user)

    # execute the process
    # We could probably fit consumer.conf and producer.config there
    # too and remove the xmx hack
    mirror_args=[]
    for k,v in params.configs['mirror'].iteritems():
      if k not in ["xmx", "xms"]:
        mirror_args += [format("--{k}={v}")]

    mirror_joinedargs=" ".join(mirror_args)
    process_cmd = format("{app_root}/bin/kafka-mirror-maker.sh --consumer.config {consumer} --producer.config {producer} {mirror_joinedargs}",
                         **confs)

    HEAP_OPTS = []
    for xopt in ["mx", "ms"]:
      xoptval=params.configs['mirror'][format('x{xopt}')]
      if xoptval:
        HEAP_OPTS += [format("-X{xopt}{xoptval}")]

    if HEAP_OPTS:
        os.environ['KAFKA_HEAP_OPTS'] = " ".join(HEAP_OPTS)

    os.environ['LOG_DIR'] = params.app_log_dir + "/kafka_mirror"
    os.environ['DAEMON_MODE'] = "true"
    os.environ['CONSOLE_OUTPUT_FILE'] = params.app_log_dir + "/kafka.log"
    Execute(process_cmd,
        user=params.app_user,
        logoutput=True,
        wait_for_finish=False,
        pid_file=params.pid_file
    )

  def stop(self, env):
    import params
    env.set_params(params)
    pid = format("`cat {pid_file}` >/dev/null 2>&1")
    Execute(format("kill {pid}"),
      user=params.app_user
    )
    Execute(format("kill -9 {pid}"),
      ignore_failures=True,
      user=params.app_user
    )
    Execute(format("rm -f {pid_file}"),
      user=params.app_user)

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.pid_file)

if __name__ == "__main__":
  MirrorMaker().execute()
