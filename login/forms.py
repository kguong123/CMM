from django import forms
from .models import MyUser

class UserCreationForm(forms.ModelForm): #모델폼 사용
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
 
    class Meta:
        model = MyUser
        fields = ('email', 'nickname','birth')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].help_text=None
            self.fields[field].label=''

        self.fields['nickname'].widget.attrs['placeholder'] = "닉네임"
        self.fields['nickname'].widget.attrs['class'] = "form-control"
        self.fields['password1'].widget.attrs['placeholder'] = "비밀번호"
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs['placeholder'] = "비밀번호 확인"
        self.fields['password2'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['placeholder'] = "exampl@abc.com"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['birth'].widget.attrs['placeholder'] = "2017-01-01"
        self.fields['birth'].widget.attrs['class'] = "form-control"

    
    #패스워드 일치 유효성 검사
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("입력하신 패스워드가 맞지 않습니다.")

        #단순한 패스워드 인지 유효성 검사
        #password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        
        return password2


 
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])#패스워드는 항상 set_password로 입력받음(그래야 암호화를 해서 넘겨줌)
        if commit:
            user.save()
        return user

'''
###20170504_Backup code before update_Change of 'def __init__'###
class UserCreationForm(forms.ModelForm): #모델폼으로 불러옴
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    #패스워드가 맞지 않을때
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput, #별표로 나오게 함
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput,
        strip=False,
    )
    birth = forms.DateField(
        label=_("Birth"),
        widget=forms.TextInput,
        strip=False,
    )

    class Meta:
        model = User #모델이 유저 모델이면
        fields = ("username",) #유저네임만 가져와서 폼필드를 생성함
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': ''})

    ###패스워드 확인의 일치 유효성 검사###
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")#PW1 값가져오기
        password2 = self.cleaned_data.get("password2")#PW2 값가져오기
        if password1 and password2 and password1 != password2:#두개가 입력이 되어있고 and 두개의 암호가 틀릴때
            
            #에러를 낸다
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        #비번이 같을때 정상적으로 출력
        self.instance.username = self.cleaned_data.get('username')#cleaned_data를 사용해 username을 가져와 username에 저장
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)#패스워드도 가져와서 저장하는데 암호가 간단한 것은 아닌지 유효성 검사
        
        #유효성검사가 정상적으로 끝나면 그때 리턴받음
        return password2

    ###저장###
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])#set_password를 통해 입력을 받는다
        if commit:
            user.save()
        return user
'''