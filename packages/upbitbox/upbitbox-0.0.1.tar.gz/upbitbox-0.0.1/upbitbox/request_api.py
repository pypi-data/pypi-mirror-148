import requests

def _get(URL: str, **kwargs) -> requests.Response:
    return requests.get(URL, **kwargs)

def _post(URL: str, **kwargs) -> requests.Response:
    return requests.post(URL, **kwargs)

def _delete(URL: str, **kwargs) -> requests.Response:
    return requests.delete(URL, **kwargs)

def public_get(url, headers, **kwargs):
    resp = _get(url, headers=headers, params=kwargs)
    return resp.json()

def get(url, headers, **kwargs):
    resp = _get(url, headers=headers, data=kwargs)
    return resp.json()

def post(url, headers, **kwargs):
    resp = _post(url, headers=headers, data=kwargs)
    return resp.json()

def delete(url, headers, **kwargs):
    resp = _delete(url, headers=headers, data=kwargs)
    return resp.json()

