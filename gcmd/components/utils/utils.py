def transform_configs(from_config=None, to_config=None, key=None):
    configs = to_config.get(key)
    if configs:
        targets = {
            from_config.get(config_key).get('map'): from_config.get(config_key).get('value')
        for config_key in configs }

        to_config[key] = targets

    return to_config