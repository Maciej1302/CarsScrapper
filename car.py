# Car attributes (some might not be provided by the advertiser)
    # Oferta od
    # Pokaż oferty z numerem VIN
    # Model pojazdu
    # Generacja
    # Rok produkcji
    # Przebieg
    # Pojemność skokowa
    # Rodzaj paliwa
    # Moc
    # VIN
    # Skrzynia biegów
    # Spalanie W Mieście
    # Typ nadwozia
    # Liczba drzwi
    # Kolor
    # Zarejestrowany w Polsce
    # Stan

class Car:
    def __init__(self, car_attributes):

        if not car_attributes:
            raise ValueError("car_attributes cannot be None")
        self.car_attributes = car_attributes

    def get_attribute(self, key):
        return self.car_attributes.get(key)

    def __eq__(self, other):
        if not isinstance(other, Car):
            return NotImplemented
        return self.car_attributes['Url'] == other.car_attributes['Url']

    def __hash__(self):
        return hash(self.car_attributes['Url'])

