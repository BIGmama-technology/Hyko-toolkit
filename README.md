# The HYKO SDK.
- `./hyko-sdk` package which defines functions endpoitns `/on_startup`, `/on_execute`, defines hyko typing system and what downloads/uploads inputs and outputs.

- `./sdk` A collection of functions and AI models that are available on hyko.
- `./scripts/sdk_builder.py` allows you to validate and build images of sdk functions and to push them to a registry.

## To publish

Before publishing a new version of `hyko-sdk` make sure to update its version in `pyproject.toml`

Follow this convetion by [npm](https://docs.npmjs.com/about-semantic-versioning)

| Code status                            | Stage           | Rule                                                | Example version |
|----------------------------------------|-----------------|-----------------------------------------------------|-----------------|
| First release                          | New product     | Start with 1.0.0                                    | 1.0.0           |
| Backward compatible bug fixes          | Patch release   | Increment the third digit                          | 1.0.1           |
| Backward compatible new features       | Minor release   | Increment the middle digit and reset last digit to zero | 1.1.0           |
| Changes that break backward compatibility | Major release | Increment the first digit and reset middle and last digits to zero | 2.0.0 |

Generate a `pypi` token and add it to configure poetry to use it
```bash
poetry config pypi-token.pypi your-pypi-token
```

Now you can build and publish
```bash
poetry build
poetry publish
``` 
