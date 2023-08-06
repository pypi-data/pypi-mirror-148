# elasticwrapper

Elasticsearch offers (major) API-versioned packages for its Python SDK, called `elasticsearch2`,
`elasticsearch5` and so on.
This wrapper connects to the given URL, retrieves the major version and imports the versioned
module according to that.

Usage examples:

```python
from elasticwrapper import elasticsearch

es = elasticsearch.Elasticsearch()

res = es.search(index="*", body={})
```

This will connect to the default `http://localhost:9200/` URL.

## Customizing the wrapper

You can override defaults in the following ways:

### With environment variables

You can set the Elasticsearch URL with the following environment variable:

```sh
ELASTICWRAPPER_URL=http://localhost:9200 python -c "from elasticwrapper import elasticsearch; print(elasticsearch)"
```

And the connect timeout with:
`ELASTICWRAPPER_TIMEOUT`
(specified in seconds)


### Through `builtins`

The URL can be set from code as well, either by setting the above environment variable (before)
the import, or by through the `builtins` module:

```python
# anywhere in the code before the `elasticwrapper` import
import builtins
builtins.elasticwrapper_url = "http://localhost:9200"
builtins.elasticwrapper_timeout = 30

# anywhere in the code after variables has been set up in `builtins`
from elasticwrapper import elasticsearch
```

# Caveats

Elasticwrapper (currently) does nothing more than selecting the right (major) `elasticsearch`
module to be imported and imports it under `elasticwrapper.elasticsearch`.

Be aware, that `elasticsearch` might be incompatible with your Elasticsearch cluster even in the
same major version (like `7.x`).
Also, `elasticwrapper` currently does nothing to provide API compatibility, so different SDK versions
might (and will) need different syntax.