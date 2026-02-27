from django.contrib import admin
from .models import Donation, Feedback, SupportTicket, Notification

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'quantity', 'pickup_address', 'created_at', 'status', 'is_collected')
    list_filter = ('status', 'is_collected', 'created_at', 'city')
    search_fields = ('title', 'donor__username', 'pickup_address')

    actions = ['approve_donations', 'mark_collected']

    def approve_donations(self, request, queryset):
        count = 0
        for d in queryset:
            if d.status != 'approved':
                d.status = 'approved'
                d.save(update_fields=['status'])
                Notification.objects.create(user=d.donor, message=f"Your donation '{d.title}' was approved.")
                count += 1
        self.message_user(request, f"Approved {count} donations.")
    approve_donations.short_description = 'Approve selected donations'

    def mark_collected(self, request, queryset):
        count = 0
        for d in queryset:
            if d.status != 'collected' or not d.is_collected:
                d.status = 'collected'
                d.is_collected = True
                d.save(update_fields=['status', 'is_collected'])
                Notification.objects.create(user=d.donor, message=f"Your donation '{d.title}' was marked collected.")
                count += 1
        self.message_user(request, f"Marked {count} donations as collected.")
    mark_collected.short_description = 'Mark selected donations as collected'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username', 'message')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'priority', 'status', 'name', 'email', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('subject', 'message', 'email', 'name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
