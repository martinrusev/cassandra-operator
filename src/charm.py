#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import cast
import yaml
import os


from ops.charm import CharmBase, PebbleReadyEvent
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, ModelError
from ops.pebble import ServiceStatus

from jproperties import Properties

CLUSTER_PORT = 7001
UNIT_ADDRESS = "{}-{}.{}-endpoints.{}.svc.cluster.local"
CONFIG_PATH = "/etc/cassandra"
SERVICE = "cassandra"

logger = logging.getLogger(__name__)

class CassandraOperator(CharmBase):

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(
            self.on.cassandra_pebble_ready, self._on_cassandra_pebble_ready
        )

        # self.framework.observe(self.on["cql"].relation_changed, self.on_cql_changed)

        # self.framework.observe(
        #     self.on["cassandra"].relation_changed, self.on_cassandra_changed
        # )
        # self.framework.observe(
        #     self.on["cassandra"].relation_departed, self.on_cassandra_departed
        # )


    def seeds(self):
        seeds = UNIT_ADDRESS.format(self.meta.name, 0, self.meta.name, self.model.name)
        num_units = self.num_units()
        if num_units >= 2:
            seeds = (
                seeds
                + ","
                + UNIT_ADDRESS.format(
                    self.meta.name, 1, self.meta.name, self.model.name
                )
            )
        if num_units >= 3:
            seeds = (
                seeds
                + ","
                + UNIT_ADDRESS.format(
                    self.meta.name, 2, self.meta.name, self.model.name
                )
            )
        return seeds

    def num_units(self):
        relation = self.model.get_relation("cassandra")
        # The relation does not list ourself as a unit so we must add 1
        return len(relation.units) + 1 if relation is not None else 1


    def _on_cassandra_pebble_ready(self, event: PebbleReadyEvent) -> None:
        container = event.workload
        logger.info("_on_cassandra_pebble_ready")

        # Check we can get a list of services back from the Pebble API
        if self._is_running(container, "cassandra"):
            logger.info("cassandra already started")
            return

        self._generate_config_file()
        self._generate_properties_file()

        logger.info("_start_cassandra")
        container.add_layer("cassandra", self._cassandra_layer(), True)
        container.autostart()
        self.unit.status = ActiveStatus("cassandra started")


    def _cassandra_layer(self):
        layer = {
            "summary": "cassandra layer",
            "description": "cassandra layer",
            "services": {
                "cassandra": {
                    "override": "replace",
                    "summary": "cassandra service",
                    "command": "sh -c docker-entrypoint.sh",
                    "default": "start",
                    "environment": []
                }
            },
        }

        return layer

    def _generate_properties_file(self):
        properties_file = os.path.join(CONFIG_PATH, "cassandra-rackdc.properties")

        cassandra_properties = Properties()
        cassandra_properties["dc"] = "dc1"
        cassandra_properties["rack"] = "rack1"

        with open(properties_file, "wb") as f:
            cassandra_properties.store(f, encoding="utf-8")


    def _generate_config_file(self):
        config_dict = {
            "cluster_name": "charm-cluster",
            "num_tokens": 256,
            "listen_address": "0.0.0.0",
            "start_native_transport": "true",
            "native_transport_port": self.model.config["port"],
            "seed_provider": [
                {
                    "class_name": "org.apache.cassandra.locator.SimpleSeedProvider",
                    "parameters": [{"seeds": self.seeds()}],
                }
            ],
            # Required configs
            "commitlog_sync": "periodic",
            "commitlog_sync_period_in_ms": 10000,
            "partitioner": "org.apache.cassandra.dht.Murmur3Partitioner",
            "endpoint_snitch": "GossipingPropertyFileSnitch",
        }

        config_yaml = os.path.join(CONFIG_PATH, "cassandra.yaml")
        logger.info("Creating a config file at: {}".format(config_yaml))
        with open(config_yaml, "w+") as file:
            yaml.dump(config_dict, file)


    def _is_running(self, container, service):
        """Helper method to determine if a given service is running in a given container"""
        try:
            service = container.get_service(service)
        except ModelError:
            return False
        return service.current == ServiceStatus.ACTIVE


if __name__ == "__main__":
    main(CassandraOperator)
