""" Tools for settings.


!!! CURRENTLY NOT USED !!!

The ability to overwrite any variable seems like overkill and a
simpler way is just to have those explicitly added in the code. Basically it 
allows the ability to overwriting any variable in the settings using
an environment variable.

To implement

```
globals().update(recursive_load_from_env(globals()))
```

config based on yaml with ability to overwrite in environment


CONFIG_PATH = ./config/

CONFIG_FILES = 'base.yaml'

Then it loads ./config/base.yaml

Which is a nested dictionary. Then it loads from the environment based on
nested keys.

DJANGO__level1_key__level2_key: value


"""
import os


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

    # string
    return value


def recursive_load_from_env(config, key_list=None):
    """ Load from the environment

    ENV DJANGO__key1___0___key2: True

    This will update config['key1'][0]['key2'] = True

    Parameters
        config (dict): nested dict of variables
        key_list (list): recursive keys

    """
    if key_list is None:
        key_list = []
        value = config
    else:
        key = key_list[-1]

        env_name = '__'.join(['DJANGO'] + [str(k) for k in key_list])
        if env_name in os.environ:
            print(f'found env key {env_name}')
            config[key] = _get_env(env_name)
            return config

        value = config[key]

    if isinstance(value, dict):
        for nested_key in value:
            if isinstance(nested_key, str) and nested_key.startswith('_'):
                continue
            recursive_load_from_env(value, key_list + [nested_key])
        return value
    elif isinstance(value, list):
        for i in range(len(value)):
            recursive_load_from_env(value, key_list + [i])
        return value

    else:
        # t = type(value)
        # raise TypeError(f'Invalid type {t} with {value}')
        return config
