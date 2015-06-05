import logging
import sys
import os
import inspect
import pprint
import util
from resource_management import *

logger = logging.getLogger()

class Rest(Script):
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
    conffile=format("{params.rest_conf_dir}/kafka-rest.slider.properties")
    PropertiesFile(conffile,
                   properties = params.rich_config["kafka-rest"],
                   owner=params.app_user)

    process_cmd = format("{app_root}/bin/kafka-rest-start {conffile}")

    HEAP_OPTS = []
    for xopt in ["mx", "ms"]:
      xoptval=params.configs['rest'][format('x{xopt}')]
      if xoptval:
        HEAP_OPTS += [format("-X{xopt}{xoptval}")]

    if HEAP_OPTS:
        os.environ['KAFKAREST_HEAP_OPTS'] = " ".join(HEAP_OPTS)

    os.environ['LOG_DIR'] = params.app_log_dir
    # workaround bug in kafka-rest-run-class for the log4j of zip file
    os.environ['KAFKAREST_LOG4J_OPTS'] = format("-Dlog4j.configuration=file:{params.rest_conf_dir}/log4j.properties")
    Execute(process_cmd,
            user=params.app_user,
            logoutput=True,
            wait_for_finish=False,
            pid_file=params.pid_file)

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
  Rest().execute()
