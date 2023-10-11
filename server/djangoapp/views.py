from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# def get_staticpage(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'st.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            #return redirect('djangoapp:popular_course_list')
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            # return render(request, 'djangoapp/user_login.html', context)
            return redirect(request, 'djangoapp:index')

    # else:
    #     # return render(request, 'djangoapp/user_login.html', context)
    return redirect('djangoapp:index')



# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    # return redirect('onlinecourse:popular_course_list')
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'onlinecourse/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "http://127.0.0.1:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealership_list"] = dealerships
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "http://127.0.0.1:5000/api/get_reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        print(dealer_reviews)
        review_names = '<br>'.join( review.name + " : " + review.review+ " : " + review.sentiment for review in dealer_reviews)
        context["review_list"] = dealer_reviews
        #return HttpResponse(review_names)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    print("This is add review dealer_id,", dealer_id)
    user = request.user
    print("Use logged in, ", user.is_authenticated)
    print(request.method)
    json_data = json.loads(request.body)
    print(json_data)

    if request.method == "POST":
        url = "http://127.0.0.1:5000/api/post_review"
        review = dict()
        review["id"] = json_data["id"]
        review["name"] = json_data["name"]
        review["dealership"]= json_data["dealership"]
        review["review"] = json_data["review"]
        review["purchase"] = json_data["purchase"]
        review["purchase_date"] = json_data["purchase_date"]
        review["car_make"] = json_data["car_make"]
        review["car_model"] = json_data["car_model"]
        review["car_year"] = json_data["car_year"]
        try:
            print("call before post_request")
            response = post_request(url, review, dealerId=dealer_id)
            print("call end post_request")
            return HttpResponse("Success to add review")
        except:
            print("Network exception occurred")
    else:
        print("User is not logged in")
        return HttpResponse("Failed to add review")



