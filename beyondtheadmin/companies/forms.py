# -*- coding: utf-8 -*-
from django.forms.models import ModelForm

from colorfield.widgets import ColorWidget

from .models import Company


class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = '__all__'

        widgets = {
            'contrast_color': ColorWidget(),
        }
