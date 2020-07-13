import functools
import urllib
import requests

def http_handler(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        base_url_key = kwargs.get('base') 
        base_url = args[0].url_store.get(base_url_key, 'default')
        endpoint = kwargs.get('endpoint')

        if endpoint:
            kwargs['endpoint'] = "{base_url}/{endpoint}".format(
                base_url=base_url,
                endpoint=endpoint
            )

        else:
            kwargs['endpoint'] = base_url

        try:
            result = func(*args, **kwargs)
            result.raise_for_status()
        
        except requests.exceptions.HTTPError as failed_request:
            raise failed_request 

        return result.json()
    
    return wrapper