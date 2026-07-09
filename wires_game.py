"""
Wires - An Android Game
A puzzle game about untangling colored wires.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Line, Color, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager, FadeTransition

import random
import math
from collections import defaultdict

# Set window size for mobile
Window.size = (540, 960)

class Point:
    """A 2D point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Wire:
    """Represents a wire in the game"""
    def __init__(self, wire_id, color, length, num_segments=20):
        self.wire_id = wire_id
        self.color = color
        self.length = length
        self.num_segments = num_segments
        self.points = []
        self.original_points = []
        self.is_being_dragged = False
        self.drag_index = None
        self.untangled = False
        
    def initialize_points(self, start_x, start_y):
        """Create the initial wire points"""
        self.points = []
        segment_length = self.length / self.num_segments
        
        current_x = start_x
        current_y = start_y
        
        for i in range(self.num_segments + 1):
            # Add some random curves to the wire
            noise_x = random.uniform(-10, 10)
            noise_y = random.uniform(-10, 10)
            
            x = current_x + noise_x
            y = current_y + noise_y
            
            self.points.append(Point(x, y))
            
            # Move along the wire length
            current_y += segment_length
        
        self.original_points = [Point(p.x, p.y) for p in self.points]
    
    def apply_tangles(self, other_wires, intensity=1.0):
        """Tangle this wire with others"""
        for other_wire in other_wires:
            if other_wire.wire_id <= self.wire_id:
                continue
            
            # Create intersection points
            for i, point in enumerate(self.points):
                for j, other_point in enumerate(other_wire.points):
                    distance = point.distance_to(other_point)
                    if distance < 30 * intensity:
                        # Push points apart slightly to create visible tangles
                        dx = point.x - other_point.x
                        dy = point.y - other_point.y
                        
                        if distance > 0:
                            angle = math.atan2(dy, dx)
                            push_distance = (30 * intensity - distance) * 0.5
                            
                            self.points[i].x += math.cos(angle) * push_distance
                            self.points[i].y += math.sin(angle) * push_distance
                            
                            other_wire.points[j].x -= math.cos(angle) * push_distance
                            other_wire.points[j].y -= math.sin(angle) * push_distance
    
    def start_drag(self, touch_x, touch_y):
        """Start dragging the wire"""
        min_distance = float('inf')
        closest_index = None
        
        for i, point in enumerate(self.points):
            distance = math.sqrt((point.x - touch_x)**2 + (point.y - touch_y)**2)
            if distance < min_distance and distance < 40:
                min_distance = distance
                closest_index = i
        
        if closest_index is not None:
            self.is_being_dragged = True
            self.drag_index = closest_index
            return True
        
        return False
    
    def drag(self, touch_x, touch_y):
        """Update wire position while dragging"""
        if self.is_being_dragged and self.drag_index is not None:
            dx = touch_x - self.points[self.drag_index].x
            dy = touch_y - self.points[self.drag_index].y
            
            # Drag this point and nearby points
            for i, point in enumerate(self.points):
                distance_to_drag = abs(i - self.drag_index)
                influence = max(0, 1 - (distance_to_drag / 5.0))
                
                point.x += dx * influence * 0.8
                point.y += dy * influence * 0.8
    
    def end_drag(self):
        """Stop dragging the wire"""
        self.is_being_dragged = False
        self.drag_index = None
    
    def check_untangled(self, all_wires, threshold=100):
        """Check if this wire is relatively untangled"""
        total_distance = 0
        for i, point in enumerate(self.points):
            original = self.original_points[i]
            distance = point.distance_to(original)
            total_distance += distance
        
        # Check if tangled with other wires
        tangled_count = 0
        for other_wire in all_wires:
            if other_wire.wire_id == self.wire_id:
                continue
            
            for i in range(len(self.points)):
                for j in range(len(other_wire.points)):
                    distance = self.points[i].distance_to(other_wire.points[j])
                    if distance < 25:
                        tangled_count += 1
        
        # Wire is untangled if it doesn't cross much with others
        self.untangled = tangled_count < 5
        return self.untangled


