from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "biddingsystem/index.html")

def create(request):
    return render(request, "biddingsystem/createListing.html")

def listing(request, listing_id):
    return render(request, "biddingsystem/listing.html")