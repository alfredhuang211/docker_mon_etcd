# -*- coding: UTF-8 -*-
import logging.config
import os
import sys


def is_bundle():
    return getattr(sys, 'frozen', False)

if is_bundle():
    log_config_file = os.path.realpath(sys._MEIPASS + os.sep + 'logging.conf')
else:
    log_config_file = os.path.realpath(os.path.split(os.path.realpath(__file__))[0] + os.sep + 'logging.conf')

print log_config_file

logging.config.fileConfig(log_config_file)
logger = logging.getLogger()


def docker_mon():
    from container.container import DockerClient
    from store.etcdstore import EtcdStore
    import simplejson as json
    import time
    dc = DockerClient()
    ec = EtcdStore()
    i = 0
    while True:
        for id_str in dc.get_running_id():
            print id_str
            if i % 10 == 0:
                inspect_json = json.dumps(dc.get_inspect(id_str=id_str))
                ec.write_container_inspect(container_id=id_str, contaier_inspect_json=inspect_json)
            stats_json = json.dumps(dc.get_stats(id_str))
            ec.write_container_stats(container_id=id_str, contaier_stats_json=stats_json)
        print "round ", i
        time.sleep(2)
        i += 1

if __name__ == '__main__':
    logger.info("Start")
    docker_mon()
    logger.info("Exit")
