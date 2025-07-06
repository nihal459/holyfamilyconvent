from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    latest_news = NewsAndAnnouncement.objects.filter(is_published=True).order_by('-published_date')[:15]
    active_banner = AdvertisementBanner.objects.filter(is_active=True).first()
    gallery_items = GalleryItem.objects.all().order_by('-created_at')[:5]  # Limit to 10 items or as you like

    return render(request, 'index.html', {
        'latest_news': latest_news,
        'banner': active_banner,
        'gallery_items': gallery_items
    })



def view_announcements(request):
    all_announcements = NewsAndAnnouncement.objects.filter(is_published=True).order_by('-published_date')
    paginator = Paginator(all_announcements, 15)  # 15 announcements per page

    page = request.GET.get('page')
    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)

    return render(request, 'view_announcements.html', {'announcements': announcements})


def view_gallery(request):
    gallery_items = GalleryItem.objects.all()
    paginator = Paginator(gallery_items, 15)  # Show 15 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'view_gallery.html', {
        'gallery_items': page_obj,
        'page_obj': page_obj
    })



def view_careers(request):
    job_vacancies = JobVacancy.objects.filter(is_active=True)
    paginator = Paginator(job_vacancies, 5)  # 5 items per page
    page_number = request.GET.get('page')
    job_vacancies = paginator.get_page(page_number)
    return render(request, 'view_careers.html', {'job_vacancies': job_vacancies})




def view_contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Basic validation
        if not full_name or not email or not subject or not message:
            messages.error(request, "All fields are required. Please fill out the form completely.")
        elif '@' not in email or '.' not in email.split('@')[1]:
            messages.error(request, "Please enter a valid email address.")
        else:
            # Save to database
            contact_message = ContactMessage(
                full_name=full_name,
                email=email,
                subject=subject,
                message=message,
                submitted_at=timezone.now(),
                is_read=False
            )
            contact_message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('view_contact')  # Redirect to the same page or a thank you page

    return render(request, 'view_contact.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def admission(request):
    return render(request, 'admission.html')


def academics(request):
    return render(request, 'academics.html')