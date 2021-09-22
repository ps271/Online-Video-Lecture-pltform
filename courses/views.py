from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Video, Comment, Category
from .forms import CommentForm
from django.http import JsonResponse
import json

# Create your views here.
class Index(LoginRequiredMixin, ListView):
	model = Video
	template_name = 'courses/index.html'
	order_by = '-date_time'

class UserUploads(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'courses/user_uploads.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Video.objects.filter(uploader=user).order_by('-date_time')
    
    


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['caption', 'video_description', 'video_file', 'thumbnail', 'category']
    template_name = 'courses/create_video.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('courses:video-detail', kwargs={'pk': self.object.pk})



class DetailVideo(View):
    def get(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm()
        comments = Comment.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:15]

        context = {
            'object': video,
            'comments': comments,
            'form': form,
            'categories': categories
        }
        return render(request, 'courses/detail_video.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                user=self.request.user,
                comment=form.cleaned_data['comment'],
                video=video
            )
            comment.save()

        comments = Comment.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:15]

        context = {
            'object': video,
            'comments': comments,
            'form': form,
            'categories': categories
        }
        return render(request, 'courses/detail_video.html', context)

class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['caption', 'video_description']
    template_name = 'courses/create_video.html'

    def get_success_url(self):
        return reverse('courses:video-detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader

class DeleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'courses/delete_video.html'

    def get_success_url(self):
        return reverse('courses:home')
    
    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader

class VideoCategoryList(View):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        videos = Video.objects.filter(category=pk).order_by('-date_time')
        context = {
            'category': category,
            'videos': videos
        }

        return render(request, 'courses/video_category.html', context)

class VideoSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        query_list = Video.objects.filter(
            Q(caption__icontains = query) |
            Q(video_description__icontains=query) |
            Q(uploader__username__icontains=query)
        )

        context = {
            'query_list': query_list
        }

        return render(request, "courses/video_search.html", context)

class Like(View):
    template_name = "courses/detail_video.html"
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'post' and request.is_ajax():
            result = ''
            pk = json.loads(request.POST.get('videoid'))
            video = get_object_or_404(Video, pk = pk)
            if video.likes.filter(pk=request.user.pk):
                video.likes.remove(request.user)
                video.like_count -= 1
                result = video.like_count
                video.save()
            else:
                video.likes.add(request.user)
                video.like_count += 1
                result = video.like_count
                video.save()
            return JsonResponse({'result': result})
