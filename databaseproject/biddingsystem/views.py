from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
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

def my_custom_sql():
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
    listings = my_custom_sql()
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
    return render(request, "biddingsystem/createListing.html")

def listing(request, listing_id):
    listing = get_listing(listing_id)

    return render(request, "biddingsystem/listing.html", {
        "listing": listing
    })