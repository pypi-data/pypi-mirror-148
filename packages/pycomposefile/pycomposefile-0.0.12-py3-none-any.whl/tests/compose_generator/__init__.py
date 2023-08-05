
from pycomposefile import ComposeFile
import yaml


class ComposeGenerator:

    @staticmethod
    def convert_yaml_to_compose_file(yaml_string):
        compose_yaml = yaml.load(yaml_string, Loader=yaml.Loader)
        return ComposeFile(compose_yaml)

    @staticmethod
    def get_compose_with_string_value(variable_name):
        compose = """
services:
  frontend:
    image: awesome/${replace_me}
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose.format(replace_me=variable_name))

    @staticmethod
    def get_compose_with_decimal_value(variable_name):
        compose = """
services:
  frontend:
    image: awesome/website
    cpu_count: ${replace_me}
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose.format(replace_me=variable_name))

    @staticmethod
    def get_with_two_environment_variables_in_string_value(first_variable_name, second_variable_name):
        compose = """
services:
  frontend:
    image: awesome/website
    cpu_count: 1.5
    ports: "${replace_first}:${replace_second}"
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose.format(replace_first=first_variable_name, replace_second=second_variable_name))

    @staticmethod
    def get_compose_with_one_service_with_deploy():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose: "3000"
    command: bundle exec thin -p 3000
    blkio_config:
      weight: 300
      weight_device:
        - path: /dev/sda
          weight: 400
      device_read_bps:
        - path: /dev/sdb
          rate: '12mb'
      device_read_iops:
        - path: /dev/sdb
          rate: 120
      device_write_bps:
        - path: /dev/sdb
          rate: '1024k'
      device_write_iops:
        - path: /dev/sdb
          rate: 30
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
      placement:
        constraints:
          - disktype=ssd
      resources:
        limits:
          cpus: '0.50'
          memory: 50M
          pids: 1
        reservations:
          cpus: '0.25'
          memory: 20M
      labels:
        com.example.description: "This label will appear on the web service"
        com.example.otherstuff: "random things"
      rollback_config:
        order: stop-first
        monitor: 5m
      update_config:
        order: start-first
        failure_action: rollback
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_one_service_with_multiple_expose():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose:
      - 3000
      - "4000"
      - '5000'
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_command_list():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose: "3000"
    command:
      - bundle
      - exec
      - thin
      - -p
      - 3000
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_command_list_with_quotes():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - "8080:80"
    expose: "3000"
    command:
      - echo
      - "hello world"
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_structured_ports():
        compose = """
services:
  frontend:
    image: awesome/webapp
    ports:
      - target: 80
        host_ip: 127.0.0.1
        published: 8080
        protocol: tcp
        mode: host

      - target: 443
        host_ip: 192.168.1.11
        published: 8443
        protocol: tcp
        mode: host
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_structured_configs():
        compose = """
services:
  frontend:
    image: awesome/webapp
    configs:
      - source: my_config
        target: /redis_config
        uid: "103"
        gid: "103"
        mode: 0440

      - source: another_config
        target: /db_config
        uid: "105"
        gid: "105"
        mode: 0777
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)

    @staticmethod
    def get_compose_with_string_configs():
        compose = """
services:
  frontend:
    image: awesome/webapp
    configs:
      - source: my_config
      - source: another_config
"""
        return ComposeGenerator.convert_yaml_to_compose_file(compose)
