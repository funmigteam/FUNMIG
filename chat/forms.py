from django import forms


from .models import ChatGroup, ChatMessage


class CreateGroupForm(forms.ModelForm):


    class Meta:


        model = ChatGroup


        fields = ['name', 'group_type', 'is_private']


        widgets = {


            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام گروه یا چنل را وارد کنید...'}),


            'group_type': forms.HiddenInput(),


            'is_private': forms.HiddenInput(),


        }


class InviteUserForm(forms.Form):


    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری را وارد کنید...'}))


