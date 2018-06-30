# Dependencies

```bash
pip install jsonschema
```

# Installation/Usage

To use the plugins and modules in another role, create a dependency
from that role to this one.

* In the new role, create the file `./meta/main.yml` with the 
following structure:

```yaml

---
dependencies:
  - { role: jcheroske.common }
```

# Plugins

## `validate`

A plugin that brings `jsonschema` validation to Ansible
data structures. Declare a `schema` that describes the correct 
structure, and then pass an `instance` to be validated. See
https://python-jsonschema.readthedocs.io

### Usage

```yaml
- validate:
    schema: "{{ the_json_schema }}"
    instance: "{{ the_data_to_be_validated }}"
```

### Examples

#### Simple scalar

```yaml
- validate:
    schema:
      type: string
      pattern: ^some-regex-.*$
    instance: "{{ my_string_var }}"
```

#### Object

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