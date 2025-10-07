from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ["nombre", "email", "mensaje"]
        widgets = {
        "nombre": forms.TextInput(attrs={"placeholder": "Tu nombre", "required": True}),
        "email": forms.EmailInput(attrs={"placeholder": "tu@email.com", "required": True}),
        "mensaje": forms.Textarea(attrs={"placeholder": "Mensaje...", "rows": 4, "required": True}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if email.endswith("@ejemplo.com"):
            raise forms.ValidationError("Usa un email real")
        return email

    def clean_mensaje(self):
        msg = self.cleaned_data.get("mensaje", "").strip()
        if len(msg) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return msg
