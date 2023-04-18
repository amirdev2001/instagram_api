from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model 
from django.core.validators import FileExtensionValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )   
    email = models.EmailField(_('email address'), blank=True)
    phone_number = models.CharField(_("phone number"), blank=True, max_length=11)
    avatar = models.ImageField(upload_to='users/avatar/', blank=True) 
    bio = models.TextField(_("bio"), blank=True)
    website = models.URLField(_("website"), blank=True)
    is_verified = models.BooleanField(_('is verified'),default=False)
    is_private = models.BooleanField(_('is private'), default=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']



    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')



    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.username

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username
    


User = get_user_model()


class BaseModel(models.Model):
    create_time = models.DateTimeField(_("created time") ,auto_now_add=True)
    modified_time = models.DateTimeField(_("modified time") ,auto_now=True)


        
class Location(models.Model):
    title = models.CharField(_("title"), max_length=32)
    points = models.JSONField(_("points")) # sample : {"lat": 48.826265, "long": 2.3262565}


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")


       
class Post(models.Model):
    caption = models.TextField(_('caption'), blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_users')
    locations = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='posts_locations', null=True,blank=True)
    create_time = models.DateTimeField(_("created time") ,auto_now_add=True)
    modified_time = models.DateTimeField(_("modified time") ,auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.user.username, self.id)
    
    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')    

class Comment(models.Model):
    caption = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    create_time = models.DateTimeField(_("created time") ,auto_now_add=True)
    modified_time = models.DateTimeField(_("modified time") ,auto_now=True)

    def __str__(self):
        return self.caption
    
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    create_time = models.DateTimeField(_("created time") ,auto_now_add=True)
    modified_time = models.DateTimeField(_("modified time") ,auto_now=True)

    def __str__(self):
        return "{} >> {}".format(self.user.username, self.post.id)
    

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('likes')



class PostMedia(models.Model):
    IMAGE = 1
    VIDEO = 2

    TYPE_CHOICES = (
        (IMAGE, _('Image')),
        (VIDEO, _('Video')),
    )

    media_type = models.PositiveSmallIntegerField(_('media type'), choices=TYPE_CHOICES, default=IMAGE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    media_file = models.FileField(
        _('media file'), upload_to='content/media', 
        validators=[FileExtensionValidator(allowed_extensions=('mp4', 'png', 'jpg', 'jpeg', 'flv'))]
    )
    create_time = models.DateTimeField(_("created time") ,auto_now_add=True)
    modified_time = models.DateTimeField(_("modified time") ,auto_now=True)

    def __str__(self):
        return "{} - {}".format(str(self.post), self.get_media_type_display())

    class Meta:
        verbose_name = _('post media')
        verbose_name_plural = _('post medias')

class Tag(models.Model):
    title = models.CharField(_('title'), max_length=255)
    create_time = models.DateTimeField(_("created time") ,auto_now_add=True)
    modified_time = models.DateTimeField(_("modified time") ,auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags') 

class PostTag(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='hashtags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return "{} - {}".format(str(self.tag), str(self.post))

    class Meta:
        verbose_name = _('post tag')
        verbose_name_plural = _('post tags')

class TaggedUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagged_users')
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tagged_posts')

    def __str__(self):
        return "{} - {}".format(str(self.user), str(self.Post))
    
    class Meta:
        verbose_name = _('tagged user')
        verbose_name_plural = _('tagged users')                             





class Relation(BaseModel):
    from_user = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{} >> {}".format(self.from_user.username, self.to_user.username)
    
    class Meta:
        verbose_name = _('relation')
        verbose_name_plural = _('relations')
