from django.db import models
from django.urls import reverse # Used to generates URLS by reversing the URL patterns.
import uuid #Required for unique book instance.
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genre(models.Model):
    '''Model represent the book genre'''
    name = models.CharField(max_length=200,help_text='Enter a book genre (e.g Science Fiction)')

    def __str__(self):
        """String for representing the Model Objects."""
        return self.name

class Book(models.Model):
    """Model representing the boook but not the specific copy of the book."""
    title =models.CharField(max_length=200)

    #Foreign key used because book can only have one author but author can have multiple books.
    #Auther as string rather than object because it hasnt been declare yet in the file.

    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)

    summary = models.TextField(max_length=1000,help_text='Enter a brief decription of the book')
    isbn = models.CharField('ISBN',max_length=13,unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    #manyToMany Field used because genre can contain many book and book can contain many genre
    #Genre Class has already defined so we can specify the object above.

    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')
    language = models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        '''String representing a Model objects.'''
        return self.title

    def get_absolute_url(self):
        '''Return the URL to access a detail record for this book '''
        return reverse('book-detail',args=[str(self.id)])

    def display_genre(self):
        """Creating the string for the Gerne which is required to display gerne in Admin"""
        return ','.join(genre.name for genre in self.genre.all())

    display_genre.short_description = 'Gerne'

class BookInstance(models.Model):
    """Model representing a specific copy of the book (i.e that can be borrowed from the library)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text='Unique Id for the perticular book for whole library')
    book = models.ForeignKey('Book',on_delete=models.PROTECT,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS,
    blank=True,default='m',help_text='Book Availability',)
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:

        ordering = ['due_back']
        permissions = (("can_mark_returned","Set book as returned"),)

    def __str__(self):
        return f'{self.id}({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    """Model  representing the Authors"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_Birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        """ Returns     the url to access a particular author instance"""
        return reverse('author-detail',args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name},{self.first_name}'

class Language(models.Model):
    """Models representing a Language(i.e English,French...etc)"""
    name =models.CharField(max_length=200,help_text='Enter the book natural Language')

    def __str__(self):
        return self.name
