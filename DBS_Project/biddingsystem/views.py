from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads
from .models import Message
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import stripe

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

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    

def get_user(username):
    with connection.cursor() as cursor:
        cursor.callproc("get_user", [username])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()  
        if row:
            return dict(zip(columns, row))


    

def get_user_listings(username):
    with connection.cursor() as cursor:
        cursor.callproc("user_listing", [username])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    

def close_auction(listing_id):
    with connection.cursor() as cursor:
        cursor.callproc("close_auction", [listing_id])

def return_listing_page_with_message(request, listing_id, message):
    listing = get_listing(listing_id)
    comments = get_listing_comments(listing_id)
    return render(request, 'biddingsystem/layout.html', {
        "listing": listing,
        "comments": comments,
        "message": message
    })

def sufficient_balance(username, amount):
    with connection.cursor() as cursor:
        cursor.callproc("sufficient_balance", [username, amount])
        return cursor.fetchone()[0]
    
def make_payment(listing_id, payer, payee, amount):
    with connection.cursor() as cursor:
        cursor.callproc("make_payment", [listing_id, payer, payee, amount])

    
def get_watchlist_listings(username):
    with connection.cursor() as cursor:
        cursor.callproc("watchlist_page", [username])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def add_to_watchlist(username, listing_id):
    with connection.cursor() as cursor:
        cursor.callproc("add_to_watchlist", [username, listing_id])

def get_category(categoryID):
    with connection.cursor() as cursor:
        cursor.callproc("return_category", [categoryID])
        return cursor.fetchone()[0]
    
def listing_in_watchlist(username, listing_id):
    with connection.cursor() as cursor:
        cursor.callproc("check_watchlist", [username, listing_id])
        return cursor.fetchone()[0]


def remove_from_watchlist(username, listing_id):
    with connection.cursor() as cursor:
        cursor.callproc("remove_from_watchlist", [username, listing_id])

def add_to_wallet(username, amount):
    with connection.cursor() as cursor:
        cursor.callproc("wallet_add_amount", [username, amount])

def get_wallet_amount(username):
    with connection.cursor() as cursor:
        cursor.callproc("wallet_amount", [username])
        return cursor.fetchone()[0]
    

def check_follow(follower, followed):
    with connection.cursor() as cursor:
        cursor.callproc("check_follow", [follower, followed])
        return cursor.fetchone()[0]
    
def follow_user(follower, followed):
    with connection.cursor() as cursor:
        cursor.callproc("follow", [follower, followed])

def unfollow_user(follower, followed):
    with connection.cursor() as cursor:
        cursor.callproc("unfollow", [follower, followed])

def get_followers(username):
    with connection.cursor() as cursor:
        cursor.callproc("user_followers", [username])
        return cursor.fetchone()[0]

def get_following(username):
    with connection.cursor() as cursor:
        cursor.callproc("user_following", [username])
        return cursor.fetchone()[0]
    
def get_no_of_listings(username):
    with connection.cursor() as cursor:
        cursor.callproc("user_listing", [username])
        return cursor.fetchone()[0]
    

def get_following_listings(username):
    with connection.cursor() as cursor:
        cursor.callproc("followed_user_posts", [username])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

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
        "listings": listings,
        "key": settings.STRIPE_PUBLISHABLE_KEY
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
    comments = get_listing_comments(listing_id) 
    if request.method == "POST":
        if request.POST.get('bidAmount'):
            bid_amount = request.POST['bidAmount']
            if request.user.username == listing["lister"]:
                return_listing_page_with_message(request, listing_id, "You can't place a bid on your own listing")
            elif listing["is_closed"]:
                return_listing_page_with_message(request, listing_id, "This listing has been closed")
            place_bid(listing_id, request.user.username, bid_amount)
            return_listing_page_with_message(request, listing_id, "Bid placed successfully")

        
        if request.POST.get('comment'):
            comment_text = request.POST.get('comment_text')
            commenter = request.user.username
            if listing["is_closed"]:
                return_listing_page_with_message(request, listing_id, "This listing has been closed")

            make_comment(listing_id, commenter, comment_text)


        if request.POST.get('close_auction'):
            if request.user.username != listing["lister"]:
                return_listing_page_with_message(request, listing_id, "Only the owner of the listing can close the auction")
 
            close_auction(listing_id)
            return_listing_page_with_message(request, listing_id, "Successfully closed the listing")

        if request.POST.get('payment'):
            if request.user.username == listing["winner"]:
                payer = request.user.username
                payee = listing["lister"]
                amount = listing["current_price"]
                if not sufficient_balance(request.user.username, amount):
                    return return_listing_page_with_message(request, listing_id, "You dont have enough amount to pay for this product")
                make_payment(listing_id, payer, payee, amount)

        if request.POST.get('add_to_watchlist'):
            add_to_watchlist(request.user.username, listing_id)

        if request.POST.get('remove_from_watchlist'):
            remove_from_watchlist(request.user.username, listing_id)





    listing = get_listing(listing_id)

    comments = get_listing_comments(listing_id)

    category = get_category(listing["category"])

    add_to_watchlist_button = not listing_in_watchlist(request.user.username, listing_id)

    return render(request, "biddingsystem/listing.html", {
        "listing": listing,
        "comments": comments,
        "category": category,
        "bid_option": bool (request.user.username != listing["lister"]),
        "close_option": bool (request.user.username == listing["lister"]),
        "add_to_watchlist_button": add_to_watchlist_button
    })


