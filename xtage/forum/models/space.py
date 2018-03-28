from django.db import models
from base import * 

class Space(BaseModel):
    space_name = models.CharField(max_length=64, default='General')

    @models.permalink    
    def get_absolute_url(self):
        return ('space', (), {'id': self.id, 'slug': django_urlquote(slugify(self.space_name))})

    def __unicode__(self):
        return self.space_name 