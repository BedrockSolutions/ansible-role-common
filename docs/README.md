# bedrock.common

Ansible role that contains commonly used tasks and plugins.

Documentation is located at 
https://bedrocksolutions.github.io/ansible-role-common
 
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
  - name: bedrock.common
    scm: git
    src: https://github.com/BedrockSolutions/ansible-role-common.git
    vars:
      common:
        command: dependency
    version: master
```

This allows importing or including of the role, and makes the 
plugins available.

>__Note:__ The `version` field can be a branch, tag, or commit hash.

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
    register: the_validated_data_with_defaults # See note
```

>__Note:__ The data with defaults is available at the `result` key.
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

## Tasks/Commands

### `controller_reset_connection`

Resets the connection between the controller and a target machine.
Subsequent tasks will establish a new SSH login.

#### Example

```yaml
- import_task:
    name: bedroc.common
  vars:
    common:
      command: controller_reset_connection
```