class WireGameWidget(Widget):
    """The main game widget for rendering and logic"""
    
    def __init__(self, level=1, **kwargs):
        super().__init__(**kwargs)
        self.level = level
        self.wires = []
        self.all_untangled = False
        self.level_complete = False
        
        # Difficulty scaling
        difficulty_params = self.get_difficulty_params(level)
        self.num_wires = difficulty_params['num_wires']
        self.tangle_intensity = difficulty_params['tangle_intensity']
        self.wire_length_min = difficulty_params['wire_length_min']
        self.wire_length_max = difficulty_params['wire_length_max']
        
        # Colors for wires
        self.wire_colors = [
            (1, 0, 0, 1),      # Red
            (0, 1, 0, 1),      # Green
            (0, 0, 1, 1),      # Blue
            (1, 1, 0, 1),      # Yellow
            (1, 0, 1, 1),      # Magenta
            (0, 1, 1, 1),      # Cyan
            (1, 0.5, 0, 1),    # Orange
            (0.5, 0, 1, 1),    # Purple
        ]
        
        self.initialize_level()
        self.bind(size=self.on_size)
        Clock.schedule_interval(self.update, 1/60.0)  # 60 FPS
    
    def get_difficulty_params(self, level):
        """Get difficulty parameters for each level"""
        params = {
            1: {'num_wires': 3, 'tangle_intensity': 0.5, 'wire_length_min': 150, 'wire_length_max': 250},
            2: {'num_wires': 4, 'tangle_intensity': 0.7, 'wire_length_min': 200, 'wire_length_max': 300},
            3: {'num_wires': 5, 'tangle_intensity': 0.9, 'wire_length_min': 250, 'wire_length_max': 350},
            4: {'num_wires': 5, 'tangle_intensity': 1.2, 'wire_length_min': 300, 'wire_length_max': 400},
            5: {'num_wires': 6, 'tangle_intensity': 1.5, 'wire_length_min': 300, 'wire_length_max': 450},
        }
        return params.get(level, params[5])
    
    def initialize_level(self):
        """Create wires for the current level"""
        self.wires = []
        self.level_complete = False
        self.all_untangled = False
        
        # Create wires with random colors and lengths
        for i in range(self.num_wires):
            color = self.wire_colors[i % len(self.wire_colors)]
            length = random.uniform(self.wire_length_min, self.wire_length_max)
            
            wire = Wire(i, color, length, num_segments=30)
            
            # Position wires at different X positions but starting from top
            start_x = 100 + (i * 70)
            start_y = 150
            
            wire.initialize_points(start_x, start_y)
            self.wires.append(wire)
        
        # Apply tangles
        for _ in range(int(self.num_wires * 2 * self.tangle_intensity)):
            for wire in self.wires:
                wire.apply_tangles(self.wires, self.tangle_intensity)
    
    def on_size(self, instance, value):
        """Handle window resize"""
        pass
    
    def on_touch_down(self, touch):
        """Handle touch down - start dragging a wire"""
        for wire in self.wires:
            if wire.start_drag(touch.x, touch.y):
                touch.grab(self)
                return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        """Handle touch move - drag wires"""
        if touch.grab_current is self:
            for wire in self.wires:
                if wire.is_being_dragged:
                    wire.drag(touch.x, touch.y)
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """Handle touch up - stop dragging"""
        if touch.grab_current is self:
            for wire in self.wires:
                if wire.is_being_dragged:
                    wire.end_drag()
            touch.ungrab(self)
            return True
        return super().on_touch_up(touch)
    
    def update(self, dt):
        """Update game state"""
        # Check if all wires are untangled
        untangled_count = 0
        for wire in self.wires:
            wire.check_untangled(self.wires)
            if wire.untangled:
                untangled_count += 1
        
        if untangled_count == len(self.wires) and not self.level_complete:
            self.all_untangled = True
            self.level_complete = True
    
    def on_draw(self):
        """Draw the game"""
        pass
    
    def render(self):
        """Render all wires"""
        self.canvas.clear()
        
        with self.canvas:
            # Draw background
            Color(0.1, 0.1, 0.1, 1)
            self.canvas.clear()
            
            # Draw each wire
            for wire in self.wires:
                Color(*wire.color)
                
                # Draw as a line connecting all points
                points = []
                for point in wire.points:
                    points.extend([point.x, point.y])
                
                if len(points) >= 4:
                    Line(points=points, width=3)
                
                # Draw endpoints as circles
                if len(wire.points) > 0:
                    start = wire.points[0]
                    end = wire.points[-1]
                    
                    # Draw start point (brighter)
                    Color(*wire.color, 0.8)
                    Ellipse(pos=(start.x - 8, start.y - 8), size=(16, 16))
                    
                    # Draw end point
                    Color(*wire.color, 0.6)
                    Ellipse(pos=(end.x - 6, end.y - 6), size=(12, 12))


