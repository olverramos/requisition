from django_mongoengine import Document, fields, EmbeddedDocument
import datetime
import json

module_folder = 'modules/parameters'


class FieldType(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(max_length=100, verbose_name='Nombre')

    meta = {
        'collection': 'parameters_fieldtypes',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }
    
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


class FieldOption(EmbeddedDocument):
    value = fields.StringField(verbose_name='Valor')
    title = fields.StringField(verbose_name='Nombre')

    def __str__(self):
        return f"{self.title}"
    

class RamoField(Document):
    field_type = fields.ReferenceField(FieldType, verbose_name="Tipo de Campo")
    name = fields.StringField(verbose_name='Nombre', unique=True)
    title = fields.StringField(verbose_name='Título', unique=True)
    mandatory = fields.BooleanField(verbose_name="Es Obligatorio", dafault=False)
    options = fields.ListField(
        fields.EmbeddedDocumentField('FieldOption'), blank=True,
    )

    meta = {
        'collection': 'parameters_ramofields',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }
    
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
                                        option.value = option_data['value']
                                        option.title = option_data['title']
                                        ramo_field.options.append(option)
                            ramo_field.save()

                            print (f'Campo {ramo_field} creado')

        except FileNotFoundError:
            pass


class DocumentClassType(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=20)
    name = fields.StringField(verbose_name='Nombre')

    def __str__(self):
        return f"{self.name}"

    meta = {
        'collection': 'parameters_documentclasstypes',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }

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

class DocumentClass(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=20)
    name = fields.StringField(verbose_name='Nombre')
    document_type = fields.ReferenceField(DocumentClassType, verbose_name="Tipo de Documento")
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    meta = {
        'collection': 'parameters_documentclasses',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }
    
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

class AvailableDocument(EmbeddedDocument):
    name = fields.StringField(verbose_name='Nombre')
    title = fields.StringField(verbose_name='Título')
    mandatory = fields.BooleanField(verbose_name="Es Obligatorio", dafault=False)

    def __str__(self):
        return f"{self.title}"

class Ramo(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=20)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    ramo_fields = fields.ListField(
        fields.ReferenceField(RamoField), blank=True,
    )
    document_classes = fields.ListField(
        fields.ReferenceField(DocumentClass), blank=True,
    )
    available_documents = fields.ListField( 
        fields.EmbeddedDocumentField(AvailableDocument), blank=True,
    )
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'parameters_ramos',
        'ordering': ['name'],
        'indexes': [
            ('name',), 
        ]
    }
    
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
