from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel
from django.db import models
import datetime
import json

module_folder = 'modules/parameters'


class FieldType(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=10)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/fieldtypes.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            field_type = FieldType.objects.get(id=data["id"])
                        except FieldType.DoesNotExist:
                            field_type = FieldType()
                            field_type.id = data['id']
                            field_type.name = data['name']
                            field_type.save()

                            print (f'Tipo de Campo {field_type} creada')

        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_fieldtypes'
        verbose_name = 'Tipo de Campo'
        verbose_name_plural = 'Tipos de Campos'
        ordering = ['name']


class FieldOption(models.Model):
    field = models.ForeignKey('RamoField', verbose_name="Campo", on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Valor')
    title = models.CharField(verbose_name='Nombre')
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'parameters_fieldoptions',
        'ordering': ['title'],
        'indexes': [
            ('title',), 
        ]
    }
    
    def __str__(self):
        return f"{self.value} - {self.title}"
    

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_fieldoptions'
        verbose_name = 'Opción de Campo'
        verbose_name_plural = 'Opciones de Campos'
        ordering = ['field', 'title']
        unique_together = ('field', 'value',)


class RamoField(models.Model):
    field_type = models.ForeignKey(FieldType, verbose_name="Tipo de Campo", on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Nombre', unique=True)
    title = models.CharField(verbose_name='Título', db_index=True)
    mandatory = models.BooleanField(verbose_name="Es Obligatorio", default=False)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/ramofields.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    field_type = None
                    if 'field_type' in data.keys():
                        field_type_id = data["field_type"]
                        try:
                            field_type = FieldType.objects.get(pk=field_type_id)
                        except FieldType.DoesNotExist:
                            print (f"Tipo de Campo {field_type} no Existe")
                            field_type = None
                    
                    if field_type is not None and 'name' in data.keys() and 'title' in data.keys():
                        mandatory = False
                        if 'mandatory' in data.keys():
                            mandatory = data["mandatory"]
                    
                        try:
                            ramo_field = RamoField.objects.get(name=data["name"])
                        except RamoField.DoesNotExist:
                            ramo_field = RamoField()
                            ramo_field.field_type = field_type
                            ramo_field.name = data['name']
                            ramo_field.title = data['title']
                            ramo_field.mandatory = mandatory
                            ramo_field.options = []
                            if 'options' in data.keys():
                                for option_data in data["options"]:
                                    if 'value' in option_data.keys() and 'title' in option_data.keys():
                                        option = FieldOption()
                                        option.field = ramo_field
                                        option.value = option_data['value']
                                        option.title = option_data['title']
                                        option.created_at = datetime.now()
                                        option.created_by = 'System'
                                        option.updated_at = datetime.now()
                                        option.updated_by = 'System'
                                        option.save()
                            ramo_field.save()

                            print (f'Campo {ramo_field} creado')

        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_ramofields'
        verbose_name = 'Campo de Ramo'
        verbose_name_plural = 'Campos de Ramos'
        ordering = ['name']


class DocumentClassType(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=20)
    name = models.CharField(verbose_name='Nombre')

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/documentclasstypes.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'name' in data.keys() and 'id' in data.keys():
                        try:
                            document_type = DocumentClassType.objects.get(id=data["id"])
                        except DocumentClassType.DoesNotExist:
                            document_type = DocumentClassType()
                            document_type.name = data['name']
                            document_type.id = data['id']
                            document_type.save()

                            print (f'Tipo de Documento {document_type} creada')
                    
        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_documentclasstypes'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['name']


class DocumentClass(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=20)
    name = models.CharField(verbose_name='Nombre')
    document_type = models.ForeignKey('DocumentClassType', verbose_name="Tipo de Documento", on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/documentclasses.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:

                    document_type = None
                    
                    if 'document_type' in data.keys():
                        document_type_id = data["document_type"]
                        try:
                            document_type = DocumentClassType.objects.get(pk=document_type_id)
                        except DocumentClassType.DoesNotExist:
                            print (f"Tipo de Documento {document_type} no Existe")
                            document_type = None

                    if 'name' in data.keys() and 'id' in data.keys() and document_type is not None:
                        try:
                            document_class = DocumentClass.objects.get(id=data["id"])
                        except DocumentClass.DoesNotExist:
                            document_class = DocumentClass()
                            document_class.id = data['id']
                            document_class.name = data['name']
                            document_class.document_type = document_type
                            document_class.created_at = datetime.datetime.now()
                            document_class.save()

                            print (f'Clase de Documento {document_class} creada')
                    
        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_documentclasses'
        verbose_name = 'Clase de Documento'
        verbose_name_plural = 'Clases de Documentos'
        ordering = ['name']


class AvailableDocument(EmbeddedModel):
    name = models.CharField(verbose_name='Nombre')
    title = models.CharField(verbose_name='Título')
    mandatory = models.BooleanField(verbose_name="Es Obligatorio", default=False)

    def __str__(self):
        return f"{self.title}"


class Ramo(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=20)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    ramo_fields = ArrayField(
        models.ForeignKey('RamoField', on_delete=models.CASCADE), blank=True,
    )
    document_classes = ArrayField(
        models.ForeignKey('DocumentClass', on_delete=models.CASCADE), blank=True,
    )
    available_documents = ArrayField( 
        EmbeddedModelField('AvailableDocument'), blank=True,
    )
    created_at = models.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True, auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True, auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def fix_document_classes():
        ramo_list = Ramo.objects.all()
        for ramo in ramo_list:
            ramo.document_classes = []
            for available_document in ramo.available_documents:
                try:
                    document_class = DocumentClass.objects.get(name=available_document.name)
                    ramo.document_classes.append(document_class)
                except DocumentClass.DoesNotExist:
                    print (f"Clase de Documento {available_document.name} no Existe")

            ramo.save()

    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/ramos.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            ramo = Ramo.objects.get(id=data["id"])
                        except Ramo.DoesNotExist:
                            ramo = Ramo()
                            ramo.id = data['id']
                            ramo.name = data['name']
                            ramo.ramo_fields = []
                            if 'fields' in data.keys():
                                for field_name in data['fields']:
                                    try:
                                        ramo_field = RamoField.objects.get(name=field_name)
                                        ramo.ramo_fields.append(ramo_field)
                                    except RamoField.DoesNotExist:
                                        print (f"Campo {field_name} no Existe")
                                        ramo_field = None

                            ramo.document_classes = []
                            if 'document_classes' in data.keys():
                                for document_class_name in data['document_classes']:
                                    try:
                                        document_class = DocumentClass.objects.get(name=document_class_name)
                                        ramo.document_classes.append(document_class)
                                    except DocumentClass.DoesNotExist:
                                        print (f"Clase de Documento {document_class_name} no Existe")
                                        document_class = None

                            ramo.created_at = datetime.datetime.now()
                            ramo.save()

                            print (f'Ramo {ramo} creada')
        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_ramos'
        verbose_name = 'Ramo'
        verbose_name_plural = 'Ramos'
        ordering = ['name']
