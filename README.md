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

When building my first Django project with Bootstrap I went looking for available open soure applications that connected Django and Bootstrap. I found  https://github.com/tzangms/django-bootstrap-form, but I felt limiting the Django support to forms only was too limited.

This is how my django-bootstrap-toolkit project started. The basic idea of filtering a form came from django-bootstrap-form. I wrote my own version and improved the form handling, added various tags and filters, and gave the applications some settings to work from. Then I put the Apache 2.0 license on it and published it on GitHub. We'll see where it goes, I hope it comes in handy.

Thanks
------

* to Twitter for building and releasing Bootstrap
* to the Django community for Django
* to the authors of django-bootstrap-form for the inspiration
