from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Pages
import barrapunto

# Create your views here.

bp = ""

def mostrar(request, recurso):
    #SOLO PUEDES HACER POST SI ESTAS AUTENTICADO
    if request.user.is_authenticated():
        salida = "Eres " + request.user.username + " " + "<a href='/logout'>logout</a>.  Puedes cambiar la page mediante un PUT<br><br>"
        if request.method == "PUT":
            p = Pages(name=recurso, page=request.body)
            p.save()
            return HttpResponse("guardada pagina, haz un get para comprobar")        
    else:
        salida = "No estas logueado <a href='/admin/login/'>Login</a>. No puedes cambiar la page<br><br>"
    

    try:
        fila = Pages.objects.get(name=recurso)
        salida += request.method + " " + str(fila.id) + " " + fila.name + " " + fila.page
        salida += "<br><hr>" + bp
        return HttpResponse(salida)
    except Pages.DoesNotExist:
        salida += "Page not found: " + recurso
        return HttpResponseNotFound(salida)


def todo(request):
    if request.user.is_authenticated():
        salida = "Eres " + request.user.username + " " + "<a href='/logout'>logout</a><br><br>"
    else:
        salida = "No estas logueado <a href='/admin/login/'>Login</a><br><br>"
            
    lista = Pages.objects.all()
    salida += "Esto es lo que tenemos:<ul>"
    for fila in lista:
        salida += "<li>" + fila.name + "->" + str(fila.page) + " "
    salida += "</ul>"
    salida += "<br><hr>" + bp
    return HttpResponse(salida)


def actualizarbp(request):
    global bp 
    bp = barrapunto.get_bp()
    return HttpResponse("Actualizado bp:   " + bp)


