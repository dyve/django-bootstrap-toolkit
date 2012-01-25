Django Toolkit for integration with Twitter's Bootstrap
=======================================================
http://twitter.github.com/bootstrap


Installation
------------
1. Install using pip:

        pip install django-bootstrap-toolkit

2. Add to INSTALLED_APPS:

        'bootstrap_toolkit',

Alternatively, you can add `django-bootstrap-toolkit` to your requirements.txt.

If you want to hack django-bootstrap itself, clone this repo and call `pip install -e .`.

Usage
-----

    {% load bootstrap_toolkit %}

    <form action="/url/to/submit/" method="post">
        {% csrf_token %}
        {{ form|as_bootstrap }}
        <div class="actions">
            <button type="submit" class="btn primary">Submit</button>
        </div>
    </form>

About
-----

django-bootstrap-toolkit is written by Dylan Verheul (dylan@dyve.net).

Bug tracker
-----------

Have a bug? Please create an issue here on GitHub!

https://github.com/dyve/django-bootstrap-toolkit/issues

History
-------

When building my first Django project with Bootstrap I went looking for available open source applications that connected Django and Bootstrap.

I found  https://github.com/tzangms/django-bootstrap-form. The approach to template tags and filters seemed right, but Bootstrap does so much more than just forms.

This is how `django-bootstrap-toolkit` started. I used ideas from other Django apps. The code was started from scratch in order to avoid license issues.

License
-------

You can use this under Apache 2.0. See LICENSE file for details.

Thanks
------

* to Twitter for building and releasing Bootstrap
* to the Django community for Django
* to the authors of django-bootstrap-form for the inspiration