def profile(request, username):
    profile = get_user(username)
    wallet_credit = get_wallet_amount(username)
    follow = check_follow(request.user.username, username)
    followers = get_followers(username)
    following = get_following(username)
    no_of_listings = get_no_of_listings(username)
    return render(request, "biddingsystem/profile.html", {
        "profile": profile,
        "self_profile": bool (request.user.username == profile.get("username")),
        "listings": get_user_listings(username),
        "wallet_credit": wallet_credit,
        "follow": follow,
        "followers": followers,
        "following": following,
        "no_of_listings": no_of_listings
    })

@csrf_exempt
def follow(request, username):
    if request.method != "POST":
        return JsonResponse({"message": "Post request required"})
    
    data = loads(request.body)
    follower = data.get('follower')
    followed = data.get('followed')

    #code to make an entry in the follow table

    if data.get('operation') == "follow":
        try:
            follow_user(follower, followed)
            pass
        except IntegrityError:
            return render(request, 'biddingsystem/profile.html', {
                "message": "You already follow this user"
            })
        
    elif data.get('operation') == "unfollow":
        try:
            unfollow_user(follower, followed)
            pass
        except:
            return render(request, 'biddingsystem/profile.html', {
                "message": "You don't follow this user"
            })
        
    return JsonResponse({
        "message": "success"
    })

def following(request):
    listings = get_following_listings(request.user.username)
    return render(request, "biddingsystem/index.html", {
        "listings": listings
    })


def watchlist(request):
    listings = get_watchlist_listings(request.user.username)
    return render(request, "biddingsystem/index.html", {
        "listings": listings
    })

def payment(request, listing_id):
    if request.method == "POST":
        pass
    return render(request, "biddingsystem/payment.html", {
        "listing": get_watchlist_listings(listing_id)
    })


def topup(request):
    if request.method == "POST":
        if request.POST.get('topup'):
            topup_amount = str(request.POST['topup_amount'])
            return render(request, "biddingsystem/topup.html", {
                "key": settings.STRIPE_PUBLISHABLE_KEY,
                "amount": topup_amount
            })
        
        amount = request.POST["topup_payment"]

        add_to_wallet(request.user.username, amount)
        
        return redirect(reverse(profile, kwargs = {
            "username": request.user.username
        }))
    return render(request, "biddingsystem/topup.html", {
        "key": settings.STRIPE_PUBLISHABLE_KEY
    })

#defining a function to create a chat page
def chat_view(request):
    # This function excludes the currently logged in user (i-e us) from the chat list to avoid self-chat
    users = User.objects.exclude(id=request.user.id)
    
    # Fetch messages for each user in the loop
    for user in users:
        # Fetch messages for the current user from the database
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=user)) |
            (Q(sender=user) & Q(recipient=request.user))
        ).order_by('timestamp')
        
        # Attach the messages to the user object for rendering
        user.messages = messages
    
    return render(request, 'biddingsystem/chat.html', {'users': users})

@login_required
def individual_chat_view(request, user_id):
    recipient = get_object_or_404(User, pk=user_id)

    # Fetch chat messages between the logged-in user and the selected user
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by('timestamp')
    
    return render(request, 'biddingsystem/individual_chat.html', {'recipient': recipient, 'chat_messages': messages})


@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            print("entered send_message function")
            data = json.loads(request.body)
            recipient_id = data.get('recipient_id')
            message_text = data.get('message')
            print(recipient_id)
            print(message_text)
            
            # Validate recipient_id and message_text
            if not (recipient_id and message_text):
                return JsonResponse({'status': 'error', 'message': 'Recipient ID or message missing'})

            print("control reached checking existing recipient")
            # Check if the recipient exists
            recipient = User.objects.filter(id=recipient_id).first()
            if not recipient:
                return JsonResponse({'status': 'error', 'message': 'Recipient does not exist'})

            # Create a message
            print("control reaches create message method")
            message = Message.objects.create(sender=request.user, recipient=recipient, content=message_text)
            return JsonResponse({'status': 'ok'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
