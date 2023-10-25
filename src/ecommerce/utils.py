import random
import string

from django.utils.text import slugify

def random_string_generator(size=10):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(size))

def unique_slug_generator(instance, new_slug: str=None):
    '''Generate uniuqe slug for a instance'''
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}--{random_string_generator(size=4)}"

        # check if slug already exists
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
