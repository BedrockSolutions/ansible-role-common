#!/usr/bin/env python3

try:
    import copy
    from ansible.errors import AnsibleError, AnsibleActionFail
    from ansible.module_utils._text import to_native
    from ansible.plugins.action import ActionBase
    from jsonschema import Draft6Validator, SchemaError, ValidationError, validators
except ImportError as e:
    raise AnsibleError(to_native(e))


def set_defaults(validator, properties, instance, schema):
    for prop, subschema in properties.items():
        if "default" in subschema:
            instance.setdefault(prop, subschema["default"])

    return Draft6Validator.VALIDATORS["properties"](validator, properties, instance, schema)


validator_overrides = {
    "patternProperties": set_defaults,
    "properties": set_defaults,
    "required": None,
    "oneOf": None,
}

DefaultValidator = validators.extend(Draft6Validator, validator_overrides)
RequiredValidator = Draft6Validator


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        action_vars = self._task.args

        if 'instance' not in action_vars:
            raise AnsibleError("instance parameter missing")

        if 'schema' not in action_vars:
            raise AnsibleError("schema parameter missing")

        instance_copy = copy.deepcopy(action_vars['instance'])

        try:
            default_validator = DefaultValidator(action_vars['schema'])
            default_validator.validate(instance_copy)

            # This fixes the bug where required was being enforced before
            # defaults were set.
            required_validator = RequiredValidator(action_vars['schema'])
            required_validator.validate(instance_copy)
        except ValidationError as e:
            raise AnsibleActionFail(to_native(e))
        except SchemaError as e:
            raise AnsibleActionFail(to_native(e))

        return_value = super(ActionModule, self).run(tmp, task_vars)
        return_value['result'] = instance_copy
        return return_value
