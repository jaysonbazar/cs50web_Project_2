from django.contrib import admin

from .models import User, Listing, Comment, Category, Watchlist

# Register your models here.
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id","watchlist")

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist, WatchlistAdmin)