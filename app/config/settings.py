""" Settings module, uses a different paradigm from django

config based on yaml with ability to overwrite in environment


CONFIG_PATH = ./config/

CONFIG_FILES = 'base.yaml'

Then it loads ./config/base.yaml

Which is a nested dictionary. Then it loads from the environment based on
nested keys.

DJANGO__level1_key__level2_key: value


"""

import os
import yaml

# ############################################################################ #
#
# Relative paths
#
# ############################################################################ #


# /opt/app/
BASE_DIR = os.path.dirname(
    os.path.dirname(
        __file__
    )
)

# /opt/app
APP_DIR = os.path.join(BASE_DIR, 'app')


# ############################################################################ #
#
# Load the yaml settings
#
# ############################################################################ #


# Look in this path. E.g. /opt/app/config
CONFIG_PATH = os.environ.get(
    'CONFIG_PATH',
    os.path.join(BASE_DIR, 'config')
)


# Look for these files
CONFIG_FILES = os.environ.get(
    'CONFIG_FILES',
    'base.yaml',
)


def get_config(config_path, config_files):
    # get all config paths
    config_filenames = config_files.split(':')
    config_filepaths = []
    for filename in config_filenames:
        filepath = os.path.join(config_path, filename)
        if os.path.exists(filepath):
            print(f'found config {filepath}')
            config_filepaths.append(filepath)
        else:
            raise ValueError(f'no config {filepath}')

    # load config from each
    config = {}
    for filepath in config_filepaths:
        with open(filepath) as f:
            config.update(
                yaml.safe_load(f.read())
            )

    for key in config:
        if config[key] == [None]:
            config[key] = []

    return config


_config = get_config(CONFIG_PATH, CONFIG_FILES)


# ############################################################################ #
#
# Load environment variables
#
# ############################################################################ #


def get_env(setting):
    """ Read an environment file and load.

    """
    value = os.environ[setting]

    # Boolean values
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False

    # floats
    if '.' in value:
        try:
            return float(value)
        except ValueError:
            pass

    # integers
    try:
        return int(value)
    except ValueError:
        pass

    # list
    if ':' in value:
        return value.split(':')

    return value


def recursive_load_from_env(config, key_list=None):
    """ Load from the environment

    ENV DJANGO__key1___0___key2: True

    This will update config['key1'][0]['key2'] = True

    """
    if key_list is None:
        key_list = []
        value = config
    else:
        key = key_list[-1]
        if isinstance(key, str) and key.startswith('_'):
            return config
        value = config[key]

    env_name = '__'.join(['DJANGO'] + [str(k) for k in key_list])
    if env_name in os.environ:
        print(f'found env key {env_name}')
        config[key] = get_env(env_name)

    if isinstance(value, dict):
        for nested_key in value:
            recursive_load_from_env(value, key_list + [nested_key])
    elif isinstance(value, list):
        for i in range(len(value)):
            recursive_load_from_env(value, key_list + [i])


recursive_load_from_env(_config)

# add all _config to the globals of this module
globals().update(_config)
