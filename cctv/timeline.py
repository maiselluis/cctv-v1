from django.shortcuts import render
from .models import Cash_Desk_Transaction
from .forms import FilterTtransactionsByTimeLine
from datetime import date

def transaction_timeline(request):
    user_location = None
    location_id = None
    transactions = Cash_Desk_Transaction.objects.none()  # Inicializamos vacío

    if not request.user.is_superuser:
        user_location = getattr(request.user.userprofile, "location", None)
        location_id = getattr(user_location, "id", None)

    form = FilterTtransactionsByTimeLine(request.GET or None, initial={"location": user_location, "location_id": location_id} )

    if form.is_valid():
        transactions = Cash_Desk_Transaction.objects.select_related("customer").order_by("-date", "-time")

        if user_location:
            transactions = transactions.filter(location=user_location)

        date_begin = form.cleaned_data.get("date_begin")
        date_end = form.cleaned_data.get("date_end")
        customer_id = form.cleaned_data.get("customer")

        if date_begin and date_end:
            transactions = transactions.filter(date__range=(date_begin, date_end))

        if customer_id:
            transactions = transactions.filter(customer_id=customer_id)

    return render(request, "timeline/transaction-timeline.html", {"form": form, "transactions": transactions})




