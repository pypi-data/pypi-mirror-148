# django-usefathom

Fathom Analytics integration with Django projects. Provides ability to integrate
page view tracking and goal reporting.

## Installation

Install the package:

```
pip install django-usefathom
```

Add `usefathom` to your `settings.py` file:

```python
INSTALLED_APPS = [
    # ...
    "usefathom",
    # ...
]
```

Add template processor to your `settings.py` file:

```python
TEMPLATES = [
    {
        # ....
        "OPTIONS": {
            "context_processors": [
                # ...
                "usefathom.context_processors.usefathom",
                # ...
            ],
        },
    },
]
```

Add your fathom site id to your `settings.py` file:

```python
FATHOM_SITE_ID = "XXXX1234"
```

Include tracking snippet in your templates:

```jinja2
{% include "usefathom/usefathom.html" %}
```

From this point your site visits will be tracked.

## Custom domain for Fathom Analytics script

If you want to use the custom domain for Fathom Analytics add to your `settings.py`:

```python
FATHOM_SCRIPT_URL=https://cname.yourdomain.com/script.js
```

## Goal Tracking

### Python

Optionally, add your goals dictionary to your `settings.py` file:

```python
FATHOM_GOALS = {
    "registration": "XXXO9X",
    "add_to_card": "YYYO9X,
    # ....
}
```

Now if you want to report a goal from your backend service to Fathom analytics:

```python
from usefathom.api import track

def some_view(request, *args, **kwargs):
    # anywhere you have request object, most likely views are a good place for this
    track(request, "add_to_card", "2999")  # Third parameter is optional, attaches the monetary value to the goal. 29.99 in example
```

And the goal will be reported to Fathom analytics on the next page load.

### HTML+JS

You can use template tags to track the goals from the html. It's useful when tracking external link clicks, etc.

```jinja2
{% load fathom }
......with link
<a href="https://go-somewhere.com/link" {% click_goal "somewhere_link_clicked" 100 %}>Go somewhere?</a>
......with form
<form method="POST" {% submit_goal "registration_submit" %}>
```

