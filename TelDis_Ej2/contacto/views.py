from django.shortcuts import render
from .forms import ContactoForm

def contacto_view(request):
    msg = None
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Tu mensaje fue enviado correctamente."
            form = ContactoForm()
    else:
        form = ContactoForm()
    return render(request, "contacto.html", {"form": form, "msg": msg})
