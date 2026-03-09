from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100, db_index=True)

    # Updated for CKEditor rich text support
    summary = RichTextUploadingField(blank=True)
    content = RichTextUploadingField()

    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['category'], name='blog_category_idx'),
            models.Index(fields=['created_at'], name='blog_created_at_idx'),
            models.Index(fields=['category', 'created_at'], name='blog_category_created_idx'),
        ]
