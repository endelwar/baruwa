from django import forms
from django.forms.util import ErrorList
import re

LIST_OPTIONS = (
  ('1', 'Whitelist'),
  ('2', 'Blacklist'),
)

class UserListAddForm(forms.Form):
    from_address = forms.EmailField()
    to_address = forms.EmailField()
    list_type = forms.ChoiceField(choices=LIST_OPTIONS)

class ListAddForm(forms.Form):
    from_address = forms.EmailField()
    to_address = forms.CharField(required=False)
    to_domain = forms.CharField(required=False)
    list_type = forms.ChoiceField(choices=LIST_OPTIONS)

    def clean_to_address(self):
        to = self.cleaned_data['to_address']
        if to == "" or to is None:
            to = "default"
        else:
            to = to.strip()
            r = re.compile(r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
                r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*")', re.IGNORECASE)
            if not r.match(to):
                raise forms.ValidationError('%s is not a valid user part of an email address',to)
        return to
    
    def clean_to_domain(self):
        domain = self.cleaned_data['to_domain']
        domain = domain.strip()
       
        if domain != "" and not domain is None:
            r = re.compile(r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)
            if not r.match(domain):
                raise forms.ValidationError('provide a valid domain')
        return domain

    def clean(self):
        cleaned_data = self.cleaned_data
        to_user = cleaned_data.get("to_address")
        to_domain = cleaned_data.get("to_domain")

        if to_user != 'default' and to_domain == '':
            error_msg = u"Must provide domain name."
            self._errors["to_domain"] = ErrorList([error_msg])
            del cleaned_data["to_domain"]
            del cleaned_data["to_address"]
        return cleaned_data

class FilterForm(forms.Form):
    query_type = forms.ChoiceField(choices=((1,'containing'),(2,'excluding')))
    search_for = forms.CharField(required=False)
