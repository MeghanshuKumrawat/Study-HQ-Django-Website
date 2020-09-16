from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comment, Profile, Answer, Question


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

BATCH_CHOICE = (
    ('M', 'M-W-F'),
    ('T', 'T-T-S')
)
B_TIME_CHOICE = (
    ('9', '9 PM'),
    ('12', '12 PM')
)
PAYMENT_CHOICE = (
    ('C', 'Cradit card'),
    ('D', 'Debit card'),
    ('P', 'Paytm')
)

class StudentAddForm(forms.Form):
    your_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'}))
    father = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'}))
    address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control'}))
    batch = forms.ChoiceField(choices=BATCH_CHOICE, widget=forms.Select(attrs={
        'class':'custom-select d-block w-100'}))
    batch_time = forms.ChoiceField(choices=B_TIME_CHOICE, widget=forms.Select(attrs={
        'class':'custom-select d-block w-100'}))
    serial_no = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICE)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Promo code',
        'aria-label':'Recipient\'s username', 'aria-describedby':'basic-addon2'
    }))

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control mb-2', 'placeholder':'Write Your Comments Here...'
    }))
    class Meta:
        model = Comment
        fields = ['body']

class ContectUsForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    message = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'description_2', 'category']