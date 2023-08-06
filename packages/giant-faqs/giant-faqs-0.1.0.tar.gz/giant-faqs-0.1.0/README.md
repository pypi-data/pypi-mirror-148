# Giant-FAQs

A small reusable package that adds a 'Frequently Asked Questions' app to a django site.

This will include the basic formatting and functionality such as model creation via the admin.

Supported Django versions:

    Django 2.2, 3.2

Supported django CMS versions:

    django CMS 3.8, 3.9

## Installation and set up

You should then add "giant_faqs" to the INSTALLED_APPS in your settings file. For use of the RichText plugin needed for the answer entry field on the model, it is required that you use the giant-plugins app.

There is an optional search bar which can be removed from the top of the index template by adding 
    
    FAQ_SEARCH = False

to your project's settings.

