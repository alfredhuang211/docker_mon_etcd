# -*- coding: UTF-8
import etcd
import logging

logger = logging.getLogger("etcd")


class EtcdStore:
    def __init__(self, host="localhost", port=2379, base_uri="/docker_mon"):
        self.host = host
        self.port = port
        self.client = etcd.Client(host=self.host, port=self.port)
        self.base_uri = base_uri

    def get_docker_uri(self, container_id=""):
        docker_base = "/docker"
        if len(container_id) > 0:
            return self.base_uri+docker_base+"/"+container_id.strip(" /r/n")
        else:
            return self.base_uri+docker_base

    def get_host_uri(self, host_id=""):
        host_base = "/host"
        if len(host_id) > 0:
            return self.base_uri + host_base + "/" + host_id.strip(" /r/n")
        else:
            return self.base_uri + host_base

    def write_container_inspect(self, container_id, contaier_inspect_json, ttl=60):
        uri = self.get_docker_uri(container_id)+"/inspect"
        self.client.write(uri, contaier_inspect_json, ttl=ttl)

    def write_container_stats(self, container_id, contaier_stats_json, ttl=30):
        uri = self.get_docker_uri(container_id) + "/stats"
        self.client.write(uri, contaier_stats_json, ttl=ttl)

    def write_host_info(self, host_id, host_info, ttl=120):
        uri = self.get_host_uri(host_id) + "/info"
        self.client.write(uri, host_info, ttl=ttl)

