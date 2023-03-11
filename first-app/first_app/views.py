from django.shortcuts import render

from .models import DataModel
from .script import main as result

def main(request):
    return render(request, "main.html")

def results(request):
    if request.method == "POST":
        context = {}
        name = request.POST.get("name")
        organization = request.POST.get("org")
        color = request.POST.get("color")
        image = request.FILES.get("image")
        obj = DataModel(name=name, organization=organization, color=color, image=image)
        obj.save()
        context["image"] = obj.image.url
        context["result"] = result(obj.image.url)
        context["color"] = color
        return render(request, "results.html", context=context)