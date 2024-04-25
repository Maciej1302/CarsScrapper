from bs4 import BeautifulSoup
import requests
from car import Car
import webbrowser


def scrap_page(url: str) -> str:
    page = requests.get(url)
    return page.text


def scrap_cars_links(url: str) -> list[str]:
    soup = BeautifulSoup(scrap_page(url), "html.parser")
    href_links = soup.find_all("a", href=True, string="ad link")
    direct_links = [link["href"] for link in href_links]
    return direct_links


def find_how_many_pages(url: str) -> int:
    soup = BeautifulSoup(scrap_page(url), "html.parser")
    pages_amount = soup.find_all(class_="ooa-g4wbjr eezyyk50")
    print(pages_amount)
    return int(pages_amount[-1].text)


def get_car_attributes(url: str) -> dict[str] | None:
    car_attributes = {}
    soup = BeautifulSoup(scrap_page(url), "html.parser")
    containers = soup.find_all("div", class_="ooa-162vy3d e18eslyg3")
    try:
        for i in containers:
            if i.find(class_="e16lfxpc0 ooa-1pe3502 er34gjf0") is not None:
                car_attributes[i.find(class_="e18eslyg4 ooa-12b2ph5").text] = i.find(
                    class_="e16lfxpc0 ooa-1pe3502 er34gjf0"
                ).text
            else:
                car_attributes[i.find(class_="e18eslyg4 ooa-12b2ph5").text] = i.find(
                    class_="e16lfxpc1 ooa-1ftbcn2"
                ).text
    except AttributeError:
        pass

    car_attributes["Cena"] = int(
        soup.find(
            "h3", class_="offer-price__number eqdspoq4 ooa-o7wv9s er34gjf0"
        ).text.replace(" ", "")
    )
    car_attributes["Nazwa aukcji"] = soup.find(
        "h3", class_="offer-title big-text ezl3qpx2 ooa-ebtemw er34gjf0"
    ).text
    car_attributes["Url"] = url
    return car_attributes


def create_cars(url: str) -> list[Car]:
    cars = []
    car_links = scrap_cars_links(url)
    for link in car_links:
        if get_car_attributes(link):
            car = Car(get_car_attributes(link))
            cars.append(car)
    return cars


def scrapper(url: str) -> list[Car]:
    all_cars = []
    for i in range(1):  # <- find_how_many_pages(url: str) -> int:
        all_cars.extend(create_cars(url))
        print("Scrapped pages: "+i)
        url = url + "&page=" + str(i)
    return list(set(all_cars))  # removing duplicated cars


def open_advertisement(
    cars: list[Car], price: int, milage: int, fuel: str
):  # can add all of the car attributes like hp, transmission etc.
    for car in cars:
        if (
            car.get_attribute("Cena") <= price
            and int(car.get_attribute("Przebieg").replace(" ", "").strip("km"))
            <= milage
            and car.get_attribute("Rodzaj paliwa") == fuel
        ):
            webbrowser.open(car.get_attribute("Url"))


url = "https://www.otomoto.pl/osobowe/bmw/seria-3/seg-cabrio/od-2010?search%5Bfilter_enum_generation%5D=gen-e90-2005-2012"
cars = scrapper(url)
open_advertisement(cars, 80000, 150000, "Benzyna")

