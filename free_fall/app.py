import tkinter as tk
import math
import time
from dataclasses import dataclass
from typing import Callable

# ==================== PHYSICS MODEL ====================
@dataclass
class BallPhysics:
    """Physics parameters for bouncing ball simulation."""
    gravity: float = 9.8  # m/s²
    restitution: float = 0.8  # coefficient of restitution
    height_threshold: float = 0.1  # stop simulation below this height (m)
    initial_height: float = 100.0  # meters
    
    def get_impact_velocity(self, height: float) -> float:
        """Velocity when hitting ground from given height."""
        return math.sqrt(2 * self.gravity * height)
    
    def get_rise_height(self, impact_velocity: float) -> float:
        """Maximum height reached after bounce with given impact velocity."""
        bounce_velocity = self.restitution * impact_velocity
        return (bounce_velocity ** 2) / (2 * self.gravity)
    
    def get_fall_time(self, height: float) -> float:
        """Time to fall from given height to ground."""
        return math.sqrt(2 * height / self.gravity)
    
    def get_rise_time(self, height: float) -> float:
        """Time to rise to given maximum height after bounce."""
        velocity = math.sqrt(2 * self.gravity * height)
        return velocity / self.gravity

# ==================== ANIMATION CONTROLLER ====================
class BouncingBallAnimation:
    def __init__(self, canvas: tk.Canvas, physics: BallPhysics):
        self.canvas = canvas
        self.physics = physics
        self.ball = None
        self.animation_id = None
        self.is_animating = False
        
        # Animation state
        self.current_height = physics.initial_height
        self.current_phase = "falling"  # "falling" or "rising"
        self.bounce_count = 0
        self.animation_start_time = 0
        
        # UI elements
        self.info_label = None
        self.height_label = None
        
        # Calculate display parameters based on canvas size
        self.setup_display_parameters()
    
    def setup_display_parameters(self):
        """Calculate display scaling based on canvas dimensions."""
        # Ensure geometry is updated
        try:
            self.canvas.update_idletasks()
        except Exception:
            pass

        self.canvas_width = self.canvas.winfo_width() or self.canvas.winfo_reqwidth()
        self.canvas_height = self.canvas.winfo_height() or self.canvas.winfo_reqheight()
        
        # Reserve 20% space above max height for visual comfort
        max_possible_height = self.physics.initial_height
        self.pixels_per_meter = (self.canvas_height * 0.8) / max_possible_height
        
        # Ground position (10% from bottom)
        self.ground_y = self.canvas_height * 0.9
        self.ball_radius = 15
    
    def create_ball(self):
        """Create the ball object on canvas."""
        # Recompute display params in case canvas was resized
        self.setup_display_parameters()

        x_center = self.canvas_width / 2
        y_initial = self.ground_y - (self.current_height * self.pixels_per_meter)

        if self.ball is None:
            self.ball = self.canvas.create_oval(
                x_center - self.ball_radius,
                y_initial - self.ball_radius,
                x_center + self.ball_radius,
                y_initial + self.ball_radius,
                fill="blue",
                outline="darkblue",
                width=2
            )
        else:
            self.update_ball_position(self.current_height)
    
    def update_ball_position(self, height: float):
        """Update ball position based on current height."""
        x_center = self.canvas_width / 2
        y_pos = self.ground_y - (height * self.pixels_per_meter)
        
        self.canvas.coords(
            self.ball,
            x_center - self.ball_radius,
            y_pos - self.ball_radius,
            x_center + self.ball_radius,
            y_pos + self.ball_radius
        )
    
    def update_info_display(self):
        """Update the information display."""
        if self.info_label:
            self.info_label.config(
                text=f"Bounce #{self.bounce_count} | "
                     f"Height: {self.current_height:.2f}m | "
                     f"Phase: {self.current_phase.title()}"
            )
    
    def animate_fall(self, start_height: float, duration: float, callback: Callable):
        """
        Animate falling motion from start_height to ground.
        duration: total time for the fall in seconds
        """
        # Deprecated: legacy per-phase animation. Use continuous integration.
        return
    
    def animate_rise(self, target_height: float, duration: float, callback: Callable):
        """
        Animate rising motion from ground to target_height.
        duration: total time for the rise in seconds
        """
        # Deprecated: legacy per-phase animation. Use continuous integration.
        return

    def step(self):
        """Physics integration step called on each frame."""
        if not self.is_animating:
            return

        now = time.time()
        dt = now - getattr(self, "last_time", now)
        self.last_time = now

        # Integrate motion: velocity positive = upward, gravity pulls down
        self.velocity -= self.physics.gravity * dt
        self.current_height += self.velocity * dt

        # Collision with ground
        if self.current_height <= 0:
            self.current_height = 0
            # If velocity is small, stop simulation
            if abs(self.velocity) < 0.1:
                self.stop_animation()
                if self.info_label:
                    self.info_label.config(text=f"Simulation Complete! {self.bounce_count} bounces. Final height: {self.current_height:.3f}m")
                return
            # Bounce
            self.velocity = -self.velocity * self.physics.restitution
            self.bounce_count += 1

        self.update_ball_position(self.current_height)
        self.update_info_display()

        # Schedule next frame (~60 FPS)
        self.animation_id = self.canvas.after(16, self.step)
    
    def start_bounce_cycle(self):
        """Start or continue the bouncing cycle."""
        # Not used with continuous integrator; keep for backward compat.
        if not self.is_animating:
            return
    
    def start_animation(self):
        """Start the animation."""
        if self.is_animating:
            return
        self.is_animating = True
        self.bounce_count = 0
        self.current_height = self.physics.initial_height
        self.current_phase = "falling"
        self.velocity = 0.0
        self.last_time = time.time()

        # Ensure ball exists and display params are current
        self.create_ball()
        self.update_ball_position(self.current_height)
        self.update_info_display()
        self.step()
    
    def stop_animation(self):
        """Stop the animation."""
        self.is_animating = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
    
    def reset_animation(self):
        """Reset the animation to initial state."""
        self.stop_animation()
        self.current_height = self.physics.initial_height
        self.current_phase = "falling"
        self.bounce_count = 0
        self.velocity = 0.0
        self.update_ball_position(self.current_height)
        self.update_info_display()

