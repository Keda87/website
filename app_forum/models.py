from django.db import models
from markdownx.models import MarkdownxField

from app_author.models import Profile


class Category(models.Model):
    """
    Category Model
    """
    id = models.AutoField(
        primary_key=True
    )

    category_title = models.CharField(
        max_length=200,
        verbose_name=u'Category Name',
        blank=False,
        null=False
    )

    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.category_title)

    def save(self, **kwargs):
        if not self.slug:
            from djangoid.utils import get_unique_slug
            self.slug = get_unique_slug(instance=self, field='category_title')
        super(Category, self).save(**kwargs)

    def get_absolute_url(self):
        """
        Call Category Slug
        """
        return 'app_forum:category'


class Forum(models.Model):
    """
    Thread Model
    """
    forum_author = models.ForeignKey(
        Profile,
        related_name='user_forums',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    forum_title = models.CharField(
        max_length=225,
        verbose_name=u'Title',
        blank=False,
        null=False
    )

    forum_category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name=u'Category',
    )

    forum_content = MarkdownxField(
        verbose_name=u'Content (Use Markdown)',
    )

    is_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    is_modified = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    is_hot = models.BooleanField(
        default=False
    )

    is_closed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return str(self.forum_title)

    def latest_comment_author(self):
        return self.forum_comments.latest('is_created').comment_author

    def latest_comment_date(self):
        return self.forum_comments.latest('is_created').is_created

    def get_absolute_url(self):
        """
        Call Forum ID
        """
        return 'app_forum:forum'


class Comment(models.Model):
    """
    Comment Model
    """
    forum = models.ForeignKey(
        'Forum',
        on_delete=models.CASCADE,
        related_name='forum_comments'
    )

    comment_author = models.ForeignKey(
        Profile,
        related_name='user_comments',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    comment_content = MarkdownxField(
        verbose_name=u'Markdown',
    )

    is_created = models.DateTimeField(
        auto_now_add=True,
    )

    is_modified = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.comment_content
