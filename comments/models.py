from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from PIL import Image


class Comment(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Поле для зображень
    text_file = models.FileField(upload_to='files/', blank=True, null=True)  # Поле для текстових файлів

    def save(self, *args, **kwargs):
        # Якщо додається зображення, змінюємо розмір до 320x240
        if self.image:
            img = Image.open(self.image)
            if img.width > 320 or img.height > 240:
                output_size = (320, 240)
                img.thumbnail(output_size)
                img.save(self.image.path)
        super().save(*args, **kwargs)

    def clean(self):
        # Перевірка формату файлу
        if self.text_file:
            if not self.text_file.name.endswith('.txt'):
                raise ValidationError('Only .txt files are allowed.')
            if self.text_file.size > 100 * 1024:  # 100 кб
                raise ValidationError('The file size must not exceed 100 KB.')

    def __str__(self):
        return self.text
