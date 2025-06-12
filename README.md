# Coolify API

## This is my implementation of the Coolify api

The `CoolifyAPIClient` is a Python class defined in the `api_client.py` module of the `coolify_api` package. It serves as the main interface between the user and the Coolify API, providing organized access to various features of the API. The class uses an API key and base URL, typically fed from environment variables, to handle authentication with the API.

Upon initialization, it creates instances of multiple specialized classes, each corresponding to a different aspect of the Coolify API. Through these instances, users gain access to interactions with applications, databases, deployments, operations, private keys, projects, resources, servers, services, and teams. It essentially provides an organized set of handles to manage different components through the Coolify API, structuring the overall interaction with the API for ease of use and clarity.

The `CoolifyAPIClient` class provides an effective way to interact with the Coolify API. It handles the API key and base URL and provides Pythonic methods corresponding to various Coolify API endpoints.
Here is how you could instantiate the `CoolifyAPIClient` class and use its methods:

```python
# Import the CoolifyAPIClient
from coolify_api import CoolifyAPIClient
# Instantiate the class using appropriate credentials
api_client = CoolifyAPIClient(base_url='<your_coolify_base_url>', api_key='<your_coolify_api_key>')
# Use the instance's methods corresponding to different aspects of the Coolify API
response = api_client.applications.list_all()  # response is a list[dict[str, Any]].
```

**Note:** Replace `'<your_coolify_base_url>'` and `'<your_coolify_api_key>'` with the actual base URL and API key for your Coolify application.
Please refer to the specific documentation for the methods available under each instance variable (like `applications`, `databases`, etc.) in the `CoolifyAPIClient` class. The exact methods and their usage will depend on the corresponding classes (`CoolifyApplications`, `CoolifyDatabases`, etc.).
_Disclaimer:_ The above code is just an example, and the actual usage might differ depending on the methods available in the `CoolifyAPIClient` class. Always refer to the official Coolify API documentation and `CoolifyAPIClient` class documentation for accurate information.