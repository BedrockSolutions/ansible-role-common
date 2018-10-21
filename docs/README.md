# bedrock.common

Ansible role that contains commonly used tasks and plugins.

A prettier version of this documentation is located at 
https://bedrocksolutions.github.io/ansible-role-common

* Commands
  * [controller_reset_connection](#controller_reset_connection)
  
* Plugins
  * [validate](#validate)

## Dependencies

`jsonschema` pip module: 
```bash
pip install jsonschema
```

## Installation

To use `bedrock.common` in another role, create the file 
`<role_root>/meta/main.yml` with the following structure:

```yaml
dependencies:
  - name: bedrock.common
    scm: git
    src: https://github.com/BedrockSolutions/ansible-role-common.git
    vars:
      common:
        command: dependency
    version: v1.0
```

If you just want to use this role in a playbook or task file, then
add an entry to the `requirements.yml` file:

```yaml
- name: bedrock.common
  scm: git
  src: https://github.com/BedrockSolutions/ansible-role-common.git
  version: v1.0
```
>__Note:__ In both examples, the `version` field can be a branch,
tag, or commit hash. Set it to `master` to track the latest changes.

The plugins are now available, and the role can be imported or included
as `bedrock.common`.

## Command Invocation

The role is made up of commands that can be invoked using the following 
syntax:

```yaml
- import_role
    name: bedrock.common
  vars:
    common:
      command: <command_name>
      ...command_vars
```

or

```yaml
- include_role
    name: bedrock.common
  vars:
    common:
      command: <command_name>
      ...command_vars
```

## Commands

### __controller_reset_connection__

Resets the connection between the controller and a target machine.
Subsequent tasks will establish a new SSH login. This is useful when,
for example, the SSH user is added to a new group and a fresh login is
necessary to pick up the new group's privileges.

#### Example

```yaml
- import_task:
    name: bedrock.common
  vars:
    common:
      command: controller_reset_connection
```

## Plugins

### __validate__

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
