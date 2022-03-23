import threading
import time

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import psycopg2

Builder.load_file('KivyBox.kv')


class myThread(threading.Thread):

    def __init__(self, progress_bar):
        threading.Thread.__init__(self)
        self.progress_bar = progress_bar

    def run(self):
        while self.progress_bar.value < 100:
            self.progress_bar.value += 1
            print(self.progress_bar.value)
            time.sleep(1 / 15)


class MyGrid(Widget):
    progress_bar = ObjectProperty()
    airline = ObjectProperty(None)
    customer = ObjectProperty(None)
    admin = ObjectProperty(None)
    flights = ObjectProperty(None)
    tickets = ObjectProperty(None)
    countries = ObjectProperty(None)

    def __init__(self, **kwa):
        super(MyGrid, self).__init__(**kwa)
        self.progress_bar = ProgressBar()
        self.popup = Popup(title='Importing', content=self.progress_bar)
        self.popup.bind(on_open=self.puopen)

    def press(self):
        airline = self.airline.text
        customer = self.customer.text
        admin = self.admin.text
        flights = self.flights.text
        tickets = self.tickets.text
        countries = self.countries.text
        print(f'You just added {airline} airlines ,{customer}-customers,'
              f'{admin}-admins,{flights}-flights, {tickets}-tickets, {countries}-countries ')
        self.airline.text = ''
        self.customer.text = ''
        self.admin.text = ''
        self.flights.text = ''
        self.tickets.text = ''
        self.countries.text = ''
        self.progress_bar.value = 1
        self.popup.open()

        conn = psycopg2.connect(
            host="localhost",
            database="test_kivy",
            user="postgres",
            password="admin",
            port="5431",
        )
        c = conn.cursor()

        c.execute("""CREATE TABLE if not exists CUSTOMER 
        (name TEXT);
        """)

        conn.commit()
        conn.close()

    def next(self, dt):
        if self.progress_bar.value >= 100:
            return False
        self.progress_bar.value += 1

    def puopen(self, instance):
        t1 = myThread(self.progress_bar)
        t1.start()


class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()
