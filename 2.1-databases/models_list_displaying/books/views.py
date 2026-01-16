from datetime import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from books.models import Book
from django.core.paginator import Paginator


def index(request):
    return redirect('books')

def books_view(request: HttpRequest, pub_date=None) -> HttpResponse:
    template = 'books/books_list.html'
    books = Book.objects.all()
    prev_date = None
    next_date = None
    
    if pub_date is not None:
        books = books.filter(pub_date=pub_date)
        all_dates = list(Book.objects.dates('pub_date', 'day'))
        pub_date = datetime.strptime(pub_date, '%Y-%m-%d').date()
        paginator = Paginator(all_dates, 1)
        current_index = all_dates.index(pub_date)
        page_number = current_index + 1
        current_page = paginator.page(page_number)
    
        if current_page.has_previous():
            prev_page = paginator.page(current_page.previous_page_number())
            prev_date = prev_page.object_list[0] if prev_page.object_list else None
        
        if current_page.has_next():
            next_page = paginator.page(current_page.next_page_number())
            next_date = next_page.object_list[0] if next_page.object_list else None
    
    context = {
        'books': books,
        'prev_date': prev_date,
        'next_date': next_date,
    }
        
    return render(request, template, context)
