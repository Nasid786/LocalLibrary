
from django.shortcuts import render
from django.views.generic.base import TemplateView
from catalog.models import Book,Author,BookInstance,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View

# Create your views here.
def index(request):
    """view function for the home page of the site"""

    """Generate the count of some of the main objects """
    num_books = Book.objects.all().count()
    num_instance =BookInstance.objects.all().count()

    #Available Book (Status = 'a')
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()

    # the 'all()'  is implied by defaults

    num_author = Author.objects.all().count()

    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1

    context = {
            'num_books':num_books,
            'num_instance':num_instance,
            'num_instance_available':num_instance_available,
            'num_author':num_author,
            'num_visits':num_visits
        }

    #return the HTML templates index.html with the data in the context variable

    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    #context_object_name = 'book1_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='Men')[:5] # Get 5 books containing the title war
    #template_name = 'books/book_list.html'  # Specify your own template name/location

    # def get_queryset(self):
    #    return Book.objects.filter(title__icontains='Men')[:5] # Get    5 books containig the title war
    #
    # def get_context_data(self,**kwargs):
    #      #Call the base implementation to get the context
    #     context = super(BookListView,self).get_context_data(**kwargs)
    #    #Create any data and add it to the context
    #
    #     context['some_data'] = 'This is just some data'
    #     return context

class BookDetailedView(generic.DetailView):
    model = Book

    # def book_detail_view(request, primary_key):
    #     try:
    #         book = Book.objects.get(pk=primary_key)
    #     except Book.DoesNotExist:
    #         raise Http404('Book does not exist')
    #
    #     return render(request, 'catalog/book_detail.html', context={'book': book})

    # def book_detail_view(request,primary_key):
    #     book = get_object_or_404(Book,pk=primary_key)
    #     return render(request,'catalog/book_detail.html',context={'book':book})
class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'

class AuthorDetailedView(generic.DetailView):
    model = Author

    # def get_context_data(self,**kwargs):
    #
    #     context = super(AuthorDetailedView,self).get_context_data(**kwargs)
    #     count=Entry.objects.count()
    #     print(count)
    #     return context

# def logout_view(request):
#     return render(request,'registration/logged_out.html')



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class Myview(PermissionRequiredMixin,View):
    permission_required = ('catalog.can_mark_returned')
    