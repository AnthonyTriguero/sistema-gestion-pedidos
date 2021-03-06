from django import forms 
from apps.acts.models import User

class UsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                    'class':'form-control'
                }
            )

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','is_active','groups','image']
        labels = {
            'first_name':'Nombre:',
            'last_name': 'Apellido:',
            'username':'Usuario:',
            'email':'Email:',
            'password':'Contraseña:',
            'is_active':'Estado:',
            'groups':'Permisos:',
            'image':'Imagen:'
        }

        widgets ={
            'password':forms.PasswordInput(
                render_value = True
            )
        }

        exclude = ['user_permissions','last_login','is_superuser','is_staff']

    def clean(self):
        try:
            use = User.objects.get(
                    username = self.cleaned_data["username"]
                )
            if not self.instance.pk:
                raise forms.ValidationError("Registro ya existente")
            elif self.instance.pk != use.pk:
                raise forms.ValidationError("Cambio no Permitido , Ya coincide con otro registro")
        except User.DoesNotExist:
            pass
        return self.cleaned_data 
