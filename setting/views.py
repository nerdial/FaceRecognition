from django.shortcuts import render

from .models import ProjectSetting

def all_settings(request):
    if request.method == "POST":
        confidence = request.POST.get('confidence')
        algorithm = request.POST.get('recognition_algorithm')
        setting = ProjectSetting.objects.first()
        setting.confidence = confidence
        setting.recognition_algorithm = algorithm
        setting.save()
    setting = ProjectSetting.objects.filter().first()
    return render(request, 'setting/index.html', {'setting': setting})