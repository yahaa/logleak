#!/usr/bin/python
# encoding=utf-8

import fnmatch
import os
import re


container_dir = "/var/lib/docker/containers"
suffix = re.compile(r'-json.log.*')

includes = ['*.log.*']
includes = r'|'.join([fnmatch.translate(x) for x in includes])


def check(root_path):
    root = os.walk(root_path)
    filters = {}
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            if re.match(includes, file_name):
                container_id = suffix.sub("", file_name)
                log_file = os.path.join(root, file_name)

                if container_id in filters:
                    filters[container_id].append(log_file)
                else:
                    filters[container_id] = [log_file]

    for id, log_files in filters.items():
        log_files.sort()

        if len(log_files) <= 1:
            continue

        t1 = os.stat(log_files[0]).st_mtime
        t2 = os.stat(log_files[1]).st_mtime

        # 2min
        if t1-t2 <= 120:
            print("leak container: {}".format(id))


if __name__ == '__main__':
    check(container_dir)
