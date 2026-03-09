from django.test import TestCase
from modules.base.models import PersonType, DocumentType, Applicant, Taker
from modules.localization.models import Country, State, City
from django.contrib.auth.models import User
from modules.auths.models import Account, Genre, Role


class PersonTypeModelTest(TestCase):
    def setUp(self):
        self.person_type = PersonType.objects.create(id="NAT", name="Natural")

    def test_person_type_creation(self):
        self.assertEqual(self.person_type.id, "NAT")
        self.assertEqual(self.person_type.name, "Natural")

    def test_person_type_str(self):
        self.assertEqual(str(self.person_type), "Natural")

    def test_person_type_ordering(self):
        person_types = PersonType.objects.all()
        self.assertEqual(person_types[0].name, "Natural")

    def test_person_type_verbose_names(self):
        self.assertEqual(self.person_type._meta.verbose_name, "Tipo de Persona")
        self.assertEqual(
            self.person_type._meta.verbose_name_plural, "Tipos de Personas"
        )

    def test_person_type_db_table(self):
        self.assertEqual(self.person_type._meta.db_table, "base_persontypes")

    def test_person_type_app_label(self):
        self.assertEqual(self.person_type._meta.app_label, "base")


class DocumentTypeModelTest(TestCase):
    def setUp(self):
        self.person_type = PersonType.objects.create(id="NAT", name="Natural")
        self.document_type = DocumentType.objects.create(
            id="CC", name="Cédula de Ciudadanía", person_type=self.person_type
        )

    def test_document_type_creation(self):
        self.assertEqual(self.document_type.id, "CC")
        self.assertEqual(self.document_type.name, "Cédula de Ciudadanía")
        self.assertEqual(self.document_type.person_type, self.person_type)

    def test_document_type_str(self):
        self.assertEqual(str(self.document_type), "Cédula de Ciudadanía")

    def test_document_type_ordering(self):
        document_types = DocumentType.objects.all()
        self.assertEqual(document_types[0].name, "Cédula de Ciudadanía")

    def test_document_type_verbose_names(self):
        self.assertEqual(self.document_type._meta.verbose_name, "Tipo de Documento")
        self.assertEqual(
            self.document_type._meta.verbose_name_plural, "Tipos de Documentos"
        )

    def test_document_type_db_table(self):
        self.assertEqual(self.document_type._meta.db_table, "base_documenttypes")

    def test_document_type_app_label(self):
        self.assertEqual(self.document_type._meta.app_label, "base")


class ApplicantModelTest(TestCase):
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
        self.applicant = Applicant.objects.create(
            identification="1234567890",
            name="Juan Pérez",
            email="juan@example.com",
            phone_number="1234567890",
            state=self.state,
            city=self.city,
            created_by="testuser",
        )

    def test_applicant_creation(self):
        self.assertEqual(self.applicant.identification, "1234567890")
        self.assertEqual(self.applicant.name, "Juan Pérez")
        self.assertEqual(self.applicant.email, "juan@example.com")
        self.assertEqual(self.applicant.phone_number, "1234567890")
        self.assertEqual(self.applicant.state, self.state)
        self.assertEqual(self.applicant.city, self.city)
        self.assertEqual(self.applicant.created_by, "testuser")

    def test_applicant_str(self):
        self.assertEqual(str(self.applicant), "Juan Pérez")

    def test_applicant_with_null_state(self):
        applicant = Applicant.objects.create(
            identification="0987654321",
            name="Pedro García",
            email="pedro@example.com",
            phone_number="0987654321",
            state=None,
            city=None,
            created_by="testuser",
        )
        self.assertIsNone(applicant.state)
        self.assertIsNone(applicant.city)

    def test_applicant_ordering(self):
        applicants = Applicant.objects.all()
        self.assertEqual(applicants[0].name, "Juan Pérez")

    def test_applicant_verbose_names(self):
        self.assertEqual(self.applicant._meta.verbose_name, "Solicitante")
        self.assertEqual(self.applicant._meta.verbose_name_plural, "Solicitantes")

    def test_applicant_db_table(self):
        self.assertEqual(self.applicant._meta.db_table, "base_applicants")

    def test_applicant_app_label(self):
        self.assertEqual(self.applicant._meta.app_label, "base")


class TakerModelTest(TestCase):
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
            created_by="testuser",
        )

    def test_taker_creation(self):
        self.assertEqual(self.taker.person_type, self.person_type)
        self.assertEqual(self.taker.document_type, self.document_type)
        self.assertEqual(self.taker.identification, "1234567890")
        self.assertEqual(self.taker.name, "Empresa Test SAS")
        self.assertEqual(self.taker.email, "test@empresa.com")
        self.assertEqual(self.taker.phone_number, "1234567890")
        self.assertEqual(self.taker.contact_name, "Juan Pérez")
        self.assertEqual(self.taker.address, "Calle 123")
        self.assertEqual(self.taker.state, self.state)
        self.assertEqual(self.taker.city, self.city)
        self.assertEqual(self.taker.created_by, "testuser")

    def test_taker_str(self):
        self.assertEqual(str(self.taker), "Empresa Test SAS")

    def test_taker_with_null_fields(self):
        taker = Taker.objects.create(
            person_type=self.person_type,
            document_type=self.document_type,
            identification="0987654321",
            name="Empresa Test 2 SAS",
            email=None,
            phone_number=None,
            contact_name=None,
            address=None,
            state=None,
            city=None,
            created_by="testuser",
        )
        self.assertIsNone(taker.email)
        self.assertIsNone(taker.phone_number)
        self.assertIsNone(taker.contact_name)
        self.assertIsNone(taker.address)
        self.assertIsNone(taker.state)
        self.assertIsNone(taker.city)

    def test_taker_ordering(self):
        takers = Taker.objects.all()
        self.assertEqual(takers[0].name, "Empresa Test SAS")

    def test_taker_verbose_names(self):
        self.assertEqual(self.taker._meta.verbose_name, "Tomador")
        self.assertEqual(self.taker._meta.verbose_name_plural, "Tomadores")

    def test_taker_db_table(self):
        self.assertEqual(self.taker._meta.db_table, "base_takers")

    def test_taker_app_label(self):
        self.assertEqual(self.taker._meta.app_label, "base")
