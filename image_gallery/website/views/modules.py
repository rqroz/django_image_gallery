from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
