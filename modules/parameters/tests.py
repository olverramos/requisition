from django.test import TestCase
from modules.parameters.models import (
    FieldType,
    FieldOption,
    RamoField,
    DocumentClassType,
    DocumentClass,
    AvailableDocument,
    Ramo,
)


class FieldTypeModelTest(TestCase):
    def setUp(self):
        self.field_type = FieldType.objects.create(id="TEXT", name="Texto")

    def test_field_type_creation(self):
        self.assertEqual(self.field_type.id, "TEXT")
        self.assertEqual(self.field_type.name, "Texto")

    def test_field_type_str(self):
        self.assertEqual(str(self.field_type), "Texto")

    def test_field_type_ordering(self):
        field_types = FieldType.objects.all()
        self.assertEqual(field_types[0].name, "Texto")

    def test_field_type_verbose_names(self):
        self.assertEqual(self.field_type._meta.verbose_name, "Tipo de Campo")
        self.assertEqual(self.field_type._meta.verbose_name_plural, "Tipos de Campos")

    def test_field_type_db_table(self):
        self.assertEqual(self.field_type._meta.db_table, "parameters_fieldtypes")

    def test_field_type_app_label(self):
        self.assertEqual(self.field_type._meta.app_label, "parameters")


class FieldOptionModelTest(TestCase):
    def setUp(self):
        self.field_type = FieldType.objects.create(id="SELECT", name="Selección")
        self.ramo_field = RamoField.objects.create(
            field_type=self.field_type,
            name="test_field",
            title="Campo de Prueba",
            mandatory=True,
        )
        self.field_option = FieldOption.objects.create(
            field=self.ramo_field,
            value="option1",
            title="Opción 1",
            created_by="testuser",
        )

    def test_field_option_creation(self):
        self.assertEqual(self.field_option.value, "option1")
        self.assertEqual(self.field_option.title, "Opción 1")
        self.assertEqual(self.field_option.field, self.ramo_field)

    def test_field_option_str(self):
        self.assertEqual(str(self.field_option), "option1 - Opción 1")

    def test_field_option_verbose_names(self):
        self.assertEqual(self.field_option._meta.verbose_name, "Opción de Campo")
        self.assertEqual(
            self.field_option._meta.verbose_name_plural, "Opciones de Campos"
        )

    def test_field_option_db_table(self):
        self.assertEqual(self.field_option._meta.db_table, "parameters_fieldoptions")

    def test_field_option_app_label(self):
        self.assertEqual(self.field_option._meta.app_label, "parameters")

    def test_field_option_unique_together(self):
        unique_together = self.field_option._meta.unique_together
        self.assertIn(("field", "value"), unique_together)


class RamoFieldModelTest(TestCase):
    def setUp(self):
        self.field_type = FieldType.objects.create(id="TEXT", name="Texto")
        self.ramo_field = RamoField.objects.create(
            field_type=self.field_type,
            name="test_field",
            title="Campo de Prueba",
            mandatory=True,
            created_by="testuser",
        )

    def test_ramo_field_creation(self):
        self.assertEqual(self.ramo_field.name, "test_field")
        self.assertEqual(self.ramo_field.title, "Campo de Prueba")
        self.assertTrue(self.ramo_field.mandatory)
        self.assertEqual(self.ramo_field.field_type, self.field_type)

    def test_ramo_field_str(self):
        self.assertEqual(str(self.ramo_field), "Campo de Prueba")

    def test_ramo_field_ordering(self):
        ramo_fields = RamoField.objects.all()
        self.assertEqual(ramo_fields[0].name, "test_field")

    def test_ramo_field_verbose_names(self):
        self.assertEqual(self.ramo_field._meta.verbose_name, "Campo de Ramo")
        self.assertEqual(self.ramo_field._meta.verbose_name_plural, "Campos de Ramos")

    def test_ramo_field_db_table(self):
        self.assertEqual(self.ramo_field._meta.db_table, "parameters_ramofields")

    def test_ramo_field_app_label(self):
        self.assertEqual(self.ramo_field._meta.app_label, "parameters")


