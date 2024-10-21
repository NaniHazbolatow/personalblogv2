from manim import *
import numpy as np

class BlackScholesDiffusionToLogo(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[0, 10, 1],  # Time axis
            y_range=[0, 200, 20],  # Stock price axis
            axis_config={"include_numbers": True}
        )
        axes_labels = axes.get_axis_labels(x_label="Time", y_label="Stock Price")

        # Add axes and title
        self.add(axes, axes_labels)
        title = Text("Black-Scholes Diffusion Process").to_edge(UP)
        self.add(title)

        # Number of random stock price paths
        n_paths = 5
        colors = [RED, BLUE, GREEN, ORANGE, PURPLE]

        # Generate stock price diffusion paths
        stock_paths = []
        for i in range(n_paths):
            stock_path = self.get_stock_price_path(axes, colors[i % len(colors)])
            stock_paths.append(stock_path)
            self.play(Create(stock_path), run_time=3)

        self.wait()

        # Converge stock price paths to form the logo
        logo_position = axes.coords_to_point(5, 100)  # Final position for logo

        for stock_path in stock_paths:
            self.play(stock_path.animate.move_to(logo_position), run_time=2)

        # Display the logo
        logo = SVGMobject("path_to_your_logo.svg").move_to(logo_position).scale(1.5)
        self.play(FadeIn(logo))

        self.wait()

    def get_stock_price_path(self, axes, color):
        """Generate a single stock price path following a geometric Brownian motion."""
        T = 10  # Time duration
        N = 100  # Number of steps
        dt = T / N
        mu = 0.1  # Drift (mean return)
        sigma = 0.3  # Volatility
        S0 = 100  # Initial stock price

        # Simulate stock prices
        times = np.linspace(0, T, N)
        prices = [S0]
        for _ in range(1, N):
            dS = mu * prices[-1] * dt + sigma * prices[-1] * np.sqrt(dt) * np.random.normal()
            prices.append(prices[-1] + dS)

        # Convert stock prices into points on the graph
        path_points = [axes.coords_to_point(t, S) for t, S in zip(times, prices)]
        stock_path = VMobject()
        stock_path.set_points_smoothly(path_points)
        stock_path.set_color(color)
        
        return stock_path
