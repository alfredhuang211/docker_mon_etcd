# -*- coding: UTF-8 -*-
from docker import Client
import logging

logger = logging.getLogger("docker")


class DockerClient:
    def __init__(self, base_url='unix://var/run/docker.sock'):
        self.base_url = base_url
        try:
            self.client = Client(base_url)
        except Exception, e:
            raise e

    def get_running_id(self):
        c_list = list()
        for c in self.client.containers(quiet=True):
            c_list.append(c['Id'])
        return c_list

    def get_inspect(self, id_str):
        return self.client.inspect_container(id_str)

    def get_stats(self, id_str):
        return self.client.stats(id_str, decode=True, stream=False)

if __name__ == "__main__":
    dc = DockerClient()
    for id_str in dc.get_running_id():
        print dc.get_inspect(id_str)
        print dc.get_stats(id_str)


