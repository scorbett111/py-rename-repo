def transform_configs(from_config=None, to_config=None, key=None):
    configs = to_config.get(key)
    if configs:
        targets = {}
        for config_key in configs:
            map_key = from_config.get(config_key).get('map')
            value = from_config.get(config_key).get('value')
            hooks = from_config.get(config_key).get('hooks')
            targets[map_key] = {
                'value': value,
                'hooks': hooks
            }
        # targets = {
        #     from_config.get(config_key).get('map'): from_config.get(config_key).get('value')
        # for config_key in configs }

        to_config[key] = targets

    return to_config