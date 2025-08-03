from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from holy_app.models import *
from django.utils import timezone
from django.core.paginator import Paginator
import os
from django.conf import settings


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('hfcadminhome')  # Make sure this URL is configured
        else:
            messages.error(request, 'Invalid credentials or not a superuser')
    return render(request, 'admin/adminlogin.html')


def hfcadminlogout(request):
    logout(request)
    return redirect('adminlogin') 

def hfcadminhome(request):
    return render(request, 'admin/hfcadminhome.html')


def ytvideo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        link = request.POST.get('link')
        if title and link:
            YTVideo.objects.create(title=title, link=link)
            messages.success(request, "Video added successfully!")
        else:
            messages.error(request, "Both title and video link are required!")
        return redirect('ytvideo')

    videos = YTVideo.objects.all()
    paginator = Paginator(videos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/ytvideo.html', {'page_obj': page_obj})

def delete_ytvideo(request, pk):
    video = get_object_or_404(YTVideo, pk=pk)
    video.delete()
    messages.success(request, "Video deleted successfully!")
    return redirect('ytvideo')


def news_announcements(request):
    # Handle POST (form submission)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_published = True if request.POST.get('is_published') == 'on' else False
        attachment = request.FILES.get('attachment')

        if title and content:
            NewsAndAnnouncement.objects.create(
                title=title,
                content=content,
                published_date=timezone.now(),
                is_published=is_published,
                attachment=attachment
            )
            messages.success(request, "News/Announcement added successfully.")
            return redirect('news_announcements')
        else:
            messages.error(request, "Title and content are required.")

    # Handle GET (with optional search)
    search_query = request.GET.get('search', '')
    announcements = NewsAndAnnouncement.objects.all().order_by('-published_date')
    if search_query:
        announcements = announcements.filter(title__icontains=search_query)

    # Pagination (15 per page)
    paginator = Paginator(announcements, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/news_announcements.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def news_announcements_detail(request,pk):
    news = get_object_or_404(NewsAndAnnouncement, pk=pk)
    return render(request, 'admin/news_announcements_detail.html', {'news': news})


def news_announcements_edit(request, pk):
    news = get_object_or_404(NewsAndAnnouncement, pk=pk)

    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.is_published = 'is_published' in request.POST

        if 'attachment' in request.FILES:
            news.attachment = request.FILES['attachment']

        news.save()
        messages.success(request, "Announcement updated successfully.")
        return redirect('news_announcements_detail', pk=news.pk)

    return render(request, 'admin/news_announcements_edit.html', {'news': news})


def delete_news(request, pk):
    news = get_object_or_404(NewsAndAnnouncement, pk=pk)

    if news.attachment:
        news.attachment.delete(save=False)

    news.delete()
    return redirect('news_announcements')





def advertisement(request):
    ad = AdvertisementBanner.objects.first()
    if not ad:
        ad = AdvertisementBanner.objects.create(title="Homepage Banner")

    if request.method == 'POST':
        # Handle image1
        if request.FILES.get('image1'):
            # Delete old image1 if it exists
            if ad.image1 and os.path.isfile(os.path.join(settings.MEDIA_ROOT, ad.image1.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, ad.image1.name))
            ad.image1 = request.FILES['image1']
        
        # Handle image2
        if request.FILES.get('image2'):
            # Delete old image2 if it exists
            if ad.image2 and os.path.isfile(os.path.join(settings.MEDIA_ROOT, ad.image2.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, ad.image2.name))
            ad.image2 = request.FILES['image2']
        
        # Handle image3
        if request.FILES.get('image3'):
            # Delete old image3 if it exists
            if ad.image3 and os.path.isfile(os.path.join(settings.MEDIA_ROOT, ad.image3.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, ad.image3.name))
            ad.image3 = request.FILES['image3']

        ad.save()
        messages.success(request, "Advertisement images updated successfully.")
        return redirect('advertisement')

    return render(request, 'admin/advertisement.html', {'ad': ad})






def gallery(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if image and not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            messages.error(request, "Only PNG, JPG, and JPEG formats are allowed.")
        else:
            GalleryItem.objects.create(title=title, description=description, image=image)
            messages.success(request, "Gallery item added successfully.")
            return redirect('gallery')

    # Handle GET (with optional search)
    search_query = request.GET.get('search', '')
    gallery_items = GalleryItem.objects.all().order_by('-created_at')
    if search_query:
        gallery_items = gallery_items.filter(title__icontains=search_query)

    # Pagination (15 per page)
    paginator = Paginator(gallery_items, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/gallery.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def delete_gallery(request, pk):
    gal = get_object_or_404(GalleryItem, pk=pk)

    if gal.image:
        gal.image.delete(save=False)

    gal.delete()
    return redirect('gallery')


def careers(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location')
        last_date_to_apply = request.POST.get('last_date_to_apply')
        mail = request.POST.get('mail')
        is_active = True if request.POST.get('is_active') == 'on' else False

        JobVacancy.objects.create(
            title=title,
            description=description,
            job_type=job_type,
            location=location,
            last_date_to_apply=last_date_to_apply if last_date_to_apply else None,
            mail=mail,
            is_active=is_active
        )
        messages.success(request, "Job vacancy posted successfully.")
        return redirect('careers')

    # Handle GET (with optional search)
    search_query = request.GET.get('search', '')
    vacancies = JobVacancy.objects.all().order_by('-posted_date')
    if search_query:
        vacancies = vacancies.filter(title__icontains=search_query)

    # Pagination (15 per page)
    paginator = Paginator(vacancies, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/careers.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def delete_careers(request, pk):
    gal = get_object_or_404(JobVacancy, pk=pk)

    gal.delete()
    return redirect('careers')



def enquiries(request):
    search_query = request.GET.get('search', '')
    messages_qs = ContactMessage.objects.all().order_by('-submitted_at')

    if search_query:
        messages_qs = messages_qs.filter(full_name__icontains=search_query)

    paginator = Paginator(messages_qs, 15)  # 15 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/enquiries.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def delete_messages(request, pk):
    gal = get_object_or_404(ContactMessage, pk=pk)
    gal.delete()
    return redirect('enquiries')

