from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, DonationForm, FeedbackForm, SupportTicketForm
from .models import Donation, SupportTicket

def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            error = "Invalid credentials"
            return render(request, 'login.html', {'error': error, 'next': next_url})
    return render(request, 'login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    donations = Donation.objects.filter(donor=request.user)
    return render(request, 'dashboard.html', {'donations': donations})

@login_required
def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('dashboard')
    else:
        form = DonationForm()
    return render(request, 'donor.html', {'form': form})   # 👈 donor.html instead of donate.html

@login_required
def donations_list(request):
    all_donations = Donation.objects.all()
    return render(request, 'food.html', {'donations': all_donations})  # 👈 food.html

def logistics_view(request):
    return render(request, 'logistics.html')

def safety_view(request):
    return render(request, 'safety.html')

def rewards_view(request):
    return render(request, 'rewards.html')

def security_view(request):
    return render(request, 'security.html')

def auth_view(request):
    return render(request, 'auth.html')

def uiux_view(request):
    return render(request, 'uiux.html')

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            if request.user.is_authenticated:
                fb.user = request.user
            fb.save()
            return redirect('index')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def tracking_view(request):
    return render(request, 'tracking.html')

def volunteer_view(request):
    return render(request, 'volunteer.html')

def support_create(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            if request.user.is_authenticated:
                ticket.user = request.user
            ticket.save()
            return render(request, 'support_thanks.html', {'ticket': ticket})
    else:
        preset = {}
        if request.user.is_authenticated:
            preset = {'name': request.user.get_username(), 'email': request.user.email}
        form = SupportTicketForm(initial=preset)
    return render(request, 'support.html', {'form': form})

@login_required
def support_list(request):
    if not request.user.is_staff:
        return redirect('index')
    tickets = SupportTicket.objects.order_by('-created_at')
    return render(request, 'support_list.html', {'tickets': tickets})

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

@login_required
@require_GET
def api_my_donations(request):
    items = Donation.objects.filter(donor=request.user).order_by('-created_at')
    data = [
        {
            'id': d.id,
            'title': d.title,
            'quantity': d.quantity,
            'pickup_address': d.pickup_address,
            'city': d.city,
            'status': d.status,
            'created_at': d.created_at.isoformat(),
        }
        for d in items
    ]
    return JsonResponse({'donations': data})

from .models import Notification

@login_required
@require_GET
def api_notifications(request):
    notes = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = [
        {
            'id': n.id,
            'message': n.message,
            'created_at': n.created_at.isoformat(),
        }
        for n in notes
    ]
    return JsonResponse({'notifications': data})

from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import User

@login_required
def generate_certificate(request):
    name_param = request.GET.get('name')
    username_param = request.GET.get('username')

    display_name = None
    target_user = None

    if name_param:
        display_name = name_param.strip()
    elif username_param:
        try:
            target_user = User.objects.get(username=username_param)
            display_name = target_user.get_username()
        except User.DoesNotExist:
            display_name = username_param
    else:
        target_user = request.user if request.user.is_authenticated else None
        display_name = (target_user.get_username() if target_user else 'Donor')

    if target_user is None and request.user.is_authenticated:
        target_user = request.user

    approved_count = 0
    if target_user is not None:
        approved_count = Donation.objects.filter(donor=target_user, status__in=['approved', 'collected']).count()

    context = {
        'display_name': display_name,
        'approved_count': approved_count,
        'issued_at': timezone.now(),
        'project_title': 'WEB-BASED FOOD DONATION AND DISTRIBUTION MANAGEMENT',
    }
    return render(request, 'certificate.html', context)
