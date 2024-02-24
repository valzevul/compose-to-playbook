import os
import shutil
import yaml

def create_folder_structure(base_dir):
    """
    Create the necessary folder structure for the Ansible project.

    Args:
        base_dir (str): The base directory for the Ansible project.
    """
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    os.makedirs(os.path.join(base_dir, 'inventory'))
    with open(os.path.join(base_dir, 'inventory', 'hosts'), 'w') as hosts_file:
        hosts_file.write("[local]\nlocalhost ansible_connection=local\n")

    os.makedirs(os.path.join(base_dir, 'playbooks'))
    os.makedirs(os.path.join(base_dir, 'roles'))

    print(f"Created folder structure at {base_dir}")

def generate_playbook(service_name, service_config, output_dir):
    """
    Generate an Ansible playbook for a Docker Compose service.

    Args:
        service_name (str): The name of the Docker Compose service.
        service_config (dict): The configuration for the Docker Compose service.
        output_dir (str): The directory to save the generated playbook.
    """
    playbook_content = [
        "- hosts: local",
        "  tasks:",
        f"    - name: Start {service_name} container",
        "      community.docker.docker_container:",
        f"        name: {service_name}",
        f"        image: {service_config['image']}"
    ]

    for section in ['command', 'ports', 'networks', 'volumes', 'labels', 'environment']:
        if section in service_config:
            playbook_content.append(f"        {section}:")
            if isinstance(service_config[section], list):
                for item in service_config[section]:
                    playbook_content.append(f"          - '{item}'")
            elif isinstance(service_config[section], dict):
                for key, value in service_config[section].items():
                    playbook_content.append(f"          {key}: '{value}'")

    if 'restart' in service_config:
        restart_policy = service_config['restart']
        if isinstance(restart_policy, str):
            playbook_content.append(f"        restart_policy: {restart_policy}")
        else:
            playbook_content.append("        restart_policy: always")

    playbook_path = os.path.join(output_dir, f"{service_name}.yml")
    with open(playbook_path, 'w') as playbook_file:
        playbook_file.write("\n".join(playbook_content))

    print(f"Generated playbook for {service_name} service: {playbook_path}")

def generate_playbooks(docker_compose_file, output_dir):
    """
    Generate Ansible playbooks from a Docker Compose file.

    Args:
        docker_compose_file (str): The path to the Docker Compose file.
        output_dir (str): The directory to save the generated playbooks.
    """
    with open(docker_compose_file, 'r') as file:
        docker_compose_data = yaml.safe_load(file)

    services = docker_compose_data['services']

    for service_name, service_config in services.items():
        generate_playbook(service_name, service_config, output_dir)

if __name__ == "__main__":
    base_dir = "ansible-playbooks"
    docker_compose_file = "docker-compose.yml"
    output_dir = os.path.join(base_dir, "playbooks")

    create_folder_structure(base_dir)
    generate_playbooks(docker_compose_file, output_dir)