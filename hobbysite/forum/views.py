from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread, ThreadCategory, Comment
from .forms import ThreadForm, CommentForm
from user_management.models import Profile
from django.contrib.auth import get_user_model


User = get_user_model()


def thread_list(request):
    all_threads = Thread.objects.select_related('category').all()

    user_threads = []
    other_threads = all_threads

    if request.user.is_authenticated:
        user_threads = all_threads.filter(author=request.user.profile)
        other_threads = all_threads.exclude(author=request.user.profile)

    categories = ThreadCategory.objects.all()
    categorized_threads = {}
    for category in categories:
        categorized_threads[category] = other_threads.filter(category=category)

    context = {
        'user_threads': user_threads,
        'categorized_threads': categorized_threads,
    }
    return render(request, 'forum/thread_list.html', context)


def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    comments = Comment.objects.filter(thread=thread)
    related_threads = Thread.objects.filter(category=thread.category).exclude(pk=pk)[:2]

    form = CommentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')  # or show error
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user.profile
            comment.save()
            return redirect('forum:thread-detail', pk=pk)

    context = {
        'thread': thread,
        'comments': comments,
        'form': form,
        'related_threads': related_threads
    }
    return render(request, 'forum/thread_detail.html', context)


@login_required
def thread_create(request):
    form = ThreadForm()
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user.profile
            thread.save()
            return redirect('forum:thread-detail', pk=thread.pk)

    context = {"form": form}
    return render(request, 'forum/thread_create.html', context)


@login_required
def thread_edit(request, pk):
    thread = get_object_or_404(Thread, pk=pk)

    if thread.author != request.user.profile:
        return redirect('forum:thread-detail', pk=pk)

    form = ThreadForm(instance=thread)
    if request.method == "POST":
        form = ThreadForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('forum:thread-detail', pk=thread.pk)

    context = {"form": form, "thread": thread}
    return render(request, 'forum/thread_edit.html', context)
