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
        return f"{self.name}"
    
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

class AvailableDocument(EmbeddedDocument):
    name = fields.StringField(verbose_name='Nombre')
    title = fields.StringField(verbose_name='Título')
    mandatory = fields.BooleanField(verbose_name="Es Obligatorio", dafault=False)


class Ramo(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=20)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    ramo_fields = fields.ListField(
        fields.ReferenceField(RamoField), blank=True,
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

                            ramo.available_documents = []
                            if 'available_documents' in data.keys():
                                for available_documents_data in data['available_documents']:
                                    if 'name' in available_documents_data.keys():
                                        name = available_documents_data["name"]
                                        title = available_documents_data["title"]
                                        mandatory = False
                                        if 'mandatory' in available_documents_data.keys():
                                            mandatory = available_documents_data["mandatory"]
                                        
                                        available_document = AvailableDocument()
                                        available_document.name = name
                                        available_document.title = title
                                        available_document.mandatory = mandatory
                                    ramo.available_documents.append(available_document)
                            
                            ramo.created_at = datetime.datetime.now()
                            ramo.save()

                            print (f'Ramo {ramo} creada')
        except FileNotFoundError:
            pass
