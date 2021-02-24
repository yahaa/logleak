#!/usr/bin/python
# encoding=utf-8

import fcntl
import sys
import click
from kubernetes import client, config


def run():
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL)

    try:
        container_ids = set(filter(lambda item: len(item) > 0,
                                   sys.stdin.read().splitlines()))

    except TypeError as e:
        click.secho("please input container ids", fg='red')
        sys.exit(1)

    config.load_kube_config()
    pods_ret = client.CoreV1Api().list_pod_for_all_namespaces(
        watch=False, field_selector="status.phase=Running")

    for item in pods_ret.items:
        for cs in item.status.container_statuses:
            id = cs.container_id.replace('docker://', '')

            if id in container_ids:
                click.secho("{}/{}".format(item.metadata.namespace,
                                           item.metadata.name), fg='red')


if __name__ == '__main__':
    run()
