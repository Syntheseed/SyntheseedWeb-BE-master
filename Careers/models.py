from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Career(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100, db_index=True)
    location = models.CharField(max_length=100, db_index=True)
    work_mode = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50, db_index=True)

    # Updated for CKEditor rich text support
    description = RichTextUploadingField()
    tags = models.TextField(blank=True)
    details = RichTextUploadingField(blank=True)

    posted_on = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted_on']
        indexes = [
            models.Index(fields=['department', 'location'], name='career_dept_loc_idx'),
            models.Index(fields=['job_type'], name='career_jobtype_idx'),
            models.Index(fields=['posted_on'], name='career_posted_on_idx'),
        ]


class JobApplication(models.Model):
    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    applied_on = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.full_name} - {self.career.title}"
