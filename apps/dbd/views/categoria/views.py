from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from apps.dbd.views.mixin.mixin import MixinFormInvalid
from apps.dbd.views.errors.views import Privilegios
from apps.dbd.modelos.estructura_model_catalogo import Categoria
from apps.dbd.forms.categoria.categoria_form import CategoriaForm


class CategoriaListView(LoginRequiredMixin,Privilegios,ListView):
    model = Categoria
    permission_required = "dbd.view_categoria"
    context_object_name = 'categoria_l'
    template_name = "categoria/categoria_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Categorías'
        return context


class CategoriaCreateView(LoginRequiredMixin,MixinFormInvalid,Privilegios,CreateView):
    model = Categoria
    permission_required = "dbd.add_categoria"
    form_class = CategoriaForm
    context_object_name = 'obj'
    template_name = "categoria/categoria_form.html"
    success_url = reverse_lazy('dbd:categoria_list')

    def form_valid(self,form):
        form.instance.usuario_crea = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Creacion de Categoria'
        return context



class CategoriaUpdateView(LoginRequiredMixin,MixinFormInvalid,Privilegios,UpdateView):
    model = Categoria
    permission_required = "dbd.change_categoria"
    form_class = CategoriaForm
    context_object_name = 'obj'
    template_name = "categoria/categoria_form.html"
    success_url = reverse_lazy('dbd:categoria_list')


    def form_valid(self, form):
        form.instance.usuario_modifica =  self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edicion de Categoria'
        return context

class CategoriaDeleteView(LoginRequiredMixin,Privilegios,DeleteView):
    model = Categoria
    permission_required = "dbd.delete_categoria"
    context_object_name = 'obj'
    template_name = "categoria/categoria_delete.html"

    def form_valid(self, form):
        form.instance.usuario_modifica =  self.request.user
        return super().form_valid(form)

    def post(self,request,pk,*args, **kwargs):
        categoria = Categoria.objects.get(id_categoria=pk)
        categoria.estado = False
        categoria.save()
        return redirect('dbd:categoria_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminacion de Categoria'
        return context