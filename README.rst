=====
Peo
=====

Peo is a simple Django app to manage peos

Quick start
-----------

1. Add "peo" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'peo',
    ]

2. Include the URLconf in your project urls.py like this::

    url(r'^peo/', include('peo.urls')),

3. Run `python manage.py migrate` to create the boter models.