from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from gameofthrones.models import CharacterInfo, CharacterFamilyTie

class CharacterInfoForm(forms.ModelForm):

    class Meta:
        model = CharacterInfo
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'submit'))


CharacterFormSet = forms.inlineformset_factory(CharacterInfo, CharacterFamilyTie, 
                   fk_name='character1', fields=('character2', 'relation_type', 'biological_type', ), extra=1)

# CharacterFormSet = forms.inlineformset_factory(CharacterInfo, CharacterFamilyTie, 
#                    fk_name='character1', fields=('character2', 'relation_type', 'biological_type', ), extra=1)

class RelationForm(forms.ModelForm):
    class Meta:
        model = CharacterFamilyTie
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'submit'))