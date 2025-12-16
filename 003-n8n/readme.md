Blog post: https://jpitc.ca/posts/palo/palo_mcp_n8n/  

```
.
|-- .env
|-- docker-compose.yml
`-- paloalto-mcp-advanced
    |-- Dockerfile
    |-- main.py
    |-- requirements.txt
    `-- tools
        |-- __init__.py
        |-- objects
        |   |-- __init__.py
        |   |-- create_address_object.py
        |   |-- delete_address_object.py
        |   |-- list_address_objects.py
        |   `-- update_address_object.py
        |-- op
        |   |-- __init__.py
        |   `-- operational_command.py
        `-- security_policies
            |-- __init__.py
            |-- create_security_policies.py
            |-- delete_security_policy.py
            |-- list_security_policies.py
            `-- update_security_policy.py
```