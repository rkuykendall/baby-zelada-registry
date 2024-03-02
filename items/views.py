import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, Prefetch
from django.db.models.functions import Coalesce
from .models import Item, Category, Gift
from .forms import GiftForm


def item_list(request):
    # Categories with at least one item
    categories = (
        Category.objects.all()
        .prefetch_related(
            Prefetch(
                "item_set",
                queryset=Item.objects.annotate(
                    num_gifts=Coalesce(Sum("gift__quantity"), 0)
                ),
            )
        )
        .filter(item__isnull=False)
        .distinct()
    )
    user_authenticated = request.user.is_authenticated

    context = {"categories": categories, "user_authenticated": user_authenticated}
    return render(request, "items_list.html", context)


def export_items_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="items.csv"'},
    )

    writer = csv.writer(response)

    # Write the headers to the CSV file.
    writer.writerow(['Category Name', 'Item Name', 'Number of Gifts', 'Quantity Desired', 'Gifts Remaining'])

    # Query the database for items
    categories = Category.objects.all().prefetch_related(
        Prefetch(
            "item_set",
            queryset=Item.objects.annotate(
                num_gifts=Coalesce(Sum("gift__quantity"), 0)
            ),
        )
    ).filter(item__isnull=False).distinct()

    # Write data rows
    for category in categories:
        for item in category.item_set.all():
            gifts_remaining = item.quantity_desired - item.num_gifts
            writer.writerow([category.name, item.name, item.num_gifts, item.quantity_desired, gifts_remaining])

    return response


def export_gifts_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="gifts.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Quantity', 'Given By'])

    # Assuming 'Gift' model has fields like 'quantity', 'given_by', and a foreign key to 'Item'
    gifts = Gift.objects.select_related('item').all()

    for gift in gifts:
        writer.writerow([gift.item.name, gift.quantity, gift.giver_name])

    return response


def create_gift(request):
    selected_item = None
    if request.method == "POST":
        form = GiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("item_list")
    else:
        if "item_id" in request.GET:
            try:
                selected_item = Item.objects.get(pk=request.GET["item_id"])
            except Item.DoesNotExist:
                pass
        form = GiftForm(initial={"item": selected_item})

    context = {"form": form, "selected_item": selected_item}
    return render(request, "create_gift.html", context)
