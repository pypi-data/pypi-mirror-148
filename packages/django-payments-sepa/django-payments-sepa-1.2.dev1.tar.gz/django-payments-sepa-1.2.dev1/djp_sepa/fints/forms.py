from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from fints.formals import AllowedFormat


class FinTSForm(forms.Form):
    def get_session_data(self):
        return self.cleaned_data


class AccountForm(FinTSForm):
    account = forms.ChoiceField(label=_("Account"))

    def __init__(self, accounts, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["accounts"].choices = list(enumerate(accounts))


class BankCredentialsForm(FinTSForm):
    bank_id = forms.CharField(label=_("Bank ID"))
    login_name = forms.CharField(label=_("Login name"))
    pin = forms.CharField(label=_("PIN"), widget=forms.PasswordInput)
    hbci_url = forms.URLField(label=_("HBCI URL"))


class TANForm(FinTSForm):
    tan = forms.CharField(label=_("TAN"))

    def __init__(self, response, mechanism, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tan"].max_length = mechanism.max_length_input
        if mechanism.allowed_format == AllowedFormat.NUMERIC:
            self.fields["tan"].validators.append(RegexValidator(r"^[0-9]+$"))
        elif mechanism.allowed_format == AllowedFormat.ALPHANUMERIC:
            self.fields["tan"].validators.append(RegexValidator(r"^[A-Za-z0-9]+$"))

    def get_session_data(self):
        return {}


class TANMechanismForm(FinTSForm):
    tan_mechanism = forms.ChoiceField(label=_("TAN mechanism"))

    def __init__(self, mechanisms, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tan_mechanism"].choices = [
            (mech.security_function, mech.name) for mech in mechanisms.values()
        ]


class TANMediumForm(FinTSForm):
    tan_medium = forms.ChoiceField(label=_("TAN medium"))

    @staticmethod
    def _medium_str(medium):
        tan_medium_detail = (
            medium.mobile_number or medium.card_number or medium.tan_list_number or ""
        )
        return f"{medium.tan_medium_name} {tan_medium_detail}"

    def __init__(self, media, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tan_medium"].choices = [
            (index, self._medium_str(medium)) for index, medium in enumerate(media[1])
        ]
