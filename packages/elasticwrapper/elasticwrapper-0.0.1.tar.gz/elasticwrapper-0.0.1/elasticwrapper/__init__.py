from importlib import import_module
import builtins
import json
import logging
import os
import sys
import time
import urllib.request


def add_submodule(submod):
    name = submod.__name__.replace(f"elasticsearch{major}", "elasticsearch")
    sys.modules[f"{__name__}.{name}"] = submod


if hasattr(builtins, "elasticwrapper_url"):
    URL = builtins.elasticwrapper_url
elif os.environ.get("ELASTICWRAPPER_URL"):
    URL = os.environ.get("ELASTICWRAPPER_URL")
else:
    URL = "http://localhost:9200"


if hasattr(builtins, "elasticwrapper_timeout"):
    TIMEOUT = builtins.elasticwrapper_timeout
elif os.environ.get("ELASTICWRAPPER_TIMEOUT"):
    TIMEOUT = int(os.environ.get("ELASTICWRAPPER_TIMEOUT"))
else:
    TIMEOUT = 30

logging.debug(f"URL: {URL}, timeout: {TIMEOUT}")

wait_until = time.time() + TIMEOUT
while True:
    retry = time.time() < wait_until
    try:
        r = urllib.request.urlopen(URL)
        data = json.loads(r.read())
    except Exception:
        if not retry:
            raise
        time.sleep(1)
        continue
    break

major = data["version"]["number"].split(".")[0]
logging.debug(f"importing elasticsearch{major}")
elasticsearch = import_module(f"elasticsearch{major}")

add_submodule(elasticsearch)

__version__ = "0.0.1"
