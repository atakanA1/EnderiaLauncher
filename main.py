import os
import platform
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.behaviors import DragBehavior
from kivy.core.window import Window

# Mobil ekranlarda daha iyi görünüm için arka plan rengini siyah yapalım
Window.clearcolor = (0.05, 0.05, 0.05, 1)

# Sürüklenebilir Buton Sınıfı (Edit Mode için)
class DragButton(DragBehavior, Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag_timeout = 10000000
        self.drag_distance = 0
        self.size_hint = (None, None)
        self.size = (100, 50)
        self.background_color = (0.2, 0.2, 0.2, 0.8)

class NavMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.2, 1)
        self.padding = 5
        self.spacing = 10
        
        btns = [
            ('ANA SAYFA', 'ana', (0.1, 0.4, 0.1, 1)),
            ('GENEL', 'genel', (0.2, 0.2, 0.2, 1)),
            ('KONTROLLER', 'kontrol', (0.2, 0.2, 0.2, 1))
        ]
        
        for text, screen, color in btns:
            btn = Button(text=text, background_color=color, font_size='14sp', bold=True)
            btn.bind(on_press=lambda x, s=screen: self.change_scr(s))
            self.add_widget(btn)

    def change_scr(self, screen_name):
        App.get_running_app().root.current = screen_name

class AnaEkran(Screen):
    def on_enter(self, *args):
        self.clear_widgets()
        layout = FloatLayout()
        layout.add_widget(NavMenu(pos_hint={'x': 0, 'y': 0}))

        # Kullanıcı Adı (Pojav stili sağ üst)
        self.user = TextInput(text='Oyuncu', size_hint=(0.25, 0.07), pos_hint={'x': 0.72, 'y': 0.9}, 
                              background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1,1,1,1), multiline=False)
        layout.add_widget(self.user)

        # Oyna Butonu (Merkezi ve Büyük)
        oyna = Button(text='OYNA', size_hint=(0.4, 0.2), pos_hint={'center_x': 0.6, 'center_y': 0.5},
                      background_color=(0.15, 0.6, 0.2, 1), font_size='24sp', bold=True)
        layout.add_widget(oyna)

        # Sürüm Barı (Alt orta)
        surum = Spinner(text='Sürüm Seçin', values=('1.20.1', '1.16.5', '1.8.9'),
                        size_hint=(0.5, 0.08), pos_hint={'center_x': 0.6, 'y': 0.05})
        layout.add_widget(surum)
        self.add_widget(layout)

class GenelAyarlar(Screen):
    def on_enter(self, *args):
        self.clear_widgets()
        layout = FloatLayout()
        layout.add_widget(NavMenu())

        box = BoxLayout(orientation='vertical', size_hint=(0.7, 0.9), pos_hint={'x': 0.25, 'y': 0.05}, spacing=10)
        box.add_widget(Label(text="GENEL AYARLAR", font_size='20sp', color=(0, 0.6, 1, 1)))

        # RAM
        box.add_widget(Label(text="Hafıza (RAM) Ayarı", size_hint_y=None, height=30))
        ram = Slider(min=1024, max=8192, value=2048, step=512)
        ram_lab = Label(text=f"{int(ram.value)} MB")
        ram.bind(value=lambda s, v: setattr(ram_lab, 'text', f"{int(v)} MB"))
        box.add_widget(ram); box.add_widget(ram_lab)

        # Çözünürlük
        box.add_widget(Label(text="Ölçeklendirme (%)", size_hint_y=None, height=30))
        box.add_widget(Slider(min=50, max=100, value=100))

        # Dosya Yolu
        box.add_widget(Label(text="Oyun Dizini", size_hint_y=None, height=30))
        path_row = BoxLayout(size_hint_y=None, height=45, spacing=5)
        path_row.add_widget(TextInput(text="/sdcard/EnderiaMC", multiline=False))
        path_row.add_widget(Button(text="GÖZAT", size_hint_x=0.3))
        box.add_widget(path_row)

        layout.add_widget(box)
        self.add_widget(layout)

class KontrolAyarlar(Screen):
    def on_enter(self, *args):
        self.clear_widgets()
        self.layout = FloatLayout()
        self.layout.add_widget(NavMenu())

        # Edit Mode Bilgisi
        self.info = Label(text="Düzenlemek için butonları sürükleyin", size_hint=(0.7, 0.1), pos_hint={'x': 0.25, 'y': 0.9})
        self.layout.add_widget(self.info)

        # Pojav Tarzı Sürüklenebilir Butonlar
        # Bunlar oyun içinde ekranda nerede duracaklarını belirler
        tuslar = [
            ('W', 0.4, 0.3), ('A', 0.3, 0.2), ('S', 0.4, 0.1), ('D', 0.5, 0.2),
            ('VUR', 0.8, 0.2), ('BLOK', 0.8, 0.4), ('INV', 0.1, 0.8), ('CHAT', 0.2, 0.8)
        ]

        for isim, px, py in tuslar:
            btn = DragButton(text=isim, pos_hint={'x': px, 'y': py})
            # drag_rect_xxx özellikleri butonun her yerinden tutulmasını sağlar
            btn.drag_rect_x = btn.x
            btn.drag_rect_y = btn.y
            btn.drag_rect_width = Window.width
            btn.drag_rect_height = Window.height
            self.layout.add_widget(btn)

        self.add_widget(self.layout)

class PojavStyleLauncher(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AnaEkran(name='ana'))
        sm.add_widget(GenelAyarlar(name='genel'))
        sm.add_widget(KontrolAyarlar(name='kontrol'))
        return sm

if __name__ == '__main__':
    PojavStyleLauncher().run()