from django.db import models
from django.contrib.auth.models import User


class Schema(models.Model):
    COLUMN_CHOICES = (
        (',', "Comma (,)"),
        ('.', "Dot (.)")
    )
    STRING_CHOICES = (
        ('"', 'Double-quote (")'),
        ("'", "Single-quote (')")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    column_separator = models.CharField(choices=COLUMN_CHOICES, max_length=5, default="Comma (,)")
    string_character = models.CharField(choices=STRING_CHOICES, max_length=6, blank=True)
    modified = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Schema {self.title} {self.id}'


class Column(models.Model):
    TYPE_CHOICES = (
        ('full_name', 'Full name'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('domain_name', 'Domain name'),
        ('phone_number', 'Phone number'),
        ('company_name', 'Company Name'),
        ('integer', 'Integer'),
        ('text', 'Text'),
        ('address', 'Address'),
        ('date', 'Date'),
    )

    column_name = models.CharField(max_length=128)
    column_type = models.CharField(choices=TYPE_CHOICES, max_length=32)
    from_range = models.IntegerField(blank=True, null=True)
    to_range = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(default=1)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'Column {self.id} {self.column_name}'


class DataSet(models.Model):
    created = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    file = models.FileField(blank=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return f'DataSet {self.id} {self.created}'

    class Meta:
        get_latest_by = ['id']
