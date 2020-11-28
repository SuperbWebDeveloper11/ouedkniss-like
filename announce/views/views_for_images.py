from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# import models
from django.contrib.auth.models import User
from ..models import Announce, Image
from ..forms import ImageForm



class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        current_announce = get_object_or_404(Announce, pk=kwargs['pk'])
        image_list = Image.objects.filter(announce=current_announce)
        context = {'image_list': image_list}
        data['temp'] = render_to_string('announce/image/image_list.html', context, request=request)
        return JsonResponse(data)
 

class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        image_create_temp = 'announce/image/image_create.html'
        if self.badform:
            image_form = self.badform
        image_form = ImageForm()
        context = {'form': image_form, 'announce_pk': kwargs['pk']}
        data['temp'] = render_to_string(image_create_temp, context, request=request)
        return JsonResponse(data)


class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        image_instance = get_object_or_404(Image, pk=kwargs['image_pk'])
        if self.badform:
            image_form = self.badform
        image_form = ImageForm(instance=image_instance)
        context = {'form': image_form, 'announce_pk': kwargs['pk']}
        data['temp'] = render_to_string('announce/image/image_update.html', context, request=request)
        return JsonResponse(data)


class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        image_instance = get_object_or_404(Image, pk=kwargs['image_pk'])
        image_form = ImageForm(instance=image_instance)
        context = {'form': image_form, 'announce_pk': kwargs['pk']}
        data['temp'] = render_to_string('announce/image/image_delete.html', context, request=request)
        return JsonResponse(data)


################## images crud views ################## 

class ImageList(RenderListTempMixin, View):
    pass
    

class ImageCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid(): 
            current_announce = get_object_or_404(Announce, pk=kwargs['pk'])
            form.instance.announce = current_announce
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


class ImageUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        current_announce = get_object_or_404(Announce, pk=kwargs['pk'])
        image_instance = Image.objects.get(announce=current_announce, pk=kwargs['image_pk'])
        form = ImageForm(request.POST, request.FILES, instance=image_instance)
        if form.is_valid():
            if not request.user == image_instance.announce.owner:
                return HttpResponse('You can not edit this image')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


class ImageDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        image_instance = get_object_or_404(Image, pk=kwargs['image_pk'])
        if not request.user == image_instance.owner:
            return HttpResponse('You can not delete this image')
        image_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)

