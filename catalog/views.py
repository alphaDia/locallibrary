from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookInstance, Genre, Author, BookInstance
from django.views import generic, View
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib import messages
from .forms import RenewaBookForm
import datetime
from django.urls import reverse_lazy
from .forms import CreateAuthorForm


@permission_required('can_renew')
def renew_book_librairian(request, id):
    book_instance = get_object_or_404(BookInstance, id=id)
    print(book_instance)

    if request.method == 'POST':
        form = RenewaBookForm(request.POST)

        if form.is_valid():
            date = form.cleaned_data.get('renewal_date')
            book_instance.due_back = date
            book_instance.save()

            return redirect('borrowed')
    else:
        proposed_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewaBookForm(initial={'due_back': proposed_date})

    context = {'form': form, 'book_instance': book_instance}

    return render(request, 'catalog/book_renew_librarian.html', context)


@login_required
@permission_required(('catalog.can_mark_returned'))
def index(request):
    "View function for home page of site"

    # Generate counts of some of the main objects
    number_books = Book.objects.all().count()
    number_instances = BookInstance.objects.all().count()

    # Available books (ie: status = 'a)
    number_instances_available = BookInstance.objects.filter(
        status__iexact='a').count()
    # All authors

    number_authors = Author.objects.count()

    number_genres = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable
    visits = request.session.get('visits', 0)
    request.session['visits'] = visits+1
    if visits >= 5:
        request.session['visits'] = 0
        request.session.modified = True

    # All genres
    # keys in the context object are variables in template
    context = {
        'number_books': number_books,
        'number_instances': number_instances,
        'number_instances_available': number_instances_available,
        'number_authors': number_authors,
        'number_genres': number_genres,
        'title': 'Home',
        'visits': visits
    }

    return render(request, 'catalog/index.html', context)


class BookListView(LoginRequiredMixin, generic.ListView):
    # login_url = '/accounts/login/'
    redirect_field_name = 'list_of_books'
    permission_required = 'catalog.can_mark_returned'
    # model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 1
    # queryset = Book.objects.filter(title__icontains='war')

    def get_queryset(self):
        return Book.objects.all()

    # def get_template_names(self):
        # return 'catalog/book_list.html'


class AuthorListView(generic.ListView):
    def get_queryset(self):
        return Author.objects.all()

    def get_template_names(self):
        return 'catalog/author_list.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['authors'] = 'Authors'
        return context


class AuthorDetailView(generic.DetailView):
    def get_object(self, queryset=None):
        _id = self.kwargs.get('id')
        return get_object_or_404(Author, id=_id)


class BookDetailView(generic.DetailView):

    def get_object(self):
        _id = self.kwargs.get('id')
        return get_object_or_404(Book, id=_id)

    def get_template_names(self):
        return 'catalog/book_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookInstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LibrairianListView(PermissionRequiredMixin, View):
    model = BookInstance
    template_name = 'catalog/librairian_list_borrowed.html'
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

    def get_context_data(self, **kwargs):
        context = {}
        context['bookinstance_list'] = self.get_queryset()
        return context

    def handle_no_permission(self):
        return redirect('index')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


@login_required
@permission_required(('catalog.can_mark_returned'))
def librairianListView(request):
    bookinstance_list = BookInstance.objects.filter(
        status__exact='o').order_by('due_back')
    context = {'bookinstance_list': bookinstance_list}
    return render(request, 'catalog/librairian_list_borrowed.html', context)


class AuthorCreate(generic.edit.CreateView):
    model = Author
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(AuthorCreate, self).get_context_data(**kwargs)
        context['title'] = 'Create Author'
        return context


class AuthorUpdate(generic.edit.UpdateView):
    model = Author
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(AuthorUpdate, self).get_context_data(**kwargs)
        context['title'] = 'update '
        return context

    def get_object(self, queryset=None):
        _id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=_id)


class AuthorDelete(generic.edit.DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    def get_object(self, queryset=None):
        _id = self.kwargs.get('id')
        return get_object_or_404(self.model, id=_id)


class CreateBook(generic.edit.CreateView):
    model = Book
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CreateBook, self).get_context_data(**kwargs)
        context['title'] = 'Create Book'
        return context
