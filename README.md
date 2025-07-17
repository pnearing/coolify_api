# Coolify API Python Client

## Overview

This library provides a comprehensive Python client for interacting with the [Coolify](https://coolify.io) API. It allows you to manage applications, databases, services, deployments, projects, servers, teams, resources, and more, all via Python code. The client supports both synchronous and asynchronous usage and is designed for seamless integration with Coolify's API endpoints.

## Features

- **Applications:** List, create, update, start, stop, restart, and manage environment variables for Coolify applications.
- **Databases:** List, create, update, start, stop, restart, and delete databases. Supports configuration for various database types.
- **Services:** Manage lifecycle (create, update, start, stop, restart, delete) and environment variables for services.
- **Deployments:** List deployments, get deployment details, and trigger deployments by UUID or tag.
- **Projects:** Create, update, delete, and list projects, and manage project environments.
- **Environments:** Manage environment variables for applications and services (list, create, update, delete).
- **Servers, Teams, Resources, Private Keys, Operations:** Full API coverage for these Coolify resources.
- **Async and Sync:** Automatically detects and supports both async and sync usage.
- **Error Handling:** Rich exceptions for authentication, validation, and API errors.
- **Rate Limiting:** Handles API rate limits for robust automation.

## Installation

Install the dependencies (see `requirements.txt`):

```bash
pip install -r requirements.txt
```

You can also add this library to your project as a module.

## Usage

### Basic Example

```python
from coolify_api import CoolifyAPIClient

# You can set COOLIFY_API_KEY and COOLIFY_API_URL as environment variables, or pass them directly
client = CoolifyAPIClient(api_key="your_api_key")

# List all applications
apps = client.applications.list_all()

# Get details for a specific application
app = client.applications.get("app-uuid")

# Start an application
deploy_result = client.applications.start("app-uuid")

# Manage environment variables
env_var = client.applications.environment.create("app-uuid", {"key": "DATABASE_URL", "value": "postgresql://..."})

# List all databases
databases = client.databases.list_all()

# Create a new project
project = client.projects.create({"name": "My Project", "description": "Project description"})
```

### Async Usage:

The async_mode parameter is optional and defaults to None, it acts as an override for the async detection logic.  If set to True, the client will always use async mode, and if set to False, the client will always use sync mode. If set to None, the client will automatically detect the mode based on the runtime environment, this detection is done at the time of the call, as such it is possible to use both async and sync mode in the same script.

```python
import asyncio
from coolify_api import CoolifyAPIClient

async def main():
    client = CoolifyAPIClient(api_key="your_api_key", async_mode=True)
    apps = await client.applications.list_all()
    print(apps)

asyncio.run(main())
```

## Environment Variables

- `COOLIFY_API_KEY`: Your Coolify API key (required)
- `COOLIFY_API_URL`: Base URL for the Coolify instance (default: `https://app.coolify.io`)
- `REQUESTS_PER_SECOND`: (optional) Set API rate limit (default: 3.3)
- `REQUESTS_TIMEOUT`: (optional) Request timeout in seconds (default: 10)

## Project Structure

- `src/coolify_api/`: Main source code
    - `api_client.py`: Main entry point client
    - `applications.py`, `databases.py`, `deployments.py`, `services.py`, `projects.py`, etc.: Resource-specific clients
    - `environments.py`: Environment variable management
    - `_http_utils.py`: HTTP and async utilities
    - `_logging.py`, `exceptions.py`: Logging and error handling
- `requirements.txt`: Python dependencies

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
