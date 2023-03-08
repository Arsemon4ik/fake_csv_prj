from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from fake_csv_app.utils.utils import create_fake_csv, check_order_duplicates
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import PermissionDenied

from .models import Schema, DataSet, Column
from .forms import SchemaForm, ColumnFormSet


class SchemaInline:
    form_class = SchemaForm
    model = Schema
    template_name = "create_update_schema.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        self.object = form
        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('schemas')

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        columns = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for column in columns:
            column.schema = self.object
            column.save()


class SchemaCreate(SchemaInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(SchemaCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'images': ColumnFormSet(prefix='images'),
            }
        else:
            return {
                'images': ColumnFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }


class SchemaUpdate(SchemaInline, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super(SchemaUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['user'] = self.object.user
        return ctx

    def get_named_formsets(self):
        return {
            'images': ColumnFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }

    # override get method to prevent updating by other user
    def get(self, request, *args, **kwargs):
        schema = self.get_object()
        if request.user != schema.user:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


def delete_column_view(request, column_id):
    try:
        column = Column.objects.get(id=column_id)
        if request.user == column.schema.user:
            column.delete()
        else:
            raise PermissionDenied()
    except Column.DoesNotExist:
        messages.error(
            request, 'Column Does not exit'
            )
        return redirect('schemas')

    return redirect('update_schema', pk=column.schema.id)


def login_page(request):
    """ Login view to retrieve data and authenticate user """

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('schemas')
        else:
            messages.error(request, 'Incorrect email or password')

    return render(request, "login.html")


@login_required
def logout_view(request):
    """ Logout view to log out user if logged in """

    logout(request)
    return redirect('login')


@login_required
def data_schemas_page(request):
    """ Data schemas function returns a template with schemas from DB based on user """

    schemas = Schema.objects.filter(user=request.user)
    context = {'schemas': schemas}
    return render(request, "data_schemas.html", context=context)


@login_required
def delete_schema_view(request, schema_id):
    """ Data schemas delete view deletes the schema from DB based on schema_id """

    try:
        schema = Schema.objects.get(id=schema_id)
        if request.user == schema.user:
            schema.delete()
        else:
            raise PermissionDenied()
    except Schema.DoesNotExist:
        return redirect('schemas')

    return redirect('schemas')


@login_required
def data_sets_page(request, schema_id):
    """ Data sets function returns a template with data sets from DB based on schema_id and user"""

    try:
        schema = Schema.objects.get(user=request.user, id=schema_id)
        columns = schema.column_set.all()
        sets = schema.dataset_set.all()
    except Schema.DoesNotExist:
        return redirect('schemas')

    context = {
        'schema': schema,
        'columns': columns,
        'data_sets': sets,
    }
    return render(request, "data_sets.html", context=context)


# TODO: IMPLEMENT CHECKING USER BASED ON SCHEMA__USER
def create_dataset(request):
    """ Create dataset function generate csv file and returns JSON response based on if file was created or not """

    if request.method == "POST" and request.is_ajax():
        # get the form data
        rows = int(request.POST.get('rows', None))
        schema_id = request.POST.get('schema_id', None)

        # if schema with id schema_id exists, create new data set
        if (schema := Schema.objects.filter(id=schema_id)).exists():
            columns = schema[0].column_set.all()

            tuple_header_types_order = columns.values_list('column_name',
                                                           'column_type',
                                                           'order',
                                                           'from_range',
                                                           'to_range',
                                                            )
            field_order = [field_type[2] for field_type in tuple_header_types_order]
            # check order duplicates
            if check_order_duplicates(field_order):
                return JsonResponse({"error": "Order values are repeated! Please change ordering"}, status=400)

            # Retrieve fields for creating csv file
            field_names = [column_name[0] for column_name in tuple_header_types_order]
            field_types = [field_type[1] for field_type in tuple_header_types_order]
            field_range = [(field_type[3], field_type[4]) for field_type in tuple_header_types_order]

            filename = schema[0].title
            column_separator = schema[0].column_separator
            string_character = schema[0].string_character

            # creating csv file and return path
            csv_path = create_fake_csv(filename=filename,
                                       fieldnames=field_names,
                                       order=field_order,
                                       field_range=field_range,
                                       delimiter=column_separator,
                                       string_character=string_character,
                                       field_types=field_types,
                                       rows=rows)

            # create data set if all is fine :)
            data_set = DataSet.objects.create(schema=schema[0])

            # write to the new dataset path of the file and update the status to True
            data_set.file = csv_path
            data_set.status = True
            data_set.save()

            # fake processing
            import time
            time.sleep(1)

            return JsonResponse({"filepath": data_set.file.url}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": "Incorrect schema id or number of rows"}, status=400)

        # some error occured
    return JsonResponse({"error": "Fatal error"}, status=400)


def get_last_dataset_view(request, schema_id):
    """ Get last dataset view returns JSON response with data -> a number of last created field based on schema_id """

    try:
        schema = Schema.objects.get(id=schema_id)
        if request.user != schema.user:
            raise PermissionDenied()
    except Schema.DoesNotExist:
        JsonResponse({"error": "Schema doesn't exist"})

    count_datasets = DataSet.objects.filter(schema__id=schema_id).count()
    return JsonResponse({'data': count_datasets})
