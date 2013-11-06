# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.validators import RegexValidator
from django.db.models.fields import SlugField


slug_re = re.compile(r'^[-a-zA-Z0-9_]+(:[-a-zA-Z0-9_]+)?$')
validate_slug = RegexValidator(
    slug_re,
    'Enter a valid slug with an optional colon separator.'
)


class MachineSlugField(SlugField):

    default_validators = [validate_slug]
