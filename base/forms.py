from django.forms import ModelForm
from .models import Room,Message




class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["name","topic","description"]


    def __init__(self, *args, **kwargs):
        super(RoomForm,self).__init__(*args,**kwargs)

        self.fields["name"].widget.attrs.update({'class':'form__group-input'})
        self.fields["topic"].widget.attrs.update({'class':'form__group-input'})
        self.fields["description"].widget.attrs.update({'class':'form__group-textarea'})
