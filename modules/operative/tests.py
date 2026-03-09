from django.test import TestCase
from modules.operative.models import (
    RequestStatus,
    RequestDocument,
    OperativeRequestDocument,
    RequestFile,
    OperativeRequest,
    RequestEvent,
    RequestFieldValue,
)
from modules.base.models import PersonType, DocumentType, Applicant, Taker
from modules.localization.models import Country, State, City
from modules.parameters.models import (
    FieldType,
    RamoField,
    DocumentClassType,
    DocumentClass,
    Ramo,
)
from django.contrib.auth.models import User
from modules.auths.models import Account, Genre, Role


class RequestStatusModelTest(TestCase):
    def setUp(self):
        self.status = RequestStatus.objects.create(id="1", name="Pendiente")

    def test_request_status_creation(self):
        self.assertEqual(self.status.id, "1")
        self.assertEqual(self.status.name, "Pendiente")

    def test_request_status_str(self):
        self.assertEqual(str(self.status), "Pendiente")

    def test_request_status_ordering(self):
        statuses = RequestStatus.objects.all()
        self.assertEqual(statuses[0].name, "Pendiente")

    def test_request_status_verbose_names(self):
        self.assertEqual(self.status._meta.verbose_name, "Estado de Solicitud")
        self.assertEqual(self.status._meta.verbose_name_plural, "Estados de Solicitud")

    def test_request_status_db_table(self):
        self.assertEqual(self.status._meta.db_table, "operative_requeststatuses")

    def test_request_status_app_label(self):
        self.assertEqual(self.status._meta.app_label, "operative")


class RequestDocumentEmbeddedModelTest(TestCase):
    def test_request_document_creation(self):
        request_doc = RequestDocument(
            document_name="test_doc",
            document_title="Documento de Prueba",
            filename="test.pdf",
            file_type="application/pdf",
            content="base64content",
        )
        self.assertEqual(request_doc.document_name, "test_doc")
        self.assertEqual(request_doc.document_title, "Documento de Prueba")
        self.assertEqual(request_doc.filename, "test.pdf")
        self.assertEqual(request_doc.file_type, "application/pdf")
        self.assertEqual(request_doc.content, "base64content")

    def test_request_document_str(self):
        request_doc = RequestDocument(
            document_name="test_doc",
            document_title="Documento de Prueba",
            filename="test.pdf",
            file_type="application/pdf",
            content="base64content",
        )
        self.assertEqual(str(request_doc), "test_doc - test.pdf")


class RequestFileEmbeddedModelTest(TestCase):
    def test_request_file_creation(self):
        request_file = RequestFile(
            filename="test.pdf", file_type="application/pdf", content="base64content"
        )
        self.assertEqual(request_file.filename, "test.pdf")
        self.assertEqual(request_file.file_type, "application/pdf")
        self.assertEqual(request_file.content, "base64content")

    def test_request_file_str(self):
        request_file = RequestFile(
            filename="test.pdf", file_type="application/pdf", content="base64content"
        )
        self.assertEqual(str(request_file), "test.pdf")


class OperativeRequestDocumentModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            id="CO", name="Colombia", capital_code="BO"
        )
        self.state = State.objects.create(
            country=self.country,
            code="DC",
            short="DC",
            name="Distrito Capital",
            capital_code="01",
        )
        self.city = City.objects.create(
            country=self.country, state=self.state, code="01", name="Bogotá"
        )
        self.person_type = PersonType.objects.create(id="NAT", name="Natural")
        self.document_type = DocumentType.objects.create(
            id="CC", name="Cédula de Ciudadanía", person_type=self.person_type
        )
        self.applicant = Applicant.objects.create(
            identification="1234567890",
            name="Juan Pérez",
            email="juan@example.com",
            phone_number="1234567890",
            state=self.state,
            city=self.city,
        )
        self.taker = Taker.objects.create(
            person_type=self.person_type,
            document_type=self.document_type,
            identification="1234567890",
            name="Empresa Test SAS",
            email="test@empresa.com",
            phone_number="1234567890",
            contact_name="Juan Pérez",
            address="Calle 123",
            state=self.state,
            city=self.city,
        )
        self.field_type = FieldType.objects.create(id="TEXT", name="Texto")
        self.ramo = Ramo.objects.create(id="VIDA", name="Vida")
        self.status = RequestStatus.objects.create(id="1", name="Pendiente")
        self.document_class_type = DocumentClassType.objects.create(
            id="POLICE", name="Póliza"
        )
        self.document_class = DocumentClass.objects.create(
            id="POLICE_MAIN",
            name="Póliza Principal",
            document_type=self.document_class_type,
        )
        self.operative_request = OperativeRequest.objects.create(
            applicant=self.applicant,
            taker=self.taker,
            ramo=self.ramo,
            number=1,
            value=1000000,
            status=self.status,
            created_by="testuser",
        )
        self.operative_request_document = OperativeRequestDocument.objects.create(
            operative_request=self.operative_request,
            document_class=self.document_class,
            title="Póliza Principal",
            filename="poliza.pdf",
            file_type="application/pdf",
            content="base64content",
            created_by="testuser",
        )

    def test_operative_request_document_creation(self):
        self.assertEqual(
            self.operative_request_document.operative_request, self.operative_request
        )
        self.assertEqual(
            self.operative_request_document.document_class, self.document_class
        )
        self.assertEqual(self.operative_request_document.title, "Póliza Principal")
        self.assertEqual(self.operative_request_document.filename, "poliza.pdf")
        self.assertEqual(self.operative_request_document.file_type, "application/pdf")
        self.assertEqual(self.operative_request_document.content, "base64content")
        self.assertEqual(self.operative_request_document.created_by, "testuser")

    def test_operative_request_document_str(self):
        expected = f"{self.operative_request} - {self.document_class} - poliza.pdf"
        self.assertEqual(str(self.operative_request_document), expected)

    def test_operative_request_document_verbose_names(self):
        self.assertEqual(
            self.operative_request_document._meta.verbose_name, "Documento de Solicitud"
        )
        self.assertEqual(
            self.operative_request_document._meta.verbose_name_plural,
            "Documentos de Solicitud",
        )

    def test_operative_request_document_db_table(self):
        self.assertEqual(
            self.operative_request_document._meta.db_table, "operative_requestdocuments"
        )

    def test_operative_request_document_app_label(self):
        self.assertEqual(self.operative_request_document._meta.app_label, "operative")


class OperativeRequestModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            id="CO", name="Colombia", capital_code="BO"
        )
        self.state = State.objects.create(
            country=self.country,
            code="DC",
            short="DC",
            name="Distrito Capital",
            capital_code="01",
        )
        self.city = City.objects.create(
            country=self.country, state=self.state, code="01", name="Bogotá"
        )
        self.person_type = PersonType.objects.create(id="NAT", name="Natural")
        self.document_type = DocumentType.objects.create(
            id="CC", name="Cédula de Ciudadanía", person_type=self.person_type
        )
        self.applicant = Applicant.objects.create(
            identification="1234567890",
            name="Juan Pérez",
            email="juan@example.com",
            phone_number="1234567890",
            state=self.state,
            city=self.city,
        )
        self.taker = Taker.objects.create(
            person_type=self.person_type,
            document_type=self.document_type,
            identification="1234567890",
            name="Empresa Test SAS",
            email="test@empresa.com",
            phone_number="1234567890",
            contact_name="Juan Pérez",
            address="Calle 123",
            state=self.state,
            city=self.city,
        )
        self.ramo = Ramo.objects.create(id="VIDA", name="Vida")
        self.status = RequestStatus.objects.create(id="1", name="Pendiente")
        self.operative_request = OperativeRequest.objects.create(
            applicant=self.applicant,
            taker=self.taker,
            ramo=self.ramo,
            number=1,
            value=1000000,
            status=self.status,
            observations="Test observations",
            created_by="testuser",
        )

    def test_operative_request_creation(self):
        self.assertEqual(self.operative_request.applicant, self.applicant)
        self.assertEqual(self.operative_request.taker, self.taker)
        self.assertEqual(self.operative_request.ramo, self.ramo)
        self.assertEqual(self.operative_request.number, 1)
        self.assertEqual(self.operative_request.value, 1000000)
        self.assertEqual(self.operative_request.status, self.status)
        self.assertEqual(self.operative_request.observations, "Test observations")
        self.assertEqual(self.operative_request.created_by, "testuser")

    def test_operative_request_str(self):
        expected = f"{self.operative_request.number} - {self.taker}"
        self.assertEqual(str(self.operative_request), expected)

    def test_operative_request_with_assigned_to(self):
        self.user = User.objects.create_user(
            username="admin", password="admin123", email="admin@example.com"
        )
        self.role = Role.objects.create(id="admin", name="Administrador")
        self.account = Account.objects.create(
            user=self.user, role=self.role, created_by="testuser"
        )
        self.operative_request.assigned_to = self.account
        self.operative_request.assigned_by = "testuser"
        self.operative_request.save()

        self.assertEqual(self.operative_request.assigned_to, self.account)
        self.assertEqual(self.operative_request.assigned_by, "testuser")

    def test_operative_request_ordering(self):
        requests = OperativeRequest.objects.all()
        self.assertEqual(requests[0].number, 1)

    def test_operative_request_verbose_names(self):
        self.assertEqual(self.operative_request._meta.verbose_name, "Solicitud")
        self.assertEqual(
            self.operative_request._meta.verbose_name_plural, "Solicitudes"
        )

    def test_operative_request_db_table(self):
        self.assertEqual(
            self.operative_request._meta.db_table, "operative_operativerequests"
        )

    def test_operative_request_app_label(self):
        self.assertEqual(self.operative_request._meta.app_label, "operative")


class RequestEventModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            id="CO", name="Colombia", capital_code="BO"
        )
        self.state = State.objects.create(
            country=self.country,
            code="DC",
            short="DC",
            name="Distrito Capital",
            capital_code="01",
        )
        self.city = City.objects.create(
            country=self.country, state=self.state, code="01", name="Bogotá"
        )
        self.person_type = PersonType.objects.create(id="NAT", name="Natural")
        self.document_type = DocumentType.objects.create(
            id="CC", name="Cédula de Ciudadanía", person_type=self.person_type
        )
        self.applicant = Applicant.objects.create(
            identification="1234567890",
            name="Juan Pérez",
            email="juan@example.com",
            phone_number="1234567890",
            state=self.state,
            city=self.city,
        )
        self.taker = Taker.objects.create(
            person_type=self.person_type,
            document_type=self.document_type,
            identification="1234567890",
            name="Empresa Test SAS",
            email="test@empresa.com",
            phone_number="1234567890",
            contact_name="Juan Pérez",
            address="Calle 123",
            state=self.state,
            city=self.city,
        )
        self.ramo = Ramo.objects.create(id="VIDA", name="Vida")
        self.status = RequestStatus.objects.create(id="1", name="Pendiente")
        self.operative_request = OperativeRequest.objects.create(
            applicant=self.applicant,
            taker=self.taker,
            ramo=self.ramo,
            number=1,
            value=1000000,
            status=self.status,
            created_by="testuser",
        )
        self.request_event = RequestEvent.objects.create(
            operative_request=self.operative_request,
            status=self.status,
            observations="Evento de prueba",
            created_by="testuser",
        )

    def test_request_event_creation(self):
        self.assertEqual(self.request_event.operative_request, self.operative_request)
        self.assertEqual(self.request_event.status, self.status)
        self.assertEqual(self.request_event.observations, "Evento de prueba")
        self.assertEqual(self.request_event.created_by, "testuser")

    def test_request_event_verbose_names(self):
        self.assertEqual(self.request_event._meta.verbose_name, "Evento de Solicitud")
        self.assertEqual(
            self.request_event._meta.verbose_name_plural, "Eventos de Solicitud"
        )

    def test_request_event_db_table(self):
        self.assertEqual(self.request_event._meta.db_table, "operative_requestevents")

    def test_request_event_app_label(self):
        self.assertEqual(self.request_event._meta.app_label, "operative")

    def test_request_event_ordering(self):
        events = RequestEvent.objects.all()
        self.assertEqual(events[0], self.request_event)


class RequestFieldValueModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            id="CO", name="Colombia", capital_code="BO"
        )
        self.state = State.objects.create(
            country=self.country,
            code="DC",
            short="DC",
            name="Distrito Capital",
            capital_code="01",
        )
        self.city = City.objects.create(
            country=self.country, state=self.state, code="01", name="Bogotá"
        )
        self.person_type = PersonType.objects.create(id="NAT", name="Natural")
        self.document_type = DocumentType.objects.create(
            id="CC", name="Cédula de Ciudadanía", person_type=self.person_type
        )
        self.applicant = Applicant.objects.create(
            identification="1234567890",
            name="Juan Pérez",
            email="juan@example.com",
            phone_number="1234567890",
            state=self.state,
            city=self.city,
        )
        self.taker = Taker.objects.create(
            person_type=self.person_type,
            document_type=self.document_type,
            identification="1234567890",
            name="Empresa Test SAS",
            email="test@empresa.com",
            phone_number="1234567890",
            contact_name="Juan Pérez",
            address="Calle 123",
            state=self.state,
            city=self.city,
        )
        self.field_type = FieldType.objects.create(id="TEXT", name="Texto")
        self.ramo_field = RamoField.objects.create(
            field_type=self.field_type, name="test_field", title="Campo de Prueba"
        )
        self.ramo = Ramo.objects.create(id="VIDA", name="Vida")
        self.status = RequestStatus.objects.create(id="1", name="Pendiente")
        self.operative_request = OperativeRequest.objects.create(
            applicant=self.applicant,
            taker=self.taker,
            ramo=self.ramo,
            number=1,
            value=1000000,
            status=self.status,
            created_by="testuser",
        )
        self.request_field_value = RequestFieldValue.objects.create(
            operative_request=self.operative_request,
            field=self.ramo_field,
            value="Valor de prueba",
        )

    def test_request_field_value_creation(self):
        self.assertEqual(
            self.request_field_value.operative_request, self.operative_request
        )
        self.assertEqual(self.request_field_value.field, self.ramo_field)
        self.assertEqual(self.request_field_value.value, "Valor de prueba")

    def test_request_field_value_str(self):
        expected = f"{self.ramo_field.name}: Valor de prueba"
        self.assertEqual(str(self.request_field_value), expected)

    def test_request_field_value_verbose_names(self):
        self.assertEqual(
            self.request_field_value._meta.verbose_name, "Valor de Campo de Solicitud"
        )
        self.assertEqual(
            self.request_field_value._meta.verbose_name_plural,
            "Valores de Campos de Solicitud",
        )

    def test_request_field_value_db_table(self):
        self.assertEqual(
            self.request_field_value._meta.db_table, "operative_requestfieldvalues"
        )

    def test_request_field_value_app_label(self):
        self.assertEqual(self.request_field_value._meta.app_label, "operative")
