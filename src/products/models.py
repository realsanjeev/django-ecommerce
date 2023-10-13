from django.db import models

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Out wear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class products(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES)
    label = models.CharField(choices=LABEL_CHOICES)
    slug = models.SlugField()
    image = models.ImageField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        '''absolute url of a product'''
        return 
    
    