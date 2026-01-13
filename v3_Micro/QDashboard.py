import sys

class QDashboard:
    def __init__(self, window_size=50):
        self.window_size = window_size
        print("\n" * 5 + "--- PROJECT NEXUS LIVE MONITOR ---")
        
    def update(self, timestamp, z_score, position):
        # Create a text-based Z-score bar
        # [-4.0 ... 0.0 ... +4.0]
        width = 40
        pos = int((z_score + 4) / 8 * width)
        pos = max(0, min(width, pos))
        
        bar = [" "] * (width + 1)
        bar[width//2] = "|" # Center
        bar[pos] = "O"     # Current Z
        
        z_str = "".join(bar)
        pos_label = {1: "LONG", -1: "SHORT", 0: "FLAT"}[position]
        
        # Print a single line that overwrites itself
        sys.stdout.write(f"\r[{timestamp}] Z:[{z_str}] {z_score:>6.2f} | POS: {pos_label}")
        sys.stdout.flush()