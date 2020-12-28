import logging
from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm, DiaryCreateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Diary

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = 'index.html'

class InquiryView(generic.FormView):
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self,form):
        form.send_email()
        messages.success(self.request,  'Your message has been sent')
        logger.info('inquiry send by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

# LoginRequiredMixin はlogin状態でないとアクセスできないようにするクラス
class DiaryListView(LoginRequiredMixin,generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    paginate_by = 2

    def get_query_set(self):
        diaries = Diary.objects.filter(user = self.request.user).order_by('created_at')
        return diaries

class DiaryDetailView(generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'

class DiaryCreateView(LoginRequiredMixin,generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self,form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request,  'Your diary has been created')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Failed to create your diary')
        return super().form_invalid(form)
