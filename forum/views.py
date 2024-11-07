# forum/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like, Reply
from .forms import PostForm
from django.template.defaultfilters import truncatewords
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'forum/post_list.html', {'posts': posts, 'truncatewords': truncatewords})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Créer le commentaire
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            # Rediriger vers la page du post après avoir commenté
            return redirect('post_detail', post_id=post.id)

    return redirect('post_list')  # Si la méthode n'est pas POST, rediriger vers la liste des posts
        
# forum/views.py
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Vérifier si l'utilisateur a déjà liké ce post
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        # Si l'utilisateur a déjà liké, on le supprime (délike)
        like.delete()

    # Rediriger vers la page du post après avoir liké
    return redirect('post_detail', post_id=post.id)


@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            # Créer la réponse
            reply = Reply.objects.create(comment=comment, author=request.user, content=content)
            return redirect('post_list')  # Rediriger vers la page du post ou la liste des posts
    return redirect('post_list')  # Si la méthode n'est pas POST, rediriger vers la liste des posts

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Important de passer request.FILES
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Rediriger vers la liste des posts
    else:
        form = PostForm()

    return render(request, 'forum/add_post.html', {'form': form})