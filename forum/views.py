# forum/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Post, Comment, Like, Reply,Dislike, User
from .forms import PostForm,CustomUserCreationForm, ProfileForm
from django.template.defaultfilters import truncatewords
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse



def post_list(request):
    posts = Post.objects.all()
    return render(request, 'forum/post_list.html', {'posts': posts, 'truncatewords': truncatewords,'user': request.user})


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

@login_required
def add_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_authenticated:
        # Ajouter un dislike si l'utilisateur n'a pas déjà disliké
        if not Dislike.objects.filter(post=post, user=request.user).exists():
            Dislike.objects.create(post=post, user=request.user)

    # Supprimer un like si l'utilisateur en avait un
    Like.objects.filter(post=post, user=request.user).delete()

    return redirect('forum')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')  # Remplace 'home' par l'URL de ton choix après connexion
            else:
                form.add_error(None, "Identifiants invalides")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde l'utilisateur
            return redirect('login')  # Redirige vers la page de login après inscription
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

# views.py
from .models import Post, Subscription
from django.shortcuts import get_object_or_404, redirect

@login_required
def subscribe(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.subscriptions.all():
        post.subscriptions.remove(request.user)
        is_subscribed = False
    else:
        post.subscriptions.add(request.user)
        is_subscribed = True

    # Retourner l'état de l'abonnement sous forme de réponse JSON
    return JsonResponse({'is_subscribed': is_subscribed})

@login_required
def profile_view(request):
    user = request.user  # Utilisateur actuel
    
    # Nombre d'abonnés : tous les abonnements où cet utilisateur est suivi
    followers_count = Subscription.objects.filter(user=user).count()
    
    # Nombre d'abonnements : tous les abonnements que cet utilisateur a effectués
    subscriptions_count = Subscription.objects.filter(follower=user).count()
    
    # Récupérer les posts de l'utilisateur
    posts = Post.objects.filter(author=user)  # Remplacer 'user' par 'author'
    
    return render(request, 'forum/profil.html', {
        'user': user,
        'followers_count': followers_count,
        'subscriptions_count': subscriptions_count,
        'posts': posts,
    })

