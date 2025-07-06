from django.db import models
from django.utils import timezone

class NewsAndAnnouncement(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    attachment = models.FileField(upload_to='news_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class AdvertisementBanner(models.Model):

    title = models.CharField(max_length=100)
    image1 = models.ImageField(upload_to='ad_banners/', blank=True, null=True)
    image2 = models.ImageField(upload_to='ad_banners/', blank=True, null=True)
    image3 = models.ImageField(upload_to='ad_banners/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class GalleryItem(models.Model): 
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
    


class JobVacancy(models.Model):
    
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    location = models.CharField(max_length=255)
    posted_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_date_to_apply = models.DateField(null=True, blank=True) 
    mail = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = ['-posted_date']
        verbose_name = "Job Vacancy"
        verbose_name_plural = "Job Vacancies"

    def __str__(self):
        return self.title