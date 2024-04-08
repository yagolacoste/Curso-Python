from django.http import HttpResponse
from django.template import loader
from .models import Member


def members(request):
    mymembers = Member.objects.all().values() ##Crea un mymembersobjeto con todos los valores del Membermodelo.
    template=loader.get_template('all_members.html') ##Carga la all_members.htmlplantilla.
    context = { 
        'mymembers' : mymembers, ##Crea un objeto que contiene el mymembersobjeto.
    }##Envía el objeto a la plantilla.
    return HttpResponse(template.render(context,request)) ##Genera el HTML representado por la plantilla.



def details(request,id):
    mymember=Member.objects.get(id=id)
    template=loader.get_template('details.html')
    context = {
        'mymember':mymember,
    }
    return HttpResponse(template.render(context,request))


def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  template=loader.get_template('templates.html')
  context = {
      'fruits': ['Apple', 'Banana', 'Cherry'],
  }
  return HttpResponse(template.render(context, request))