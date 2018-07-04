# jcheroske.common

Ansible role that contains several commonly used tasks, handlers,
and plugins.
 
## Dependencies

`jsonschema` pip module: 
```bash
pip install jsonschema
```

## Installation

In the client role, create the file `./meta/main.yml` with the 
following structure:

```yaml

---
dependencies:
  - name: jcheroske.common
    scm: git
    src: git@github.com:jcheroske/ansible-role-common.git
    version: master
```

This allows importing or including of the role, 
and makes the handers and plugins available.

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

Causes the `reboot_if_required` command to initiate a reboot.

## Tasks/Commands

### controller_reset_connection

Resets the connection between the controller and a target machine.
Subsequent tasks will establish a new SSH login.

```yaml
- import_task:
    name: jcheroske.common
  vars:
    common:
      command: controller_reset_connection
```

### reboot

Reboots the machine.

```yaml
- import_role:
    name: jcheroske.common
  vars:
    common:
      command: reboot
```

### reboot_if_required

Reboots the machine if the `reboot` handler had been previously
called.

#### Example

Notify the reboot handler:

```yaml
- some_task:
  notify: reboot
```

At the point in the play where a conditional reboot is desired:

```yaml
- import_role:
    name: jcheroske.common
  vars:
    common:
      command: reboot_if_required
```
