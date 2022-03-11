import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('KivyBox.kv')


class MyGrid(Widget):
    airline = ObjectProperty(None)
    customer = ObjectProperty(None)
    admin = ObjectProperty(None)
    flights = ObjectProperty(None)
    tickets = ObjectProperty(None)
    countries = ObjectProperty(None)

    def press(self):
        airline = self.airline.text
        customer = self.customer.text
        admin = self.admin.text
        flights = self.flights.text
        tickets = self.tickets.text
        countries = self.countries.text
        print(f'hey you just add {airline}-airline,{customer}-customer,'
              f'{admin}-admin,{flights}-flights, {tickets}-tickets, {countries}-countries ')
        self.airline.text = ''
        self.customer.text = ''
        self.admin.text = ''
        self.flights.text = ''
        self.tickets.text = ''
        self.countries.text = ''


class AwsomApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    AwsomApp().run()
