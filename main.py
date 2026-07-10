import os
import threading
from kivy.utils import platform
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.image import Image

# Import Custom API Module
import gemini_api

Window.softinput_mode = 'below_target'

class HomeScreen(Screen): pass
class ChatScreen(Screen): pass

class KaboxApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attached_images = []
        self.system_instruction = (
            "Tum AI KABOX ho, ek expert agricultural assistant. "
            "Jawab Hinglish me do. 1. Fasal ki bimari batao. "
            "2. Solution do. 3. Current Mandi bhav ka andaza do."
        )
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        screen_manager = Builder.load_file("kabox_ui.kv")
        
        Clock.schedule_once(lambda dt: self.add_message(
            "Namaste Kisaan Bhai! 🙏 AI KABOX me aapka swagat hai. Batayein fasal ki kya janch karni hai?", 
            is_user=False
        ), 0.5)
        return screen_manager

    def go_back_home(self):
        self.root.current = 'home'

    # --- FILE MANAGER LOGIC ---
    def open_file_manager(self):
        # PC par home directory, Android par storage khulega
        path = os.path.expanduser("~") if platform != "android" else "/storage/emulated/0/"
        self.file_manager.show(path)

    def select_path(self, path):
        self.exit_manager()
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            if len(self.attached_images) < 3:
                self.attached_images.append(path)
                self.update_attachment_ui()

    def exit_manager(self, *args):
        self.file_manager.close()

    # --- ATTACHMENT UI ---
    def update_attachment_ui(self):
        bar = self.root.get_screen('chat').ids.attachment_bar
        bar.clear_widgets()
        if not self.attached_images:
            bar.height = 0
            return
        
        bar.height = dp(90)
        for index, img_path in enumerate(self.attached_images):
            card = MDCard(size_hint=(None, None), size=(dp(75), dp(75)), radius=[12])
            layout = MDBoxLayout()
            thumb = Image(source=img_path, allow_stretch=True, keep_ratio=False)
            
            del_btn = MDIconButton(
                icon="close-circle",
                pos_hint={"top": 1, "right": 1},
                text_color=[1, 0, 0, 1],
                theme_text_color="Custom",
                on_release=lambda x, i=index: self.remove_attachment(i)
            )
            layout.add_widget(thumb)
            layout.add_widget(del_btn)
            card.add_widget(layout)
            bar.add_widget(card)

    def remove_attachment(self, index):
        if 0 <= index < len(self.attached_images):
            self.attached_images.pop(index)
            self.update_attachment_ui()

    # --- CHAT ENGINE ---
    def add_message(self, text, is_user):
        text = text.replace("**", "").replace("*", "•")
        container = self.root.get_screen('chat').ids.chat_container
        row = MDBoxLayout(orientation="horizontal", size_hint_y=None, adaptive_height=True, padding=[dp(10), dp(5)])
        
        card = MDCard(
            radius=[16, 16, 16, 0] if is_user else [16, 16, 0, 16],
            md_bg_color=[0.41, 0.14, 0.62, 1] if is_user else [1, 1, 1, 1],
            size_hint_x=0.8, size_hint_y=None, adaptive_height=True, padding=dp(15)
        )
        
        lbl = MDLabel(
            text=text, theme_text_color="Custom",
            text_color=[1, 1, 1, 1] if is_user else [0, 0, 0, 1],
            size_hint_y=None, adaptive_height=True
        )
        card.add_widget(lbl)
        
        if is_user:
            row.add_widget(MDBoxLayout(size_hint_x=0.2))
            row.add_widget(card)
        else:
            row.add_widget(card)
            row.add_widget(MDBoxLayout(size_hint_x=0.2))
            
        container.add_widget(row)
        Clock.schedule_once(lambda dt: setattr(self.root.get_screen('chat').ids.chat_scroll, 'scroll_y', 0), 0.1)

    def send_chat(self):
        chat_input = self.root.get_screen('chat').ids.chat_input
        text = chat_input.text.strip()
        
        if not text and not self.attached_images:
            return
            
        self.add_message(text if text else "📸 Images Attached", is_user=True)
        chat_input.text = ""
        self.root.get_screen('chat').ids.chat_spinner.active = True
        
        # Async threading to prevent UI freeze
        threading.Thread(
            target=self.process_gemini,
            args=(text, self.attached_images.copy()),
            daemon=True
        ).start()
        
        self.attached_images.clear()
        self.update_attachment_ui()

    def process_gemini(self, prompt, images):
        # API call separated into gemini_api.py
        reply = gemini_api.get_gemini_response(prompt, images, self.system_instruction)
        Clock.schedule_once(lambda dt: self.on_api_success(reply), 0)

    def on_api_success(self, reply):
        self.root.get_screen('chat').ids.chat_spinner.active = False
        self.add_message(reply, is_user=False)


if __name__ == '__main__':
    KaboxApp().run()
      
