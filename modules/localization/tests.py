from django.test import TestCase
from modules.localization.models import Country, State, City


class CountryModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            id="CO", name="Colombia", capital_code="BO"
        )

    def test_country_creation(self):
        self.assertEqual(self.country.id, "CO")
        self.assertEqual(self.country.name, "Colombia")
        self.assertEqual(self.country.capital_code, "BO")

    def test_country_str(self):
        self.assertEqual(str(self.country), "Colombia")

    def test_country_ordering(self):
        countries = Country.objects.all()
        self.assertEqual(countries[0].name, "Colombia")

    def test_country_verbose_names(self):
        self.assertEqual(self.country._meta.verbose_name, "País")
        self.assertEqual(self.country._meta.verbose_name_plural, "Países")

    def test_country_db_table(self):
        self.assertEqual(self.country._meta.db_table, "localization_countries")


class StateModelTest(TestCase):
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

    def test_state_creation(self):
        self.assertEqual(self.state.code, "DC")
        self.assertEqual(self.state.short, "DC")
        self.assertEqual(self.state.name, "Distrito Capital")
        self.assertEqual(self.state.capital_code, "01")
        self.assertEqual(self.state.country, self.country)

    def test_state_str(self):
        self.assertEqual(str(self.state), "Distrito Capital")

    def test_state_ordering(self):
        states = State.objects.all()
        self.assertEqual(states[0].name, "Distrito Capital")

    def test_state_verbose_names(self):
        self.assertEqual(self.state._meta.verbose_name, "Departamento")
        self.assertEqual(self.state._meta.verbose_name_plural, "Departamentos")

    def test_state_db_table(self):
        self.assertEqual(self.state._meta.db_table, "localization_states")

    def test_state_unique_together(self):
        unique_together = self.state._meta.unique_together
        self.assertIn(("country", "code"), unique_together)


class CityModelTest(TestCase):
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

    def test_city_creation(self):
        self.assertEqual(self.city.code, "01")
        self.assertEqual(self.city.name, "Bogotá")
        self.assertEqual(self.city.country, self.country)
        self.assertEqual(self.city.state, self.state)

    def test_city_str(self):
        self.assertEqual(str(self.city), "Bogotá")

    def test_city_with_null_state(self):
        city = City.objects.create(
            country=self.country, state=None, code="02", name="Ciudad Sin Estado"
        )
        self.assertIsNone(city.state)

    def test_city_ordering(self):
        cities = City.objects.all()
        self.assertEqual(cities[0].name, "Bogotá")

    def test_city_verbose_names(self):
        self.assertEqual(self.city._meta.verbose_name, "Ciudad")
        self.assertEqual(self.city._meta.verbose_name_plural, "Ciudades")

    def test_city_db_table(self):
        self.assertEqual(self.city._meta.db_table, "localization_cities")

    def test_city_unique_together(self):
        unique_together = self.city._meta.unique_together
        self.assertIn(("country", "code"), unique_together)
