===================================
django-contentbrowser Documentation
===================================

What is django-contentbrowser?
==============================
ContentBrowser takes a unique approach to having a browser or widget for content
on your django website. A normal workflow that people might be familiar with,
is that you might have a rich text editor like TinyMCE or CKEditor, and you want
to embed a photo into your content.

But django-contentbrowser goes further than this. It takes the approach that
anything can be "content", and you want browse the available content, and
do something with it.

As an example, you might want to create "User Badges" on your website, a simple
contentitem that shows the users' full name, short bio, and photo.

Another Contentitem could be a Single photo in a gallery, or indeed a entire
gallery.

A content item can be *anything* that you want it to be. You just need create
a browser for the item, and take care of some templates and javascript actions.


Before you continue
===================
This project requires quite a bit of work to get everything set up, but once this is done, there
is a lot of benefit. Don't use this on live sites until you have played with it and are comfortable with how the browser works.


Some Requirements
=================
django-appregister
grappelli (Might still work with standard django admin, but I'm making no promises)


The very basics
===============
Assuming you already installed django-contentbrowser on your python path, you
will also need to do the following.

#. Add `'contentbrowser'` to your `INSTALLED_APPS`
#. In your `urls.py` add the following urlpattern:
    `(r'^contentbrowser/', include('contentbrowser.urls')),`


Using the ContentBrowser Widget
===============================
The ContentBrowser is basically a widget that you can add to existing fields.
Note however that it's not a widget on it's own, but a mixin, so you are meant
to use this in conjunction with another widget like `TextArea()` for example:

::
    from django import forms

    class CBWidget(CBWidgetMixin, forms.TextArea):
        pass

    class SomeAdminForm(forms.ModelForm):
        some_field = forms.CharField(widget=CBWidget)
        ...

**Note** that the ContentBrowser widget was built with the django admin in mind.

The code above, if used on a legit model in the admin, will render the contentbrowser just below the actual textarea field. If you open it however you wont see any categories or content. This is because we still need to create and register the Browsers for each of the categories we want.


Create your Browsers
====================
The ContentBrowser is made up of 3 individual parts. The registered browser categories, the template that renders the items, and the javascript event handlers.

As an example, we will build a browser that allows the user to embed a username with a mailto link in the content.

1. Create a content browser
2. Create a render template so that the browser knows how to display your content
3. Create your javascript actions


1. Creating a content browser
-----------------------------
In your main application you need to create a file called `cbitems.py`.
Here we will create "a browser" for each content item or category.

::
    from django.contrib.auth.models import User
    from contentbrowser.core import cbregistry, ContentBrowser

    @cbregistry.register
    class Users(ContentBrowser):
        content_type = 'auth.user'
        title = 'Users'

        def get_items(self, request):
            return User.objects.get()

So we just create a ContentBrowser subclass, decorated with `@cbregistry.register`.
You need to supply the following attributes and methods:

* `content_type`: A unique string for your content type. In our example I'm using the django app/model naming convention. (**Note**: This attribute will be renamed in future versions)
* `title`: A simple title for your type. This is the title for the category in the browser.
* `get_items()`: This returns the list of items to be displayed in your template.


2. Create the render template for items:
----------------------------------------
In your project templates dir create the template, `contentbrowser/browser_items.html`.

This is a single template that will render *all* items for your registered categories.
You basically put your html for the item list in a `{% if %}` block. For example:

::
    {% if ctype == 'auth.user' %}
        <ul>
            {% for user in page.object_list %}
            <li id="user_{{ user.id }}">
                <a href="mailto:{{ user.email }}" onclick="{{ cb }}.takeAction('insert_user', this); return false;">
                    {{ user.username }} ({{ user.firstname }} {{ user.lastname}})
                </a>
            </li>
            {% endfor %}
        </ul>
    {% endif %}


`ctype` is the identifier we registered the item with earlier with the attribute `content_type`. Again this name will change in a future version.

The items that is returned is paginated using django's built in pagination, hence the use of `page.object_list`.

Whatever else you do in the forloop is up to you, since this is just how you specify how you want your list of items to be rendered. In our example we are showing a link with the username, firstname and lastname.

We do however want the contentbrowser to actually *do something* when we click on a username, and this is why we make use of the built in javascript lib.
`{{ cb }}` here is the variable that passes the name of the contnetbrowser javascript object for the current widget.
This object has a function `takeAction()`, which takes two arguments.
First is the name of the action we want to take (more on that in the next section) and second is `self`. (The second is required for a quirk that I've not found a good solution for yet.)


3. Create javascript actions
----------------------------
Next we need to create our javascript actions.
You will need the following file on your STATIC Path: `js/cb_actions.js`

Currently the location for this script is fixed, but in future you will be able to customize the path.

In this script all you need to do is to add the following:

::
    var cb_actions = {

        'insert_user': function(el, target) {
            var mailto = el.attr('href');
            var name = el.html();
            var content = '<a href="' + mailto + '">' + name + '</a>';
            $(target).val($(target).val() + content);
            return false;
        }

    }


And that should be that. (Above example not guaranteed to be bug-free ^_^)


Custom Settings
===============

* CONTENT_BROWSER_RESTRICTED_TO: Restricts which user groups are allowed access to the ContentBrowser view.

.... To be continued ...

