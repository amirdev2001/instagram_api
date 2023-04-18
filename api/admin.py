from django.contrib import admin

from .models import User, Post, Location, Comment, Like, PostMedia, PostTag, Tag, TaggedUser, Relation

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostMedia)
admin.site.register(Tag)
admin.site.register(Location)
admin.site.register(PostTag)
admin.site.register(TaggedUser)
admin.site.register(Relation)