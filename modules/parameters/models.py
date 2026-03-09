from django.db import models
import datetime
import json

module_folder = 'modules/parameters'


class FieldType(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=10)
    name = models.CharField(max_length=100, verbose_name='Nombre')

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


class DocumentClassType(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=20)
    name = models.CharField(verbose_name='Nombre', max_length=100)

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
    name = models.CharField(verbose_name='Nombre', max_length=100)
    document_type = models.ForeignKey('DocumentClassType', verbose_name="Tipo de Documento", on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
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
                            document_class.created_by = 'System'
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


class Ramo(models.Model):
    id = models.CharField(verbose_name='ID', primary_key=True, max_length=20)
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
                            ramo.created_by = 'System'
                            ramo.save()

                            if 'fields' in data.keys():
                                for field_data in data['fields']:
                                    field_type = None
                                    try:
                                        field_type = FieldType.objects.get(id=field_data['field_type'])
                                    except FieldType.DoesNotExist:
                                        print (f"Tipo de Campo {field_data['field_type']} no Existe")
                                        field_type = None

                                    if field_type is not None and 'name' in field_data.keys():
                                        field_name = field_data['name']
                                        try:
                                            ramo_field = RamoField.objects.get(
                                                ramo=ramo,
                                                name=field_name
                                            )
                                        except RamoField.DoesNotExist:
                                            ramo_field = RamoField()
                                            ramo_field.ramo = ramo
                                            ramo_field.name = field_name
                                            ramo_field.field_type = field_type
                                            if 'title' in field_data.keys() and field_data['title']:
                                                ramo_field.title = field_data['title']
                                            else:
                                                ramo_field.title = field_name
                                            ramo_field.mandatory = False
                                            if 'mandatory' in field_data.keys() and field_data['mandatory']:
                                                ramo_field.mandatory = field_data['mandatory']
                                            ramo_field.created_by = 'System'
                                            ramo_field.save()

                                            print (f'Campo {ramo_field} del Ramo {ramo} creado')
                                        
                            if 'required_documents' in data.keys():
                                for required_document_data in data['required_documents']:
                                    document_class_id = required_document_data['document_class']
                                    try:
                                        document_class = DocumentClass.objects.get(pk=document_class_id)
                                    except DocumentClass.DoesNotExist:
                                        print (f"Clase de Documento {document_class_id} no Existe")
                                        document_class = None
                                    if document_class is not None:
                                        try:
                                            ramo_required_document = RamoRequiredDocument.objects.get(
                                                ramo=ramo,
                                                document_class=document_class
                                            )
                                        except RamoRequiredDocument.DoesNotExist:
                                            ramo_required_document = RamoRequiredDocument()
                                            ramo_required_document.ramo = ramo
                                            ramo_required_document.document_class = document_class
                                            ramo_required_document.mandatory = False
                                            if 'mandatory' in required_document_data.keys() and required_document_data['mandatory']:
                                                ramo_required_document.mandatory = required_document_data['mandatory']
                                            ramo_required_document.created_by = 'System'
                                            ramo_required_document.save()

                                            print (f'Documento requerido {ramo_required_document} del Ramo {ramo} creado')

                            print (f'Ramo {ramo} creado')
        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_ramos'
        verbose_name = 'Ramo'
        verbose_name_plural = 'Ramos'
        ordering = ['name']


class RamoField(models.Model):
    ramo = models.ForeignKey('Ramo', verbose_name="Ramo", on_delete=models.CASCADE)
    field_type = models.ForeignKey('FieldType', verbose_name="Tipo de Campo", on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Nombre', max_length=100)
    title = models.CharField(verbose_name='Título', db_index=True, max_length=100)
    mandatory = models.BooleanField(verbose_name="Es Obligatorio", default=False)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    def __repr__(self):
        return f"{self.ramo} - {self.title}"

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_ramofields'
        verbose_name = 'Campo de Ramo'
        verbose_name_plural = 'Campos de Ramos'
        ordering = ['name']
        unique_together = ('ramo', 'name', )


class FieldOption(models.Model):
    field = models.ForeignKey('RamoField', verbose_name="Campo", on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Valor', max_length=50)
    title = models.CharField(verbose_name='Nombre', max_length=100)

    def __str__(self):
        return f"{self.value} - {self.title}"

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_fieldoptions'
        verbose_name = 'Opción de Campo'
        verbose_name_plural = 'Opciones de Campos'
        ordering = ['field', 'title']
        unique_together = ('field', 'value',)


class RamoRequiredDocument(models.Model):
    ramo = models.ForeignKey('Ramo', verbose_name="Ramo", on_delete=models.CASCADE)
    document_class = models.ForeignKey('DocumentClass', verbose_name="Clase de Documento", on_delete=models.CASCADE)
    mandatory = models.BooleanField(verbose_name="Es Obligatorio", default=False)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    def __repr__(self):
        return f"{self.ramo} - {self.document_class}"

    def __str__(self):
        return f"{self.document_class.name}"

    class Meta:
        app_label = 'parameters'
        db_table = 'parameters_ramorequireddocuments'
        verbose_name = 'Documento Requerido para Ramo'
        verbose_name_plural = 'Documentos Requeridos para Ramos'
        ordering = ['ramo', 'document_class']
        unique_together = ('ramo', 'document_class', )