class DocumentClassTypeModelTest(TestCase):
    def setUp(self):
        self.document_class_type = DocumentClassType.objects.create(
            id="POLICE", name="Póliza"
        )

    def test_document_class_type_creation(self):
        self.assertEqual(self.document_class_type.id, "POLICE")
        self.assertEqual(self.document_class_type.name, "Póliza")

    def test_document_class_type_str(self):
        self.assertEqual(str(self.document_class_type), "Póliza")

    def test_document_class_type_ordering(self):
        document_types = DocumentClassType.objects.all()
        self.assertEqual(document_types[0].name, "Póliza")

    def test_document_class_type_verbose_names(self):
        self.assertEqual(
            self.document_class_type._meta.verbose_name, "Tipo de Documento"
        )
        self.assertEqual(
            self.document_class_type._meta.verbose_name_plural, "Tipos de Documentos"
        )

    def test_document_class_type_db_table(self):
        self.assertEqual(
            self.document_class_type._meta.db_table, "parameters_documentclasstypes"
        )

    def test_document_class_type_app_label(self):
        self.assertEqual(self.document_class_type._meta.app_label, "parameters")


class DocumentClassModelTest(TestCase):
    def setUp(self):
        self.document_class_type = DocumentClassType.objects.create(
            id="POLICE", name="Póliza"
        )
        self.document_class = DocumentClass.objects.create(
            id="POLICE_MAIN",
            name="Póliza Principal",
            document_type=self.document_class_type,
            created_by="testuser",
        )

    def test_document_class_creation(self):
        self.assertEqual(self.document_class.id, "POLICE_MAIN")
        self.assertEqual(self.document_class.name, "Póliza Principal")
        self.assertEqual(self.document_class.document_type, self.document_class_type)

    def test_document_class_str(self):
        self.assertEqual(str(self.document_class), "Póliza Principal")

    def test_document_class_ordering(self):
        document_classes = DocumentClass.objects.all()
        self.assertEqual(document_classes[0].name, "Póliza Principal")

    def test_document_class_verbose_names(self):
        self.assertEqual(self.document_class._meta.verbose_name, "Clase de Documento")
        self.assertEqual(
            self.document_class._meta.verbose_name_plural, "Clases de Documentos"
        )

    def test_document_class_db_table(self):
        self.assertEqual(
            self.document_class._meta.db_table, "parameters_documentclasses"
        )

    def test_document_class_app_label(self):
        self.assertEqual(self.document_class._meta.app_label, "parameters")


class AvailableDocumentModelTest(TestCase):
    def test_available_document_creation(self):
        available_doc = AvailableDocument(
            name="test_doc", title="Documento de Prueba", mandatory=True
        )
        self.assertEqual(available_doc.name, "test_doc")
        self.assertEqual(available_doc.title, "Documento de Prueba")
        self.assertTrue(available_doc.mandatory)

    def test_available_document_str(self):
        available_doc = AvailableDocument(
            name="test_doc", title="Documento de Prueba", mandatory=True
        )
        self.assertEqual(str(available_doc), "Documento de Prueba")


class RamoModelTest(TestCase):
    def setUp(self):
        self.field_type = FieldType.objects.create(id="TEXT", name="Texto")
        self.ramo_field = RamoField.objects.create(
            field_type=self.field_type,
            name="test_field",
            title="Campo de Prueba",
            mandatory=True,
        )
        self.document_class_type = DocumentClassType.objects.create(
            id="POLICE", name="Póliza"
        )
        self.document_class = DocumentClass.objects.create(
            id="POLICE_MAIN",
            name="Póliza Principal",
            document_type=self.document_class_type,
        )
        self.ramo = Ramo.objects.create(id="VIDA", name="Vida", created_by="testuser")

    def test_ramo_creation(self):
        self.assertEqual(self.ramo.id, "VIDA")
        self.assertEqual(self.ramo.name, "Vida")

    def test_ramo_str(self):
        self.assertEqual(str(self.ramo), "Vida")

    def test_ramo_ordering(self):
        ramos = Ramo.objects.all()
        self.assertEqual(ramos[0].name, "Vida")

    def test_ramo_verbose_names(self):
        self.assertEqual(self.ramo._meta.verbose_name, "Ramo")
        self.assertEqual(self.ramo._meta.verbose_name_plural, "Ramos")

    def test_ramo_db_table(self):
        self.assertEqual(self.ramo._meta.db_table, "parameters_ramos")

    def test_ramo_app_label(self):
        self.assertEqual(self.ramo._meta.app_label, "parameters")

    def test_ramo_with_fields(self):
        self.ramo.ramo_fields = [self.ramo_field]
        self.ramo.save()
        self.assertEqual(len(self.ramo.ramo_fields), 1)

    def test_ramo_with_document_classes(self):
        self.ramo.document_classes = [self.document_class]
        self.ramo.save()
        self.assertEqual(len(self.ramo.document_classes), 1)
