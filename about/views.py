from django.shortcuts import render
from .models import About


def about_me(request):
    """
    Renders content for the About page.
    Displays and individual instance of :model: `about.About`
    **Context**
    ``about``
        The most recent instance of :model:`about.About`.
    
    **Template**
    :template:`about/about.html`
    """
    about = About.objects.all().order_by('-updated_on').first()

    return render(
        request,
        "about/about.html",
        {"about": about},
    )