import json

from django.db import models
from django.utils.translation import gettext_lazy as _

from django.forms import ValidationError


class JSONField(models.TextField):
    description = _('JSON')

    def db_type(self, connection):
        return 'text'

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError(_('Unexpected value type: {}'.format(value.__class__.__name__)))

        try:
            json_obj = json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError(_('Invalid JSON format'))

        return json_obj

    def get_db_prep_value(self, value, connection, prepared=False):
        try:
            json_as_string = json.dumps(value)
        except json.JSONDecodeError:
            raise ValidationError(_('Invalid JSON format'))

        return json_as_string




