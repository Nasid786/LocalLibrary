from django.contrib import admin
from .models import Genre,Book,Author,BookInstance,Language
# Register your models here.

#define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display=('last_name','first_name','date_of_Birth','date_of_death')
    fields = ['first_name','last_name',('date_of_Birth','date_of_death')]
#Register the admin class with associated model
admin.site.register(Author,AuthorAdmin)
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
#Register the Admin classes for book using decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','display_genre')
    inlines = [BookInstanceInline]
#Register the admin class for Book Instance using decorator
@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display=('id','book','due_back','status','borrower')
    list_filter = ('status','due_back')
    fieldsets = ((None,
                        {'fields':('book','imprint','id')}
                ),
                ('Availability',{'fields':('status','due_back','borrower')}),
                )
admin.site.register(Language)
admin.site.register(Genre)
