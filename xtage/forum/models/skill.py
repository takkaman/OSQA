from django.db import models
from user import User
from base import BaseModel
import django.utils.timezone as timezone

class Skill(BaseModel):
	skillname = models.CharField(max_length=64)
	owner = models.ManyToManyField(User, through = 'Skillownership', blank = True)
	last_update_at = models.DateTimeField(default = timezone.now)
	popularity = models.IntegerField(default = 0)
	def __unicode__(self):
		return self.skillname 

class Skillownership(models.Model):
	skill = models.ForeignKey('Skill')
	owner = models.ForeignKey(User)
	time =  models.DateTimeField()
	adores = models.ManyToManyField(User, related_name = 'skilladorers', blank = True)
	adore_num = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return  self.owner.username + ' - ' + self.skill.skillname
	
	class Meta:
		unique_together = (("skill", "owner"),)
		app_label = 'forum'
