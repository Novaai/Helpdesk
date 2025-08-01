from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Allocation, Item_type
from .forms import ItemUpdateForm
from django.contrib.auth.models import User

# Create your views here.
@login_required
def home_inventory(request):
    return render(request, 'home_inventory.html')

@login_required
def all_items(request):
    item_types = Item_type.objects.all().order_by('item_type_name')
    all_staff = User.objects.order_by('username')

    selected_type_id = request.GET.get('type')
    selected_user_id = request.GET.get('user')

    items_qs = Item.objects.select_related('item_type').order_by('id')

    if selected_type_id:
        items_qs = items_qs.filter(item_type_id=selected_type_id)

    if selected_user_id:
        # Filter items allocated to the selected user
        items_qs = items_qs.filter(allocation__staff_id=selected_user_id)

    allocations = Allocation.objects.select_related('item', 'staff')
    allocation_map = {alloc.item.id: alloc for alloc in allocations}
    for item in items_qs:
        item.allocation = allocation_map.get(item.id)

    return render(request, 'inventory/all_items.html', {
        'items': items_qs,
        'item_types': item_types,
        'all_staff': all_staff,
        'selected_type_id': int(selected_type_id) if selected_type_id else None,
        'selected_user_id': int(selected_user_id) if selected_user_id else None,
    })

@login_required
def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    allocation = Allocation.objects.filter(item=item).first()
    is_inventory_admin = request.user.groups.filter(name="Inventory Admins").exists()
    all_staff = User.objects.all().order_by('username') if is_inventory_admin else None

    return render(request, 'inventory/detail.html', {
        'item': item,
        'allocation': allocation,
        'is_inventory_admin': is_inventory_admin,
        'all_staff': all_staff,
    })



def is_inventory_admin(user):
    return user.groups.filter(name="Inventory Admins").exists()

@login_required
@user_passes_test(is_inventory_admin)
def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    allocation = Allocation.objects.filter(item=item).first()
    all_staff = User.objects.order_by('username')

    if request.method == 'POST':
        form = ItemUpdateForm(request.POST, instance=item)
        allocated_to_id = request.POST.get('allocated_to')

        if form.is_valid():
            form.save()

            # Handle allocation logic
            if allocated_to_id:
                staff_user = get_object_or_404(User, pk=allocated_to_id)
                Allocation.objects.update_or_create(item=item, defaults={'staff': staff_user})
                item.allocation_status = 'allocated'
            else:
                Allocation.objects.filter(item=item).delete()
                item.allocation_status = 'unallocated'

            item.save()
            return redirect('inventory:detail', item_id=item.id)
    else:
        form = ItemUpdateForm(instance=item)

    return render(request, 'inventory/update_item.html', {
        'form': form,
        'item': item,
        'allocation': allocation,
        'all_staff': all_staff,
    })