# compose-to-playbook

`compose-to-playbook` is a Python tool that converts Docker Compose files into Ansible playbooks, enabling you to manage your containerized infrastructure using Ansible's powerful automation capabilities.

## Features

- Automatic conversion of Docker Compose configurations into Ansible playbooks
- Generates a structured Ansible project directory with playbooks, roles, and inventory files
- Allows easy updates to individual service configurations by modifying the corresponding Ansible playbook
- Leverages Ansible's idempotent nature for consistent and reliable deployment of containerized applications
- Enables the creation of custom Ansible roles for common tasks, promoting code reuse and maintainability

## Installation

1. Clone the repository
2. Install the required Python dependencies:
`pip install -r requirements.txt`

## Usage

1. Place your `docker-compose.yml` file in the root directory of the repository.

2. Run the conversion script:
`python dc2ansible.py`

This will generate an `ansible-playbooks` directory with the following structure:

```
ansible-playbooks/
├── inventory/
│   └── hosts
├── playbooks/
│   ├── service1.yml
│   ├── service2.yml
│   └── ...
└── roles/
```

The `playbooks` directory will contain separate Ansible playbooks for each service defined in your `docker-compose.yml` file.

## Example

Given the following `docker-compose.yml` file:

```yaml
version: '3'

services:
  web:
    image: nginx:latest
    ports:
      - 80:80
    restart: always

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
    volumes:
      - db_data:/var/lib/mysql
    restart: always

volumes:
  db_data:
```

The resulting Ansible folder structure will look like this:

```
ansible-playbooks/
├── inventory/
│   └── hosts
├── playbooks/
│   ├── web.yml
│   └── db.yml
└── roles/
```

The web.yml playbook will contain tasks to start the Nginx container, and the db.yml playbook will handle the MySQL container.

You can now use these Ansible playbooks to manage your containerized infrastructure, making updates as needed to individual services by modifying the corresponding playbook.
