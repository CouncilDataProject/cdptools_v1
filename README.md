# CDP Tools

CDP Tools contains the tools and functions required to setup and run Council
Data Project instances as well as generate city sites. For detailed
documentation please refer our [individual docs](docs/).

## Quick Start

To set up a CDP instance, you will need to provide a config file with at least
the following attributes:

`/home/server_config.json`:
```json
{
    "legistar_city": "...",
    "storage_directory": "...",
    "collection_script": "...",
    "firebase_config": "..."
}
```

To then start the server you would simply:
```bash
$ pip install git+https://github.com/CouncilDataProject/cdp.git
$ start_cdp_instance /home/server_config.json
```

## Basic Requirements

The only thing we ask for you to install is
[Docker](https://www.docker.com/community-edition#/download).

All other requirements are packaged and handled by our server setup scripts.

## About

Council Data Project was created by Jackson Maxfield Brown and Dr. Nicholas
Weber with the goal of creating tools that would be usable by as many city
councils as possible. It is our believe that in providing access to city
council information in a unified system, journalist research and citizen
engagement regarding local and regional political action would become more
readily available and accessible.
