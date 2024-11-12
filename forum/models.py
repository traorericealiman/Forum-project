from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Post
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Utilisation de 'author' ici
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Champ image
    subscriptions = models.ManyToManyField(User, related_name='subscribed_posts', blank=True)

    def __str__(self):
        return self.title

    def get_like_count(self):
        return self.likes.count()

# Commentaire
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 'user' au lieu de 'author'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"  # Utilisation de 'self.user'

# Réponse au commentaire
class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Champ pour l'image


    def __str__(self):
        return f"Reply by {self.author} on {self.comment}"

# Like
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like by {self.user.username} on {self.post.title}'

# Dislike
class Dislike(models.Model):
    post = models.ForeignKey(Post, related_name='dislikes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')  # Empêcher un utilisateur de disliker plusieurs fois un post

    def __str__(self):
        return f'Dislike by {self.user.username} on {self.post.title}'

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null=True, blank=True)  # Permettre NULL

    class Meta:
        unique_together = ('user', 'post')  # Un utilisateur ne peut s'abonner qu'une seule fois à un post

    def __str__(self):
        return f'{self.user.username} abonné à {self.post.title}'


class CustomUser(AbstractUser):
 # Champ pour la photo de profil
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Méthode __str__ pour afficher le nom d'utilisateur
    def __str__(self):
        return self.username

    # Ajoute des `related_name` pour éviter les conflits de relations
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Change le `related_name` pour éviter le conflit
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Change le `related_name` pour éviter le conflit
        blank=True,
    )