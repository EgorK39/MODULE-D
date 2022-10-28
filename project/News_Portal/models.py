from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rankingAuthor = models.FloatField(default=0.0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('ranking'))
        pRat = 0.0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('comment_ranking'))
        cRat = 0.0
        cRat += commentRat.get('commentRating')

        self.rankingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return str(self.authorUser)


class Category(models.Model):
    categoryName = models.CharField(max_length=82, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.categoryName


Artikel = "Artikel"
Nachricht = "Nachricht"
AUFLISTUNG = [
    (Artikel, "Статья"),
    (Nachricht, "Новость")
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    Wahl = models.CharField(max_length=16, choices=AUFLISTUNG, default=Artikel)
    titel_name = models.CharField(max_length=212)
    text = models.TextField()
    ranking = models.FloatField(default=0.0)
    time_in = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.ranking += 0.1
        self.save()

    def dislike(self):
        self.ranking -= 0.1
        self.save()

    def preview(self):
        return f"{self.text[0:124]}+ ..."

    def __str__(self):
        return f'{self.titel_name}'

    def get_absolute_url(self):
        if self.Wahl == 'Nachricht':
            return reverse('new', args=[str(self.id)])
        else:
            return reverse('article', args=[str(self.id)])


class PostCategory(models.Model):
    PostBeziehung = models.ForeignKey(Post, on_delete=models.CASCADE)
    CategoryBeziehung = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    comment_ranking = models.FloatField(default=0.0)

    def like(self):
        self.comment_ranking += 0.1
        self.save()

    def dislike(self):
        self.comment_ranking -= 0.1
        self.save()
