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
    if request.method == "POST":
        if request.POST.get('bidAmount'):
            bid_amount = request.POST['bidAmount']
            place_bid(listing_id, request.user.username, bid_amount)


    listing = get_listing(listing_id)

    return render(request, "biddingsystem/listing.html", {
        "listing": listing,
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

#defining a function to create a chat page
@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user from the list
    conversations = {}  # Dictionary to store conversations for each user
    
    for user in users:
        conversation = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=user)) | (Q(sender=user) & Q(recipient=request.user))
        ).order_by('-timestamp')[:5]  # Fetch the last 5 messages for each user
        
        conversations[user] = conversation
    
    return render(request, 'biddingsystem/chat.html', {'users': users, 'conversations': conversations})

@login_required
def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message', '')
        recipient_id = request.POST.get('recipient_id', None)
        if message_text and recipient_id:
            recipient = User.objects.get(id=recipient_id)
            Message.objects.create(sender=request.user, recipient=recipient, content=message_text)
    return redirect('chat_view')  # Redirect to the general chat page after sending the message

@login_required
def individual_chat_view(request, user_id):
    recipient = get_object_or_404(User, pk=user_id)
    
    # Fetch chat messages between the logged-in user and the selected user
    chat_messages = Message.objects.filter(sender=request.user, recipient=recipient) | \
                    Message.objects.filter(sender=recipient, recipient=request.user)
    
    return render(request, 'biddingsystem/individual_chat.html', {'recipient': recipient, 'chat_messages': chat_messages})

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipient_id = data.get('recipient_id')
        message_text = data.get('message')

        if recipient_id and message_text:
            recipient = User.objects.get(id=recipient_id)
            message = Message.objects.create(sender=request.user, recipient=recipient, content=message_text)
            return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error'})