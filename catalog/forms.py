from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
import catalog.models as models
# Write your forms here


class RenewaBookForm(ModelForm):
    class Meta:
        model = models.BookInstance
        fields = ('due_back',)
        label = {'due_back': _('New renewal date')}
        help_text = {'due_back': _(
            'Enter a date between now an 4 weeks (default 3). ')}

    def clean_due_back(self):
        date = self.cleaned_data.get('renewal_date')

        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        return date


class CreateAuthorForm(ModelForm):
    class Meta:
        model = models.Author
        fields = '__all__'
