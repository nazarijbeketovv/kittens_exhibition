from django.contrib import admin
from .models import Breed, Kitten, Rating
from django.db import models


# 1. Админка для модели Breed
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ()


# 2. Админка для модели Kitten с инлайн-редактированием рейтингов
class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1  # Количество пустых форм для добавления новых рейтингов
    readonly_fields = ("user",)
    can_delete = False
    show_change_link = True


@admin.register(Kitten)
class KittenAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "color", "age", "added_by", "average_rating")
    search_fields = ("name", "description")
    list_filter = ("breed", "color", "age", "added_by")
    readonly_fields = ("average_rating",)
    raw_id_fields = ("added_by",)
    list_select_related = ("breed", "added_by")
    inlines = [RatingInline]

    def average_rating(self, obj):
        return obj.ratings.aggregate(models.Avg("score"))["score__avg"] or 0

    average_rating.short_description = "Средний рейтинг"


# 3. Админка для модели Rating
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("kitten", "user", "score")
    search_fields = ("kitten__name", "user__username")
    list_filter = ("score",)
    raw_id_fields = ("kitten", "user")
    list_select_related = ("kitten", "user")
