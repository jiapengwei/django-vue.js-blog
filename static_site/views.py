# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, HttpResponseRedirect

# Create your views here.
from django.views.generic import TemplateView, DetailView, ListView
import markdown

from RaPo3.settings import HOST
from api.models import Article
from core.Mixin.CheckMixin import CheckAdminPagePermissionMixin, CheckAdminPermissionMixin


class BlogView(DetailView):
    http_method_names = ['get']
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'aid'
    model = Article

    def get_context_data(self, **kwargs):
        kwargs = super(BlogView, self).get_context_data(**kwargs)
        kwargs['host'] = HOST
        article = kwargs['article']
        article.content = markdown.markdown(article.content)
        kwargs['article'] = article
        return kwargs


class BlogListView(ListView):
    http_method_names = ['get']
    template_name = 'blog/list.html'
    model = Article

    def get_context_data(self, **kwargs):
        kwargs = super(BlogListView, self).get_context_data(**kwargs)
        kwargs['host'] = HOST
        return kwargs

    def get_queryset(self):
        queryset = super(BlogListView, self).get_queryset()
        queryset = queryset.order_by("-create_time")
        map(self.get_summary, queryset)
        return queryset

    def get_summary(self, article):
        setattr(article, 'summary', markdown.markdown(article.content[:400]))


class IndexView(ListView):
    http_method_names = ['get']
    template_name = 'blog/index.html'
    model = Article

    def get_context_data(self, **kwargs):
        kwargs = super(IndexView, self).get_context_data(**kwargs)
        kwargs['host'] = HOST
        return kwargs

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        queryset = queryset.order_by("-create_time")
        return queryset


class AboutView(TemplateView):
    http_method_names = ['get']
    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AboutView, self).get_context_data(**kwargs)
        kwargs['host'] = HOST
        return kwargs


class AdminLoginView(CheckAdminPermissionMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'admin/admin_login.html'

    def get(self, request, *args, **kwargs):
        if self.wrap_check_token_result():
            return HttpResponseRedirect('/admin/index')
        return super(AdminLoginView, self).get(request, *args, **kwargs)


class AdminIndexView(CheckAdminPagePermissionMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'admin/admin_index.html'


class AdminArticleListView(CheckAdminPagePermissionMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'admin/article.html'


class AdminCommentListView(TemplateView):
    http_method_names = ['get']
    template_name = 'admin/comment.html'


class AdminModifyArticleView(CheckAdminPagePermissionMixin, DetailView):
    http_method_names = ['get']
    template_name = 'admin/modify_article.html'
    model = Article
    pk_url_kwarg = 'aid'

    def get_object(self, queryset=None):
        if not self.kwargs.get(self.pk_url_kwarg, None):
            return None
        return super(AdminModifyArticleView, self).get_object(queryset)


class EmailView(TemplateView):
    http_method_names = ['get']
    template_name = 'email.html'

    def get_context_data(self, **kwargs):
        context = super(EmailView, self).get_context_data(**kwargs)
        context['article'] = Article.objects.all()[0]
        context['guest'] = Article.objects.all()[0]
        return context
