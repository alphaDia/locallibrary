from django.contrib import admin
from .models import Book, BookInstance, Genre, Author, Language
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(User, UserAdmin)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0


@admin.register(Book)
class Bookadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    fieldsets = (
        (None, {
            'fields': (
                'book', 'imprint', 'id'
            )
        }),
        ('Availability', {
            'fields': (
                'status', 'due_back', 'borrower'
            )
        })
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    #list_display = ('',)
    inlines = [BookInline]
