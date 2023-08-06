from wtforms import StringField, BooleanField
from wtforms.widgets import PasswordInput
from indico.web.forms.base import IndicoForm
from indico.web.forms.widgets import SwitchWidget

from indico_wp import _

class SettingsForm(IndicoForm):
    enabled = BooleanField(_("Enabled"), widget=SwitchWidget())
    wp_url = StringField(_("Wordpress URL"))
    wp_username = StringField(_("Username"))
    wp_application_password = StringField(_("Application Password"))
    wp_category_maps = StringField(_("Category maps"))

class EventSettingsForm(IndicoForm):
    enabled = BooleanField(_("Enabled"), widget=SwitchWidget())
