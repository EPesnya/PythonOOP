# Песня Евгений

class Citizen:
    def __init__(self, name, surname, age, nationality, registration):
        self._name = name
        self._surname = surname
        self._age = age
        self._nationality = nationality
        self._registration = registration
        
    def get_name(self):
        return self._name

    def set_name(self, x):
        self._name = x

    def get_surname(self):
        return self._surname

    def set_surname(self, x):
        self._surname = x

    def get_age(self):
        return self._age

    def set_age(self, x):
        self._age = x

    def get_nationality(self):
        return self._nationality

    def set_nationality(self, x):
        self._nationality = x

    def get_registration(self):
        return self._registration

    def set_registration(self, x):
        self._registration = x

class Worker(Citizen):
    def __init__(self, name, surname, age, nationality, registration,
                 company_name, company_address, company_phone):
        Citizen.__init__(self, name, surname, age, nationality, registration)
        self._company_name = company_name
        self._company_address = company_address
        self._company_phone = company_phone

    def get_company_name(self):
        return self._company_name

    def set_company_name(self, x):
        self._company_name = x

    def get_company_address(self):
        return self._company_address

    def set_company_address(self, x):
        self._company_address = x

    def get_company_phone(self):
        return self._company_phone

    def set_company_phone(self, x):
        self._company_phone = x
    

class Scientist(Worker):
    def __init__(self, name, surname, age, nationality, registration,
                 sphere, type, publications_number):
        Citizen.__init__(self, name, surname, age, nationality, registration)
        # Ученый может и не быть сотрудником какой-то компании, поэтому при создании
        # объекта ученый, можно не указывать данные компании
        self._company_name = None
        self._company_address = None
        self._company_phone = None
        self._sphere = sphere
        self._type = type
        self._publications_number = publications_number

    def get_sphere(self):
        return self._sphere

    def set_sphere(self, x):
        self._sphere = x

    def get_type(self):
        return self._type

    def set_type(self, x):
        self._type = x

    def get_publications_number(self):
        return self._publications_number

    def set_publications_number(self, x):
        self._publications_number = x

class Master(Scientist):
    pass

class PrePhD(Scientist):
    pass

class PhD(Scientist):
    pass


def print_scientist(a):
    print("""Name: {}
Surname: {}
Age: {}
Nationality: {}
Registration: {}
Company name: {}
Company address: {}
Company phone: {}
Scientific field: {}
Type of scientist: {}
Number of publications: {}""".format(
        a.get_name(),
        a.get_surname(),
        a.get_age(),
        a.get_nationality(),
        a.get_registration(),
        a.get_company_name(),
        a.get_company_address(),
        a.get_company_phone(),
        a.get_sphere(),
        a.get_type(),
        a.get_publications_number()))



a = Master("Andrey", "Smirnov", 40, "RUS", "Dolgoprudniy, Pervomayskaya str. 43",
    "Chemistry", "Experimenter", 120)
print_scientist(a)


a.set_name("Oleg")
a.set_age(20)
a.set_publications_number(40)
a.set_company_name("Google")
a.set_company_phone("+7 322 228 322")
a.set_company_address("Moskow")
print()
print_scientist(a)
