from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm

from post.models import Post
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile/profile_page.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        post = Post.objects.filter(author_id=self.object.id)
        profile = self.get_object()
        return render(request, self.template_name, {'profile': profile, 'post': post})

    def post(self, request, *args, **kwargs):
        current_user_profile = request.user.profile
        action = request.POST['follow']
        profile = self.get_object()

        if action == 'unfollow':
            current_user_profile.follows.remove(profile)
        elif action == 'follow':
            current_user_profile.follows.add(profile)

        return redirect('profile_page', slug=profile.slug)


class UpdateProfileView(UpdateView, LoginRequiredMixin):
    model = Profile
    template_name = 'profile/update_profile.html'
    form_class = ProfileForm

    def form_valid(self, form):
        self.object.user.first_name = form.cleaned_data['username']
        self.object.user.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.model.objects.get(user__username=self.kwargs['slug'])


@login_required(login_url='login')
def following_list(request):
    user_profile = request.user.profile
    following = user_profile.follows.all()
    return render(request, 'profile/following_list.html', {'following': following})
