from django.contrib import admin
from .models import Ticketbook, TripPackage



@admin.register(Ticketbook)
class TicketbookAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name', 
        'source', 
        'destination', 
        'get_bus_type_display',  # Shows the human-readable choice value
        'ticket_amount',
        'seat_number', 
        'select_date', 
        'select_time'
    )
    search_fields = ('name', 'source', 'destination', 'bus_type', 'ticket_amount')
    list_filter = ('select_date', 'bus_type', 'source', 'destination')
    readonly_fields = ('user',)
    date_hierarchy = 'select_date'

    def get_bus_type_display(self, obj):
        return dict(Ticketbook.BUS_TYPE_CHOICES).get(obj.bus_type, obj.bus_type)
    get_bus_type_display.short_description = 'Bus Type'

@admin.register(TripPackage)
class TripPackageAdmin(admin.ModelAdmin):
    list_display = ('cust_name', 'name', 'amount', 'duration_days','no_of_tickets', 'short_places', 'created_at')
    search_fields = ('name', 'cust_name')

    def short_places(self, obj):
        return ', '.join(obj.places[:3]) + ('...' if len(obj.places) > 3 else '')
    short_places.short_description = 'Places'

