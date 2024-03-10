from django.shortcuts import render
from django.db.models import Max

# i need flights
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Passenger
# Create your views here.


def index(request):
    return render (request,'flights/index.html', {
        'flights': Flight.objects.all()
    } )


def flight(request, flight_id):

    max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
    if flight_id > max_id :
        return render(request, 'flights/404.html')
 
    flight = Flight.objects.get(pk=flight_id)

    return render (request, 'flights/flight.html', {
        'flight': flight,
        'passengers': flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
    
