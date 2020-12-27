from django import forms
from django.core.mail import EmailMessage

class InquiryForm(forms.Form):
    name = forms.CharField(label = "name", max_length =30)
    email = forms.EmailField(label = "email address")
    title = forms.CharField(label = "title")
    message = forms.CharField(label = "message", widget = forms.Textarea)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'enter your name'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'enter your email-address'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'enter email title'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'enter your message'


    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'inquiry{}'.format(title)
        message = 'sender:{0}\nmailaddress:{1}\nmessage:\n{2}'.format(name,email,message)
        from_email = 'admin@example.com'
        to_list = [
            'text@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject = subject,body = message, from_email = from_email, to = to_list, cc = cc_list)
        message.send()