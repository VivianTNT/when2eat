from django import forms
from .models import Plan, Person

class PlanCreateForm(forms.ModelForm):
    # Additional fields for user input
    start_time = forms.TimeField(label='start time', widget=forms.TextInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(label='end time', widget=forms.TextInput(attrs={'type': 'time'}))
    people = forms.ModelMultipleChoiceField(label='people',queryset=Person.objects.all(), widget=forms.CheckboxSelectMultiple)
    location = forms.CharField(label='location')

    class Meta:
        model = Plan
        fields = ['location', 'people', 'start_time', 'end_time']
        
class ProfileCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        num_time_slots = kwargs.pop('num_time_slots', None)
        start_time = kwargs.pop('start_time', None)
        half = kwargs.pop('half', None)
        super(ProfileCreateForm, self).__init__(*args, **kwargs)

        if num_time_slots:
            init = 0
            if half:
                init = 1
                num_time_slots += 1
            for i in range(init, num_time_slots):
                field_name = f'{start_time + i // 2:02d}:{30 * (i % 2):02d}'
                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    label=f'{start_time + i // 2:02d}:{30 * (i % 2):02d}'
                )
