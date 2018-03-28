import os.path
from base import Setting, SettingSet
from django.utils.translation import ugettext_lazy as _

UPLOAD_SET = SettingSet('paths', _('File upload settings'), _("File uploads related settings."), 600)

UPFILES_FOLDER = Setting('UPFILES_FOLDER', os.path.join(os.path.dirname(os.path.dirname(__file__)),'upfiles'), UPLOAD_SET, dict(
label = _("Uploaded files folder"),
help_text = _("The filesystem path where uploaded files will be stored. Please note that this folder must exist.")))

UPFILES_ALIAS = Setting('UPFILES_ALIAS', '/upfiles/', UPLOAD_SET, dict(
label = _("Uploaded files alias"),
help_text = _("The url alias for uploaded files. Notice that if you change this setting, you'll need to restart your site.")))

ALLOW_MAX_FILE_SIZE = Setting('ALLOW_MAX_FILE_SIZE', 2.5, UPLOAD_SET, dict(
label = _("Max file size"),
help_text = _("The maximum allowed file size for uploads in mb.")))

 

# UPFACE_SET = SettingSet('paths', _('User face image upload settings'), _("User face image uploads related settings."), 600)

UPFACE_FOLDER = Setting('UPFACE_FOLDER', os.path.join(os.path.dirname(os.path.dirname(__file__)),'upface'), UPLOAD_SET, dict(
label = _("Uploaded user face image folder"),
help_text = _("The filesystem path where uploaded user face images will be stored. Please note that this folder must exist.")))

UPFACE_ALIAS = Setting('UPFACE_ALIAS', '/userface/', UPLOAD_SET, dict(
label = _("Uploaded user face image alias"),
help_text = _("The url alias for uploaded face files. Notice that if you change this setting, you'll need to restart your site.")))


# MEDIA_ROOT = Setting('MEDIA_ROOT', os.path.join(os.path.dirname(os.path.dirname(__file__)),'upface'), UPLOAD_SET, dict(
# label = _("Uploaded user face image folder"),
# help_text = _("The filesystem path where uploaded user face images will be stored. Please note that this folder must exist.")))
# 
# MEDIA_URL = Setting('MEDIA_URL', '/userface/', UPLOAD_SET, dict(
# label = _("Uploaded user face image alias"),
# help_text = _("The url alias for uploaded face files. Notice that if you change this setting, you'll need to restart your site.")))