class GameScreen(Screen):
    """Screen for active gameplay"""
    
    def __init__(self, level=1, **kwargs):
        super().__init__(**kwargs)
        self.level = level
        
        layout = BoxLayout(orientation='vertical')
        
        # Top info bar
        info_layout = BoxLayout(size_hint_y=0.08, spacing=10, padding=10)
        
        level_label = Label(text=f'Level {level}', size_hint_x=0.3, font_size='18sp')
        info_layout.add_widget(level_label)
        
        self.status_label = Label(text='Untangle the wires!', size_hint_x=0.4, font_size='16sp')
        info_layout.add_widget(self.status_label)
        
        reset_btn = Button(text='Reset', size_hint_x=0.3, font_size='14sp')
        reset_btn.bind(on_press=self.reset_level)
        info_layout.add_widget(reset_btn)
        
        layout.add_widget(info_layout)
        
        # Game widget
        self.game_widget = WireGameWidget(level=level, size_hint_y=0.92)
        layout.add_widget(self.game_widget)
        
        self.add_widget(layout)
        
        Clock.schedule_interval(self.update_display, 0.1)
    
    def update_display(self, dt):
        """Update display and check for level completion"""
        # Render the game
        self.game_widget.render()
        
        # Update status
        untangled = sum(1 for w in self.game_widget.wires if w.untangled)
        self.status_label.text = f'Untangled: {untangled}/{len(self.game_widget.wires)}'
        
        # Check for level completion
        if self.game_widget.level_complete:
            self.show_completion()
            Clock.unschedule(self.update_display)
    
    def show_completion(self):
        """Show level completion dialog"""
        if self.level < 5:
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(Label(text=f'Level {self.level} Complete!', font_size='20sp'))
            content.add_widget(Label(text='', size_hint_y=0.3))
            
            btn_layout = BoxLayout(spacing=10, size_hint_y=0.3)
            
            next_btn = Button(text='Next Level')
            def go_next(instance):
                self.manager.current = f'game_{self.level + 1}'
            next_btn.bind(on_press=go_next)
            btn_layout.add_widget(next_btn)
            
            retry_btn = Button(text='Retry')
            def retry(instance):
                self.reset_level(None)
            retry_btn.bind(on_press=retry)
            btn_layout.add_widget(retry_btn)
            
            content.add_widget(btn_layout)
            
            popup = Popup(title='Level Complete', content=content, size_hint=(0.8, 0.4))
            popup.open()
        else:
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(Label(text='Game Complete!', font_size='22sp'))
            content.add_widget(Label(text='You\'ve untangled all 5 levels!', font_size='16sp'))
            content.add_widget(Label(text='', size_hint_y=0.3))
            
            btn_layout = BoxLayout(spacing=10, size_hint_y=0.3)
            
            menu_btn = Button(text='Main Menu')
            def go_menu(instance):
                self.manager.current = 'menu'
            menu_btn.bind(on_press=go_menu)
            btn_layout.add_widget(menu_btn)
            
            content.add_widget(btn_layout)
            
            popup = Popup(title='Game Complete!', content=content, size_hint=(0.8, 0.4))
            popup.open()
    
    def reset_level(self, instance):
        """Reset the current level"""
        self.game_widget.initialize_level()
        self.status_label.text = 'Untangle the wires!'
        Clock.schedule_interval(self.update_display, 0.1)


class MenuScreen(Screen):
    """Main menu screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        
        layout.add_widget(Label(text='WIRES', font_size='48sp', bold=True, size_hint_y=0.3))
        layout.add_widget(Label(text='Untangle colored wires to progress', font_size='16sp', size_hint_y=0.2))
        layout.add_widget(Label(text='', size_hint_y=0.1))
        
        # Level buttons
        levels_layout = GridLayout(cols=1, spacing=10, size_hint_y=0.5)
        
        for level in range(1, 6):
            btn = Button(text=f'Level {level}', font_size='18sp')
            btn.bind(on_press=self.make_level_handler(level))
            levels_layout.add_widget(btn)
        
        layout.add_widget(levels_layout)
        
        # Info button
        info_btn = Button(text='How to Play', size_hint_y=0.1)
        info_btn.bind(on_press=self.show_info)
        layout.add_widget(info_btn)
        
        self.add_widget(layout)
    
    def make_level_handler(self, level):
        """Create a handler for level selection"""
        def handler(instance):
            self.manager.current = f'game_{level}'
        return handler
    
    def show_info(self, instance):
        """Show how to play"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        info_text = """Tap and drag parts of the wires to untangle them.

Try to separate all wires so they don't overlap.

Each level gets progressively harder with more wires.

Can you complete all 5 levels?"""
        
        content.add_widget(Label(text=info_text, font_size='14sp'))
        content.add_widget(Label(text='', size_hint_y=0.2))
        
        close_btn = Button(text='Close', size_hint_y=0.2)
        popup = Popup(title='How to Play', content=content, size_hint=(0.9, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()


class WiresGame(App):
    """Main game application"""
    
    def build(self):
        # Create screen manager
        sm = ScreenManager(transition=FadeTransition())
        
        # Add menu screen
        sm.add_widget(MenuScreen(name='menu'))
        
        # Add game screens for each level
        for level in range(1, 6):
            sm.add_widget(GameScreen(level=level, name=f'game_{level}'))
        
        return sm


if __name__ == '__main__':
    WiresGame().run()
