from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit

from .models import Invoice


class BaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("company", "client")

    def __init__(self, *args, **kwargs):
        companies = kwargs.pop("companies", None)
        clients = kwargs.pop("clients", None)
        super().__init__(*args, **kwargs)
        if companies is not None:
            self.fields["company"].queryset = companies
        if clients is not None:
            self.fields["client"].queryset = clients
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", _("Submit")))


class InvoiceStatusForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("status",)
        widgets = {"status": forms.HiddenInput}

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.include_media = False
        self.helper.layout = Layout(
            "status",
            Div(
                Submit("save", _("Save")),
            ),
        )


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False

        self.helper.layout = Layout(
            "subject",
            "message",
            Div(
                Submit("save", _("Send")),
            ),
        )
