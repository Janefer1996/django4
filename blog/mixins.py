from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from blog.models import Comment, Post

def get_post_data(post_data):
    """Вернуть данные поста."""
    post = get_object_or_404(
        Post,
        pk=post_data["pk"],
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )
    return post


class CommentMixinView(LoginRequiredMixin, View):
    """Mixin для редактирования и удаления комментария"""

    model = Comment
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_pk"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", pk=self.kwargs["pk"])
        get_post_data(self.kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("blog:post_detail", kwargs={"pk": pk})