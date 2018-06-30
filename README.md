# jcheroske.ansible-role-common

Ansible role that makes several commonly used plugins 
and handlers available to other roles.

## Dependencies

`jsonschema` pip module: 
```bash
pip install jsonschema
```

## Installation/Usage

To use the plugins and handlers in another role, 
create a dependency from that role to this one.

* In the new role, create the file `./meta/main.yml` with the 
following structure:

```yaml

---
dependencies:
  - { role: jcheroske.ansible_role_common }
```

## Plugins

### `validate`

A plugin that brings `jsonschema` validation to Ansible
data structures. Declare a `schema` that describes the correct 
structure, and then pass an `instance` to be validated. See
https://python-jsonschema.readthedocs.io

#### Usage

```yaml
- validate:
    schema: "{{ the_json_schema }}"
    instance: "{{ the_data_to_be_validated }}"
```

#### Examples

##### Simple scalar

```yaml
- validate:
    schema:
      type: string
      pattern: ^some-regex-.*$
    instance: "{{ my_string_var }}"
```

##### Object

```yaml
- validate:
    schema:
      type: object
      properties:
        foo:
          type: string
        bar:
          type: number
    instance: "{{ my_dict_var }}"
```

## Handlers

### reboot

Reboots the machine and waits for an ssh connection.

### ufw_reload

Reloads the ufw firewall

## Tasks

### controller_reset_connection

Resets the connection between the controller and a target machine.
Subsequent tasks will establish a new SSH login.

```yaml
- import_task:
    name: jcheroske.ansible_role_common
  vars:
    common:
      command: controller_reset_connection
```