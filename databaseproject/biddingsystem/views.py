from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads
# import pyrebase


# firebaseConfig = {
# "apiKey": "AIzaSyA0D4DfmdtOWCjSXutjiWaEPFcrVW124vY",
# "authDomain": "biddingsystem-55752.firebaseapp.com",
# "projectId": "biddingsystem-55752",
# "storageBucket": "biddingsystem-55752.appspot.com",
# "messagingSenderId": "111594590720",
# "appId": "1:111594590720:web:2a9f5eba258eecada3fee5",
# "measurementId": "G-8060RX134X"
# }

# firebase = pyrebase.initialize_app(firebaseConfig)
# storage = firebase.storage()

def get_all_listings():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM listing')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
def get_listing(listingID):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listing WHERE listing_id = {}".format(listingID))
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        else:
            return None  # Handle the case where no row is found

def place_bid(listing_id, bidder, bid_amount):
    with connection.cursor() as cursor:
        cursor.callproc("place_bid", [listing_id, bid_amount, bidder])

def get_categories():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM category")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
def make_comment(listing_id, commenter, comment):
    with connection.cursor() as cursor:
        cursor.callproc("make_comment", [listing_id, commenter, comment])

def get_listing_comments(listing_id):
    with connection.cursor() as cursor:
        cursor.callproc("get_comments", [listing_id])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.create_user(first_name = first_name, last_name = last_name, email = email, username = username, password = password)
            login(request, user)
        except IntegrityError:
            return render(request, "biddingsystem/register.html", {
                    "message": "Username is already taken"
                })         

        return redirect(reverse(index))
    
    return render(request, "biddingsystem/register.html")

def log_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
        except:
            return render(request, "biddingsystem/login.html", {
                "message": "Invalid username or password"
            })
        
        return redirect(reverse(index))
    
    return render(request, "biddingsystem/login.html")

def log_out(request):
    logout(request)

    return redirect(reverse(index))

def index(request):
    listings = get_all_listings()
    return render(request, "biddingsystem/index.html", {
        "listings": listings
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        base_price = request.POST["base_price"]
        category = request.POST["category"]
        image = request.POST["image"]

        query = "INSERT INTO listing (lister, title, description, base_price, current_price, category, time_created) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', NOW())".format(request.user.username, title, description, base_price, base_price, category)
        with connection.cursor() as cursor:
            cursor.execute(query)

        return redirect(reverse(index))

    categories = get_categories()
    return render(request, "biddingsystem/createListing.html", {
        "categories": categories
    })

def listing(request, listing_id):
    listing = get_listing(listing_id)
    
    if request.method == "POST":
        if request.POST.get('bidAmount'):
            bid_amount = request.POST['bidAmount']
            if request.user.username == listing["lister"]:
                return render(request, "biddingsystem/listing.html", {
                    "listing": listing,
                    "message": "You can't place a bid on your own listing"
                })
            elif listing["is_closed"]:
                return render(request, "biddingsystem/listing.html", {
                    "listing": listing,
                    "message": "This listing has already been closed"
                })
            place_bid(listing_id, request.user.username, bid_amount)
            return render(request, "biddingsystem/listing.html", {
                "listing": listing,
                "message": "Bid placed succesfully"
            })
        
        if request.POST.get('comment'):
            comment_text = request.POST.get('comment_text')
            commenter = request.user.username
            if listing["is_closed"]:
                return render(request, "biddingsystem/listing.html", {
                    "listing": listing,
                    "message": "This listing has been closed"
                }) 
            make_comment(listing_id, commenter, comment_text)



    comments = get_listing_comments(listing_id)

    return render(request, "biddingsystem/listing.html", {
        "listing": listing,
        "comments": comments,
        "bid_option": bool (request.user.username != listing["lister"]),
        "close_option": bool (request.user.username == listing["lister"])
    })


def profile(request):
    return render(request, "biddingsystem/profile.html", {
        "self_profile": True,
        "listings": get_all_listings()
    })


@csrf_exempt
def follow(request):
    if request.method != "POST":
        return JsonResponse({"message": "Post request required"})
    
    data = loads(request.body)
    follower = data.get('follower')
    followed = data.get('followed')

    #code to make an entry in the follow table

    # if data.get('operation') == "follow":
    #     try:
    #         # code to make an entry in the follow table
    #         pass
    #     except IntegrityError:
    #         return render(request, 'biddingsystem/profile.html', {
    #             "message": "You already follow this user"
    #         })
        
    # elif data.get('operation') == "unfollow":
    #     try:
    #         # code to delete an entry from the follow table
    #         pass
    #     except:
    #         return render(request, 'biddingsystem/profile.html', {
    #             "message": "You don't follow this user"
    #         })
        
    return JsonResponse({
        "message": "success"
    })


def payment(request, listing_id):
    if request.method == "POST":
        pass
    return render(request, "biddingsystem/payment.html", {
        "listing": get_listing(listing_id)
    })
