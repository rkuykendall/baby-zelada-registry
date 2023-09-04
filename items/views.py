from django.shortcuts import render, redirect
from django.db.models import Sum, Prefetch
from .models import Item, Category
from .forms import GiftForm


def item_list(request):
    categories = Category.objects.all().prefetch_related(
        Prefetch(
            "item_set", queryset=Item.objects.annotate(num_gifts=Sum("gift__quantity"))
        )
    )
    user_authenticated = request.user.is_authenticated

    context = {"categories": categories, "user_authenticated": user_authenticated}
    return render(request, "items_list.html", context)


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
