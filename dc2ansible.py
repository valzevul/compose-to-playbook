import yaml
import os
import shutil

def create_folder_structure(base_dir):
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    os.makedirs(os.path.join(base_dir, 'inventory'))
    with open(os.path.join(base_dir, 'inventory', 'hosts'), 'w') as hosts_file:
        hosts_file.write("[local]\nlocalhost ansible_connection=local\n")

    os.makedirs(os.path.join(base_dir, 'playbooks'))
    os.makedirs(os.path.join(base_dir, 'roles'))

    print(f"Created folder structure at {base_dir}")

def generate_playbooks(docker_compose_file, output_dir):
    with open(docker_compose_file, 'r') as file:
        docker_compose_data = yaml.safe_load(file)

    services = docker_compose_data['services']

    for service_name, service_config in services.items():
        playbook_content = [
            "- hosts: local",
            "  tasks:",
            f"    - name: Start {service_name} container",
            "      community.docker.docker_container:",
            f"        name: {service_name}",
            f"        image: {service_config['image']}"
        ]

        if 'command' in service_config:
            playbook_content.append("        command:")
            for command in service_config['command']:
                playbook_content.append(f"          - '{command}'")

        if 'restart' in service_config:
            playbook_content.append(f"        restart_policy: {service_config['restart']}")

        if 'ports' in service_config:
            playbook_content.append("        ports:")
            for port in service_config['ports']:
                playbook_content.append(f"          - '{port}'")

        if 'networks' in service_config:
            playbook_content.append("        networks:")
            for network in service_config['networks']:
                playbook_content.append(f"          - name: {network}")

        if 'volumes' in service_config:
            playbook_content.append("        volumes:")
            for volume in service_config['volumes']:
                playbook_content.append(f"          - {volume}")

        if 'labels' in service_config:
            playbook_content.append("        labels:")
            for label in service_config['labels']:
                playbook_content.append(f"          {label}")

        playbook_path = os.path.join(output_dir, f"{service_name}.yml")
        with open(playbook_path, 'w') as playbook_file:
            playbook_file.write("\n".join(playbook_content))

        print(f"Generated playbook for {service_name} service: {playbook_path}")

if __name__ == "__main__":
    base_dir = "ansible-playbooks"
    docker_compose_file = "docker-compose.yml"
    output_dir = os.path.join(base_dir, "playbooks")

    create_folder_structure(base_dir)
    generate_playbooks(docker_compose_file, output_dir)