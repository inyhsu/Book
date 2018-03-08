from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
from django.db.models import Count

def index(request):
    # Giving value to session

    try:
        request.session['userid']
    except KeyError:
        request.session['userid'] = ""

    if request.session['userid']:
        return redirect('/books')
        
    return render(request,'index.html')


def books(request):
    context = {}

    if not request.session['userid']:
        messages.warning(request, "You must be logged in to see these books")
        return redirect('/')

    else:
        context['users'] = User.objects.get(id=request.session['userid'])
        # users become key and contain all the values inside User
        context['reviews'] = Review.objects.all().order_by('-created_at')[:3]

    return render(request,'books.html', context)

def register(request):
    result = User.objects.basic_validator(request.POST)

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request,error, extra_tags=tag)
        return redirect('/')
    
    else:
        request.session['userid'] = result[1].id
        return redirect('/books')


def login(request):
    result = User.objects.login_validator(request.POST)

    if result[0] == False:
        for tag, error in result[1].iteritems():
            messages.error(request,error, extra_tags=tag)
        return redirect('/')

    else:
        request.session['userid'] = result[1].id 
        return redirect('/books')

def logout(request):
    request.session.clear()

    return redirect('/')

def books_add(request):
    context = {}

    if not request.session['userid']:
        messages.warning(request, "You must logged in to see these books")
        return redirect('/')

    else:
        context['author'] = Author.objects.all()
    
    return render(request,'books_add.html',context)

def add_book(request):
    result = Book.objects.book_validator(request.POST,request.session['userid'],request.FILES)

    if result[0] == False:

        for tag, error in result[1].iteritems():
            messages.error(request,error, extra_tags=tag)

        return redirect('/books/add')

    else:
        request.session['bookid'] = result[1].id
        id = result[1].id
        return redirect("/books/"+str(id))

def show_book(request,id):
    
    if not request.session['userid']:
        messages.warning(request, "You must be logged in to see these books")
        return redirect('/')

    else :
        book = Book.objects.get(id=id)
        # Under Book with that id's everything
        reviews = Review.objects.filter(reviewedbook=book)
        # get all the reviews under that book
        #filter got a list of objects
        context ={
            'book': book,
            'reviews': reviews 
        }
    return render(request,"show_book.html",context)

def delete(request,id): #This is review id from show_book.html
    this_book_id = Review.objects.get(id=id).reviewedbook.id
    #we get the id for the book first and then delete the review so that we stay at that page
    Review.objects.get(id=id).delete()

    return redirect("/books/"+str(this_book_id))

def add_review(request,id):#This is book id from show_book.html
    result = Review.objects.review_validator(request.POST,request.session['userid'],id)

    if result[0] == False:
    
        for tag, error in result[1].iteritems():
            messages.error(request,error, extra_tags=tag)
        return redirect("/books/"+str(id))

    return redirect("/books/"+str(id))

def show_user(request,id): #This is user id

    if not request.session['userid']:
        messages.warning(request, "You must be logged in to see these books")
        return redirect('/')

    else :
        user = User.objects.get(id=id)
        reviews = Review.objects.filter(reviewer=user)
        review_count = reviews.annotate(review_count = Count('reviewedbook'))

        context ={
            'user': user,
            'reviews': reviews,
            'review_count': len(review_count)
        }
    return render(request,"show_user.html",context)
    
    
    
    