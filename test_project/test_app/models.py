# -*- coding: utf-8 -*-
from django.db import models

from taggit_machinetags.managers import MachineTaggableManager


class TestModel(models.Model):
    tags = MachineTaggableManager()
