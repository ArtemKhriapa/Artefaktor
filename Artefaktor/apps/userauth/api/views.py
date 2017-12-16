from django.shortcuts import get_object_or_404
from rest_framework import generics
from apps.userauth.api.serializers import SomeSerializer
from django.shortcuts import HttpResponse


def RegistrationViev(request):
    return HttpResponse(request, "You're looking at REG %s.")



'''def post_list(request):
    return render(request, 'blog/post_list.html', {})'''