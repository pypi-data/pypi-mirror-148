# 📦 seventeentrack: A Simple Python API for 17track.net

[![CI](https://github.com/mcswindler/seventeentrack/workflows/CI/badge.svg)](https://github.com/mcswindler/seventeentrack/actions)
[![PyPi](https://img.shields.io/pypi/v/seventeentrack.svg)](https://pypi.python.org/pypi/seventeentrack)
[![Version](https://img.shields.io/pypi/pyversions/seventeentrack.svg)](https://pypi.python.org/pypi/seventeentrack)
[![License](https://img.shields.io/pypi/l/seventeentrack.svg)](https://github.com/mcswindler/seventeentrack/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/mcswindler/seventeentrack/branch/master/graph/badge.svg)](https://codecov.io/gh/mcswindler/seventeentrack)
[![Maintainability](https://api.codeclimate.com/v1/badges/cd4e8b7fcc8f840009e5/maintainability)](https://codeclimate.com/github/mcswindler/seventeentrack/maintainability)

`seventeentrack` is a simple Python library to track packages in
[17track.net](http://www.17track.net/) accounts.

This project was built off of [py17track](https://github.com/bachya/py17track).

## V1 API

You can register an account first here: https://features.17track.net/en/api
Each account will have 100 free tracking quota for testing.
Once logged in, you can find the API token/Access key under Settings -> Security -> Access Key

# Python Versions

`seventeentrack` is currently supported on:

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10

# Installation

```python
pip install seventeentrack
```

# Usage

```python
import asyncio

from aiohttp import ClientSession

from seventeentrack import Client


async def main() -> None:
    """Run!"""
    client = Client()

    # Login with API token:
    client.profile.login("<TOKEN>")

    # Get a summary of the user's packages:
    summary = await client.profile.summary()
    # >>> {'In Transit': 3, 'Expired': 3, ... }

    # Get all packages associated with a user's account:
    packages = await client.profile.packages()
    # >>> [seventeentrack.package.Package(..), ...]

    # Add new packages by tracking number
    await client.profile.add_package('<TRACKING NUMBER>', '<FRIENDLY NAME>')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

By default, the library creates a new connection to 17track with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession

from seventeentrack import Client


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        client = Client(session=session)

        # ...


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

Each `Package` object has the following info:

- `destination_country`: the country the package was shipped to
- `friendly_name`: the human-friendly name of the package
- `info`: a text description of the latest status
- `location`: the current location (if known)
- `timestamp`: the timestamp of the latest event
- `origin_country`: the country the package was shipped from
- `package_type`: the type of package (if known)
- `status`: the overall package status ("In Transit", "Delivered", etc.)
- `tracking_info_language`: the language of the tracking info
- `tracking_number`: the all-important tracking number
- `carrier`: the logistics company transporting the package

# Contributing

1. [Check for open features/bugs](https://github.com/mcswindler/seventeentrack/issues)
   or [initiate a discussion on one](https://github.com/mcswindler/seventeentrack/issues/new).
2. [Fork the repository](https://github.com/mcswindler/seventeentrack/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!

# Updating Carrier and Country JSON

If the carrier or country lists need to be updated to support new ones, simply download the updated JSON from 17track.

https://res.17track.net/asset/carrier/info/carrier.all.json

https://res.17track.net/asset/carrier/info/country.all.json
