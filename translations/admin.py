from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Word, TranslationVideo, DeletedTranslationVideo, UserVote


class UserVoteInline(admin.TabularInline):
    model = UserVote
    extra = 1


class UserAdmin(BaseUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = ()
        return super().add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = (UserVoteInline,)
        return super().change_view(*args, **kwargs)


class TranslationVideoAdmin(admin.ModelAdmin):
    inlines = (UserVoteInline,)


admin.site.register(User, UserAdmin)
admin.site.register(Word)
admin.site.register(TranslationVideo, TranslationVideoAdmin)
admin.site.register(DeletedTranslationVideo)
admin.site.register(UserVote)
