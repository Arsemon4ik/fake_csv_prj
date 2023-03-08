from django.contrib import admin
from .models import Schema, DataSet, Column


class SchemaAdmin(admin.ModelAdmin):
    fields = ('title', 'user', ('column_separator', 'string_character'))
    list_display = ('title', 'user', 'column_separator', 'string_character')
    list_filter = ('title', 'user')


class DataSetAdmin(admin.ModelAdmin):
    fields = ('schema', 'file', 'status')
    list_display = ('schema', 'status', 'file')
    list_filter = ('schema', 'status')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('column_name', 'column_type', 'schema', 'order')
    list_filter = ('column_name', 'column_type', 'schema')
    fieldsets = (
        ('Main information', {'fields': (('column_name', 'column_type'), 'order'), 'description': 'Each column has name and type and order index'}),
        ('Range properties', {'fields': ('from_range', 'to_range'), 'description': 'Each column might have range'}),
        ('Relation', {'fields': ('schema',), 'description': 'Each column has relation with schema One to Many'})
    )


admin.site.register(Schema, SchemaAdmin)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(Column, ColumnAdmin)
