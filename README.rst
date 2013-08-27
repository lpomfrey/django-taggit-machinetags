Django Taggit Machinetags
=============================

.. image:: https://badge.fury.io/py/django-taggit-machinetags.png
    :target: http://badge.fury.io/py/django-taggit-machinetags

.. image:: https://travis-ci.org/lpomfrey/django-taggit-machinetags.png?branch=master
    :target: https://travis-ci.org/lpomfrey/django-taggit-machinetags

.. image:: https://coveralls.io/repos/lpomfrey/django-taggit-machinetags/badge.png?branch=master
    :target: https://coveralls.io/r/lpomfrey/django-taggit-machinetags?branch=master

.. image:: https://pypip.in/d/django-taggit-machinetags/badge.png
        :target: https://crate.io/packages/django-taggit-machinetags?version=latest

Overview
--------

This package provides machine tagging (i.e. property:value tagging) built on
top of `django-taggit <https://github.com/alex/django-taggit>`_.

Installation
------------

Grab from PyPI with:

::
    
    $ pip install django-taggit-machinetags

Update your installed apps:

::
    
    INSTALLED_APPS = (
        ...
        'taggit',
        'taggit_machinetags',
        ...
    )

And run the migrations:

::
    
    $ python manage.py migrate

Or if you're not using south (why are you not using south?):

::
    
    $ python manage.py syncdb

Usage
-----

Usage is the same as taggit, but tags can now be specified as, colon-separated,
property-value pairs.

::

    # models.py
    from django.db import models
    from taggit_machinetags.managers import MachineTaggableManager
    
    class MyModel(models.Model):
        
        name = models.CharField(...)
        tags = MachineTaggableManager()

    #
    >>> instance = MyModel.objects.all()[0]
    >>> instance.tags.add('Property:Value')
    >>> instance.tags.add('Taggy:McTag')
    >>> instance.tags.get(namespace='Property')
    <MachineTag: Property:Value>
    >> MyModel.objects.filter(tags__slug='taggy:mctag')
    <MyModel:...>

Creating a tag with the string 'Property:Value' results in a MachineTag with
the namespace ``namespace=Property``, ``name=Value``,
``namespace_slug=property``, ``name_slug=value``, and ``slug=property:value``.