# ==================== MAIN APPLICATION ====================
class BouncingBallApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Bouncing Ball Simulation")
        self.root.geometry("400x600")
        
        # Create physics model
        self.physics = BallPhysics()
        
        # Create UI
        self.setup_ui()
        
        # Create animation controller
        self.animation = BouncingBallAnimation(self.canvas, self.physics)
        self.animation.info_label = self.info_label
        self.animation.create_ball()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Start button
        self.start_button = tk.Button(
            control_frame,
            text="Start Simulation",
            command=self.start_simulation,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(
            control_frame,
            text="Reset",
            command=self.reset_simulation,
            bg="orange",
            font=("Arial", 10)
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_button = tk.Button(
            control_frame,
            text="Stop",
            command=self.stop_simulation,
            bg="red",
            fg="white",
            font=("Arial", 10)
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Parameters frame
        param_frame = tk.Frame(self.root)
        param_frame.pack(pady=5)
        
        # Initial height control
        tk.Label(param_frame, text="Initial Height (m):").pack(side=tk.LEFT, padx=5)
        self.height_var = tk.DoubleVar(value=self.physics.initial_height)
        height_scale = tk.Scale(
            param_frame,
            from_=10,
            to=200,
            orient=tk.HORIZONTAL,
            variable=self.height_var,
            length=150
        )
        height_scale.pack(side=tk.LEFT, padx=5)
        
        # Bounciness control
        tk.Label(param_frame, text="Bounciness:").pack(side=tk.LEFT, padx=5)
        self.bounce_var = tk.DoubleVar(value=self.physics.restitution)
        bounce_scale = tk.Scale(
            param_frame,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.bounce_var,
            length=100
        )
        bounce_scale.pack(side=tk.LEFT, padx=5)
        
        # Canvas for animation
        self.canvas = tk.Canvas(
            self.root,
            width=350,
            height=400,
            bg="lightgray",
            highlightthickness=2,
            highlightbackground="black"
        )
        self.canvas.pack(pady=10)
        
        # Draw ground
        self.canvas.create_rectangle(
            0, 360, 350, 400,
            fill="brown",
            outline="black",
            width=2
        )
        self.canvas.create_text(
            175, 380,
            text="GROUND",
            fill="white",
            font=("Arial", 10, "bold")
        )
        
        # Information label
        self.info_label = tk.Label(
            self.root,
            text="Ready to simulate. Click Start.",
            font=("Arial", 10),
            bg="white",
            relief=tk.SUNKEN,
            width=50,
            height=2
        )
        self.info_label.pack(pady=5)
        
        # Stats label
        self.stats_label = tk.Label(
            self.root,
            text=f"Initial Height: {self.physics.initial_height}m | "
                 f"Bounciness: {self.physics.restitution}",
            font=("Arial", 9),
            fg="blue"
        )
        self.stats_label.pack()
    
    def start_simulation(self):
        """Start the simulation with current parameters."""
        # Update physics parameters
        self.physics.initial_height = self.height_var.get()
        self.physics.restitution = self.bounce_var.get()
        
        # Update stats display
        self.stats_label.config(
            text=f"Initial Height: {self.physics.initial_height}m | "
                 f"Bounciness: {self.physics.restitution}"
        )
        
        # Reset and start animation
        self.animation.reset_animation()
        self.animation.physics = self.physics
        self.animation.start_animation()
    
    def stop_simulation(self):
        """Stop the simulation."""
        self.animation.stop_animation()
        self.info_label.config(text="Simulation Stopped")
    
    def reset_simulation(self):
        """Reset the simulation."""
        self.animation.reset_animation()
        self.info_label.config(text="Reset to initial state. Click Start to simulate.")
        self.stats_label.config(
            text=f"Initial Height: {self.physics.initial_height}m | "
                 f"Bounciness: {self.physics.restitution}"
        )

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingBallApp(root)
    root.mainloop()
    root.mainloop()