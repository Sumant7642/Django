from django.db import models

# Create your models here.
class MyModel(models.Model):
    upload_file = models.FileField(
        upload_to='tuploaded_file/%Y/%m/%d'
    )

class file(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    pdf=models.FileField(upload_to='files/en_crypted_files/')


    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)