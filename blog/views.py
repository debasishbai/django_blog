from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .models import Post, Comment
from .forms import PostForm, CommentForm, SignUpForm, ContactUsForm


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 12
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


@login_required()
def post_draft_list(request):
    user = request.user
    if user.is_staff:
        posts = Post.objects.filter(published_date__isnull=True).order_by("creation_date")
        return render(request, "blog/post_draft_list.html", {"posts": posts})
    else:
        posts = Post.objects.filter(published_date__isnull=True, author=user).order_by("creation_date")
        return render(request, "blog/post_draft_list.html", {"posts": posts})


@login_required()
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect("post_detail", pk=pk)


@login_required()
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("post_list")


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})


@login_required()
def post_new(request):

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Disabling the published date so that all the new posts will not get published unless approved.
            # post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        greetings = "Registration completed"
        response = ""
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password_2"]
            email_address = form.cleaned_data["email_address"]
            user = User(username=username, email=email_address)
            user.set_password(password)
            user.save()
            return render(request, "registration/success.html", {"greetings": greetings, "response": response})

    else:
        form = SignUpForm()

    return render(request, "registration/sign_up.html", {"form": form})


def success(request):
    return redirect("post_list")


def contact_us(request):

    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email_address = form.cleaned_data["email_address"]
            body = form.cleaned_data["message"]
            subject = "Django Boys Contact This User!"
            to_email_address = User.objects.values_list("email").get(is_superuser=True)
            message = EmailMultiAlternatives(subject=subject, body=body, to=to_email_address, from_email=(name, email_address))
            message.send(fail_silently=False)
            greetings = "Form submitted"
            response = "I will get back to you within 24 hours."
            return render(request, "registration/success.html", {"greetings": greetings, "response": response})

    else:
        form = ContactUsForm()

    return render(request, "registration/contact_us.html", {"form": form})


@receiver(post_save, sender=User)
def send_email_to_new_user(sender, instance, created, **kwargs):
    if created:
        name = User.get_username(instance)
        email_address = User.objects.values_list("email").get(username=name)
        subject = "Welcome to Django Boys"
        team_name = "Django Boys Team"
        html_content = render_to_string('registration/welcome_email.html', {'username': name})
        text_content = strip_tags(html_content)
        message = EmailMultiAlternatives(subject=subject, body=text_content, to=email_address, bcc=["bai.debasish123@gmail.com"], from_email=(team_name))
        message.attach_alternative(html_content, "text/html")
        message.send(fail_silently=False)
