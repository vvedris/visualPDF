from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

class PdfForm(forms.Form):

    """creates crispy_forms that gathers data needed for dynamically serving images"""
    choice = [('cteq66','cteq66'),('MSTW2008nlo_asmzrange','MSTW2008nlo_asmzrange'),('NNPDF23_nlo_as_0118','NNPDF23_nlo_as_0118'),('abkm09_3_nlo','abkm09_3_nlo')]
    functions = forms.ChoiceField(choices = choice,
    widget = forms.Select)
    compare_with = forms.ChoiceField(choices = [('none','none')]+choice,
    widget = forms.Select, required=False)
    fixed = forms.ChoiceField(choices=[('Q fixed','Q fixed'),('x fixed','x fixed')], widget = forms.RadioSelect(), initial = 'Q fixed')
    Q2 = forms.FloatField(initial=100)
    xmin = forms.FloatField(initial=0.0001)
    xmax = forms.FloatField(initial=1)
    points = forms.IntegerField(min_value=0, max_value=10000, initial=1000)
    ymin = forms.IntegerField(min_value=-100, max_value=100, initial=0)
    ymax = forms.IntegerField(min_value=-100, max_value=100, initial=2)
    g = forms.BooleanField(required=False)
    u = forms.BooleanField(required=False)
    d = forms.BooleanField(required=False)
    scale = forms.ChoiceField(choices=[('lin','lin'),('log','log')], widget = forms.RadioSelect(), initial = 'log')
    error = forms.ChoiceField(choices=[('clean','clean'),('error','error')], widget = forms.RadioSelect(), initial = 'clean')

    def __init__(self, *args, **kwargs):
        """crispy_forms helper functions that manages form layout and design"""
        super(PdfForm,self).__init__(*args, **kwargs)
        self.helper =FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_id = 'id-PdfForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'form'
        self.helper.layout = Layout(
            Row(
                Column('functions', css_class="form-group mx-sm-1"),
                Column('compare_with', css_class="form-group mx-sm-1"),
                css_class='form-row'
            ),
            Row(
                Column('fixed', css_class="form-check mx-sm-1"),
                Column('Q2', css_class="form-check mx-sm-1"),
                css_class='form-row'
                ),
            Row(
                Column('xmin', css_class="form-group mx-sm-1"),
                Column('xmax', css_class="form-group mx-sm-1"),
                Column('points', css_class="form-group mx-sm-1"),
                css_class='form-row'
            ),
            Row(
                Column('ymin', css_class="form-group mx-sm-1"),
                Column('ymax', css_class="form-group mx-sm-1"),
                css_class='form-row'
                ),
            Row(
                Column('g', css_class='form-check mx-sm-1'),
                Column('u', css_class='form-check mx-sm-1'),
                Column('d', css_class='form-check mx-sm-1'),
                css_class='form-row'
            ),
            Row(
                Column('scale', css_class='form-check mx-sm-1'),
                Column('error', css_class='form-check mx-sm-1'),
                css_class='form-row'
            )
        )
        self.helper.add_input(Submit('plot','Plot'))
