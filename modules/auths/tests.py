from django.test import TestCase
from django.contrib.auth.models import User
from modules.auths.models import Genre, Role, RoleEnum, Account, Token
from modules.localization.models import Country, State, City


class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(id="M", name="Masculino")

    def test_genre_creation(self):
        self.assertEqual(self.genre.id, "M")
        self.assertEqual(self.genre.name, "Masculino")

    def test_genre_str(self):
        self.assertEqual(str(self.genre), "Masculino")

    def test_genre_ordering(self):
        genres = Genre.objects.all()
        self.assertEqual(genres[0].name, "Masculino")

    def test_genre_verbose_names(self):
        self.assertEqual(self.genre._meta.verbose_name, "Género")
        self.assertEqual(self.genre._meta.verbose_name_plural, "Géneros")

    def test_genre_db_table(self):
        self.assertEqual(self.genre._meta.db_table, "auths_genres")

    def test_genre_app_label(self):
        self.assertEqual(self.genre._meta.app_label, "auths")


class RoleModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(id="admin", name="Administrador")

    def test_role_creation(self):
        self.assertEqual(self.role.id, "admin")
        self.assertEqual(self.role.name, "Administrador")

    def test_role_str(self):
        self.assertEqual(str(self.role), "Administrador")

    def test_role_ordering(self):
        roles = Role.objects.all()
        self.assertEqual(roles[0].name, "Administrador")

    def test_role_verbose_names(self):
        self.assertEqual(self.role._meta.verbose_name, "Rol")
        self.assertEqual(self.role._meta.verbose_name_plural, "Roles")

    def test_role_db_table(self):
        self.assertEqual(self.role._meta.db_table, "auths_roles")

    def test_role_app_label(self):
        self.assertEqual(self.role._meta.app_label, "auths")


class RoleEnumTest(TestCase):
    def test_role_enum_values(self):
        self.assertEqual(RoleEnum.ADMIN, "admin")
        self.assertEqual(RoleEnum.ASSISTANT, "assitant")
        self.assertEqual(RoleEnum.APPLICANT, "applicant")

    def test_role_enum_is_strenum(self):
        self.assertEqual(str(RoleEnum.ADMIN), "admin")
        self.assertEqual(str(RoleEnum.ASSISTANT), "assitant")
        self.assertEqual(str(RoleEnum.APPLICANT), "applicant")


class AccountModelTest(TestCase):
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
        self.genre = Genre.objects.create(id="M", name="Masculino")
        self.role = Role.objects.create(id="admin", name="Administrador")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        self.account = Account.objects.create(
            user=self.user,
            genre=self.genre,
            role=self.role,
            address="Calle 123",
            phone="1234567890",
            whatsapp="1234567890",
            state=self.state,
            city=self.city,
            created_by="testuser",
        )

    def test_account_creation(self):
        self.assertEqual(self.account.user, self.user)
        self.assertEqual(self.account.genre, self.genre)
        self.assertEqual(self.account.role, self.role)
        self.assertEqual(self.account.address, "Calle 123")
        self.assertEqual(self.account.phone, "1234567890")
        self.assertEqual(self.account.whatsapp, "1234567890")
        self.assertEqual(self.account.state, self.state)
        self.assertEqual(self.account.city, self.city)
        self.assertEqual(self.account.created_by, "testuser")

    def test_account_str(self):
        self.assertEqual(str(self.account), "testuser")

    def test_account_username_property(self):
        self.assertEqual(self.account.username, "testuser")

    def test_account_complete_name_property(self):
        self.assertEqual(self.account.complete_name, "Test User")

    def test_account_first_name_property(self):
        self.assertEqual(self.account.first_name, "Test")

    def test_account_last_name_property(self):
        self.assertEqual(self.account.last_name, "User")

    def test_account_is_active_property(self):
        self.assertTrue(self.account.is_active)

    def test_account_set_password(self):
        self.account.set_password("newpass123")
        self.assertTrue(self.user.check_password("newpass123"))

    def test_account_check_password(self):
        self.assertTrue(self.account.check_password("testpass123"))
        self.assertFalse(self.account.check_password("wrongpass"))

    def test_account_get_account_with_username(self):
        account = Account.getAccount("testuser")
        self.assertEqual(account, self.account)

    def test_account_get_account_with_user(self):
        account = Account.getAccount(self.user)
        self.assertEqual(account, self.account)

    def test_account_get_account_with_nonexistent(self):
        account = Account.getAccount("nonexistent")
        self.assertIsNone(account)

    def test_account_verbose_names(self):
        self.assertEqual(self.account._meta.verbose_name, "Cuenta")
        self.assertEqual(self.account._meta.verbose_name_plural, "Cuentas")

    def test_account_db_table(self):
        self.assertEqual(self.account._meta.db_table, "auths_accounts")

    def test_account_app_label(self):
        self.assertEqual(self.account._meta.app_label, "auths")


class TokenModelTest(TestCase):
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
        self.genre = Genre.objects.create(id="M", name="Masculino")
        self.role = Role.objects.create(id="admin", name="Administrador")
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.account = Account.objects.create(
            user=self.user, genre=self.genre, role=self.role, created_by="testuser"
        )

    def test_token_str(self):
        token = Token.generate(self.account, 1)
        token_obj = Token.objects.get(token=token)
        self.assertEqual(str(token_obj), token)

    def test_token_generate(self):
        token = Token.generate(self.account, 1)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)

    def test_token_generate_with_max_times(self):
        token = Token.generate(self.account, 5)
        token_obj = Token.objects.get(token=token)
        self.assertEqual(token_obj.max_times, 5)
        self.assertEqual(token_obj.times, 0)

    def test_token_decode_valid(self):
        token = Token.generate(self.account, 1)
        account, is_expired = Token.decode(token, delete=False)
        self.assertFalse(is_expired)
        self.assertEqual(account, self.account)

    def test_token_decode_with_delete(self):
        token = Token.generate(self.account, 1)
        account, is_expired = Token.decode(token, delete=True)
        self.assertFalse(is_expired)
        self.assertEqual(account, self.account)
        self.assertFalse(Token.objects.filter(token=token).exists())

    def test_token_decode_invalid_token(self):
        account, is_expired = Token.decode("invalid_token", delete=False)
        self.assertTrue(is_expired)
        self.assertIsNone(account)

    def test_token_verbose_names(self):
        token = Token.generate(self.account, 1)
        token_obj = Token.objects.get(token=token)
        self.assertEqual(token_obj._meta.verbose_name, "Token")
        self.assertEqual(token_obj._meta.verbose_name_plural, "Tokens")

    def test_token_db_table(self):
        token = Token.generate(self.account, 1)
        token_obj = Token.objects.get(token=token)
        self.assertEqual(token_obj._meta.db_table, "auths_tokens")

    def test_token_app_label(self):
        token = Token.generate(self.account, 1)
        token_obj = Token.objects.get(token=token)
        self.assertEqual(token_obj._meta.app_label, "auths")
