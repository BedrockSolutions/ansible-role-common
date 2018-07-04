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
    register: "{{ the_validated_data_with_defaults }}" # See note below
```

* __Note:__ The data with defaults is available at the `result` key.
See complex example below.

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

##### Complex object

```yaml
- validate:
    schema:
      type: object
      properties:
        host:
          type: string
          format: hostname
        port:
          type: integer
          default: 80
          minimum: 1
          maximum: 1024
        color:
          type: string
          enum:
            - red
            - green
            - blue
          default: blue
      required:
        - host
        - port
        - color
    instance: "{{ my_dict_var }}"
    register: my_dict_var_validated

# The validated instance, with defaults, is available like this:
- debug:
    var: my_dict_var_validated.result
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

### format_device

Formats the device with the specified filesystem. Currently only
supports `ext4`

#### Parameters

* `device`: The device to format. 
  * required
  * string
  
* `filesystem`: The filesystem to use. 
  * required
  * string
  * enum: `['ext4']`
  * default: `ext4`
  
```yaml
- import_task:
    name: jcheroske.common
  vars:
    common:
      command: format_device
      device: /dev/sdb
```

### reboot

Reboots the machine. 

* Flushes all handlers beforehand.
* After the reboot, waits for the machine's ssh connection 
to return before proceeding.

```yaml
- import_role:
    name: jcheroske.common
  vars:
    common:
      command: reboot
```

### reboot_if_required

Reboots the machine if the `reboot` handler had been previously
called, or if the `/var/run/reboot-required` file exists. 

* Flushes all handlers beforehand.
* After the reboot, waits for the machine's ssh connection 
to return before proceeding.

#### Example, using the handler

Notify the reboot handler:

```yaml
- some_task:
  notify: reboot
```

At a later point in the play where a conditional reboot is desired:

```yaml
- import_role:
    name: jcheroske.common
  vars:
    common:
      command: reboot_if_required
```

### shutdown

Performs an immediate system shutdown.

```yaml
- import_role:
    name: jcheroske.common
  vars:
    common:
      command: shutdown
```

### update_packages

Updates the `apt` package cache.

```yaml
- import_role:
    name: jcheroske.common
  vars:
    common:
      command: update_packages
```

### upgrade_packages

Upgrades installed packages

#### Parameters

* autoclean
  * required
  * boolean
  * default: `true`

* autoremove
  * required
  * boolean
  * default: `true`

* force_apt_get
  * required
  * boolean
  * default: `true`

* type
  * required
  * string
  * enum: `['full', 'safe']`
  * default: `safe`

* update_cache
  * required
  * boolean
  * default: `false`

```yaml
- import_role:
    name: jcheroske.common
  vars:
    common:
      command: upgrade_packages
      update_cache: yes
```
