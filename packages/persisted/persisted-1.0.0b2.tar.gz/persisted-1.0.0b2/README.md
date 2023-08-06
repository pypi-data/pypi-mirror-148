# Persisted

Persisted is a two-way code/data persistence framework.
It can update a variable when a watched file changes, and also save data back to the file when the variable changes.

```python
>>> import persisted
>>> data = persisted.as_string('README.md', '')
>>> data.get()
"# Persisted\n\nPersisted is a two-way..."
>>> with data:
        data.value = "Change to this"
>>> data.get()
"Change to this"
```

This is very useful to keep configuration files / application state synchronized within a long-running application, and also hot-reload code / modules.

## Installing

```console
$ python -m pip install persisted
```

## Usage

There are several helper functions for you to get started:
- `persisted.as_bytes`
- `persisted.as_string`
- `persisted.as_pickle`
- `persisted.as_module` (only reloading)

All of them call `persisted.Persisted` to create a Persisted object to interact with.
