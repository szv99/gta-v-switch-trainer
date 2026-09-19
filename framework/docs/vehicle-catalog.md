# Vehicle catalog

`catalog/vehicles.json` is the static declaration for the nine vehicle choices
currently exposed by the trainer. Each entry has a stable `vehicle.*` id, a
canonical lowercase model `name`, display `label`, supported `category`, and a
separate `runtime.availability` value. `tested` currently applies only to
Adder and Sultan; the other seven entries are `unconfirmed` declarations.

Load it with the standard-library API:

```python
from catalog import load_catalog
catalog = load_catalog()
```

Run `python tools/check_catalog.py` to validate the file. The `menyoo_import`
metadata is reserved for future mapping work. It does not promise Menyoo XML
compatibility, and no Menyoo source or XML is copied into this catalog.
