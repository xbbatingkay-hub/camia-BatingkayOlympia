from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window


# --- Generator Object ---
class Generator:
    def __init__(self, name, base_cost, gps):
        self.name = name
        self.base_cost = base_cost
        self.gps = gps  # output per generator
        self.count = 0

    def cost(self):
        """Exponential scaling: each purchase gets more expensive"""
        return int(self.base_cost * (1.15 ** self.count))

    def total_gps(self):
        return self.count * self.gps


# --- Game State Manager ---
class GameManager:
    def __init__(self):
        self.g = 0
        self.click_g = 1
        self.level = 1
        self.current_exp = 0
        self.next_level_exp = 100
        self.tax_rate = 0.1  # 10% tax on passive income

        # Define generator types
        self.generators = [
            Generator("Base Generator", base_cost=10, gps=0.1),
            Generator("Better Generator", base_cost=100, gps=1),
            Generator("Industrial Generator", base_cost=1000, gps=10),
        ]

    def click(self):
        self.g += self.click_g
        self.gain_exp(self.click_g)

    def buy_generator(self, gen_index):
        gen = self.generators[gen_index]
        cost = gen.cost()
        if self.g >= cost:
            self.g -= cost
            gen.count += 1

    def tick(self, dt):
        """Auto tick every second"""
        total_gained = 0
        for gen in self.generators:
            total_gained += gen.total_gps()
        if total_gained > 0:
            taxed = total_gained * (1 - self.tax_rate)
            self.g += taxed
            self.gain_exp(taxed)

    def gain_exp(self, amount):
        self.current_exp += amount
        if self.current_exp >= self.next_level_exp:
            self.current_exp -= self.next_level_exp
            self.level += 1
            self.next_level_exp = self.level * 100
    
    def total_gps(self):
        return sum(gen.total_gps() for gen in self.generators) * (1 - self.tax_rate)


# --- Screens ---
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source="splash.png"))

    def on_enter(self):
        # Auto switch to main after 2 seconds
        Clock.schedule_once(lambda dt: self.manager.switch_to(self.manager.get_screen("main")), 2)


class MainScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        from kivy.uix.anchorlayout import AnchorLayout
        title_box = AnchorLayout(anchor_x="center", anchor_y="center", size_hint=(1, 10))
        self.title_label = Label(text = "The Game Made to Destroy Boredom: The Game\n                      MOBILE EDITION")
        title_box.add_widget(self.title_label)
        layout.add_widget(title_box)
        # Wrap G + GPS in a vertical box
        stats_box = BoxLayout(orientation="vertical", spacing=2, size_hint=(None, None), height=80)
        self.g_label = Label(text=f"{self.game.g:.1f}G", font_size=40)
        self.gps_label = Label(text=f"{self.game.total_gps():.1f} G/s", font_size=20)
        stats_box.add_widget(self.g_label)
        stats_box.add_widget(self.gps_label)

        # Anchor that box at the top-center
        stats_anchor = AnchorLayout(anchor_x="center", anchor_y="center", size_hint=(1, 50))
        stats_anchor.add_widget(stats_box)

        # Add to main layout first, so it's at the top
        layout.add_widget(stats_anchor)

        # --- Stats (moved from StatsScreen) ---
        self.level_label = Label(text=f"Level: {self.game.level}", font_size=20)
        layout.add_widget(self.level_label)

        self.exp_bar = ProgressBar(max=self.game.next_level_exp, value=self.game.current_exp, size_hint=(1, None), height=30)
        layout.add_widget(self.exp_bar)

        # Click button
        click_btn = Button(text="Increase G", size_hint=(0.3, None))
        click_btn.bind(on_press=self.on_click)
        layout.add_widget(click_btn)

        # Navigation buttons
        layout.add_widget(Button(
        text="Go to Shop",
        size_hint=(None, None),  # disables auto-stretching
        size=(150, 50),          # width x height
        on_press=lambda w: self.manager.switch_to(self.manager.get_screen("shop"))
        ))

        layout.add_widget(Button(
            text="Go to Stats",
            size_hint=(None, None),
            size=(150, 50),
            on_press=lambda w: self.manager.switch_to(self.manager.get_screen("stats"))
        ))

        self.add_widget(layout)

        # Update display every 0.5 sec
        Clock.schedule_interval(self.update, 0.5)

    def on_click(self, instance):
        self.game.click()

    def update(self, dt):
        self.g_label.text = f"{self.game.g:.1f}G"


class ShopScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Dynamic generator buttons
        self.labels = []
        for i, gen in enumerate(self.game.generators):
            label = Label(text=f"{gen.name}: {gen.count} | Cost: {gen.cost()}G | Output: {gen.gps}/s each")
            buy_btn = Button(text=f"Buy {gen.name}", size_hint=(0.3, None))
            buy_btn.bind(on_press=lambda w, i=i: self.game.buy_generator(i))
            self.layout.add_widget(label)
            self.layout.add_widget(buy_btn)
            self.labels.append(label)

        back_btn = Button(text="Back", on_press=lambda w: self.manager.switch_to(self.manager.get_screen("main")))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        for i, gen in enumerate(self.game.generators):
            self.labels[i].text = f"{gen.name}: {gen.count} | Cost: {gen.cost()}G | Output: {gen.gps}/s each"


class StatsScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.level_label = Label(text=f"Level: {self.game.level}")
        layout.add_widget(self.level_label)

        self.exp_bar = ProgressBar(max=self.game.next_level_exp, value=self.game.current_exp)
        layout.add_widget(self.exp_bar)

        back_btn = Button(text="Back", on_press=lambda w: self.manager.switch_to(self.manager.get_screen("main")))
        layout.add_widget(back_btn)

        self.add_widget(layout)
        Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        self.level_label.text = f"Level: {self.game.level}"
        self.exp_bar.max = self.game.next_level_exp
        self.exp_bar.value = self.game.current_exp


# --- Main App ---
class TycoonApp(App):
    def build(self):
        self.game = GameManager()
        Window.icon = "icon.png"  # Desktop app icon
        Window.size = (480, 800)  # Optional default window size

        # Auto-generator tick every second
        Clock.schedule_interval(self.game.tick, 1.0)

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(self.game, name="main"))
        sm.add_widget(ShopScreen(self.game, name="shop"))
        sm.add_widget(StatsScreen(self.game, name="stats"))
        sm.current = "splash"
        return sm


if __name__ == "__main__":
    TycoonApp().run()
