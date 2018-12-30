from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PdfForm(forms.Form):

    functions = forms.ChoiceField(choices=[('NNPDF21_lo_as_0119_100','NNPDF21_lo_as_0119_100'),('cteq66','cteq66'),('CT10','CT10')],
    widget = forms.Select)
    compare_with = forms.ChoiceField(choices=[('none','none'),('NNPDF21_lo_as_0119_100','NNPDF21_lo_as_0119_100'),('cteq66','cteq66'),('CT10','CT10')],
    widget = forms.Select, required=False)
    Q2 = forms.FloatField(min_value=0.1, max_value=10000000000, initial=100)
    xmin = forms.FloatField(min_value=0.0000000001, max_value=1, initial=0.0001)
    xmax = forms.FloatField(min_value=0.0000000001, max_value=1, initial=1)
    points = forms.IntegerField(min_value=0, max_value=10000, initial=1000)
    ymin = forms.IntegerField(min_value=-100, max_value=100, initial=0)
    ymax = forms.IntegerField(min_value=-100, max_value=100, initial=2)
    g = forms.BooleanField(required=False)
    u = forms.BooleanField(required=False)
    d = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper =FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_id = 'id-PdfForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'form'
        self.helper.add_input(Submit('plot','Plot'))
        super(PdfForm,self).__init__(*args, **kwargs)
