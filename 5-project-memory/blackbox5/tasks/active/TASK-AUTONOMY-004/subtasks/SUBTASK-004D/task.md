# SUBTASK-004D: Build bb5-dashboard TUI

**Parent Task:** TASK-AUTONOMY-004
**Depends On:** SUBTASK-004A (Core Library)
**Status:** pending
**Priority:** MEDIUM
**Estimated Tokens:** 40K

---

## Objective

Create the `bb5-dashboard` command - a live terminal UI showing real-time BB5 system status with sparklines, progress bars, and interactive controls.

---

## Success Criteria

- [ ] `bb5-dashboard` shows live updating interface
- [ ] Refreshes every 5 seconds
- [ ] Sparklines show 1-hour trends
- [ ] Color-coded health indicators
- [ ] Interactive keys work (q=quit, p=pause, r=reset)
- [ ] Graceful handling of terminal resize

---

## Implementation Plan

### Step 1: TUI Framework Setup (5K tokens)
Create `~/.blackbox5/bin/bb5-dashboard` using `rich` library:

```python
#!/usr/bin/env python3
"""BB5 Dashboard - Live terminal UI"""
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, BarColumn
import click

console = Console()

def make_layout() -> Layout:
    """Create dashboard layout"""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )

    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )

    return layout
```

### Step 2: Layout Design (8K tokens)
Design the dashboard layout:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ BB5 Dashboard                    VPS: prod-blackbox5    2026-02-06 14:32:15 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  OVERALL: [████████████████████████░░░░░░░░░░░░░░░░] 68% WARNING            │
│                                                                             │
│  ┌─ AGENTS ───────────────────────┐  ┌─ QUEUE ──────────────────────────┐  │
│  │ ● Planner    ⚠️  stale  2d     │  │ Pending      60  ██████████████  │  │
│  │ ● Executor   ⚠️  stale  2d     │  │ In Progress   5  ██░░░░░░░░░░░░  │  │
│  │                                │  │ Completed    25  █████░░░░░░░░░  │  │
│  │                                │  │                                  │  │
│  │ Last hour: ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁    │  │ Throughput: 3.5 tasks/day        │  │
│  └────────────────────────────────┘  └──────────────────────────────────┘  │
│                                                                             │
│  ┌─ HEALTH TREND (1 hour) ────────────────────────────────────────────────┐ │
│  │ Health:  ▁▁▂▂▃▃▄▄▅▅▆▆▇▇██▇▇▆▆▅▅▄▄▃▃▂▂▁▁  68% avg                    │ │
│  │ Queue:   ████████████████████████████████  60 pending                 │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─ RECENT EVENTS ────────────────────────────────────────────────────────┐ │
│  │ 14:30:15  [OK]   Planner completed loop 30                            │ │
│  │ 14:28:42  [WARN] Heartbeat timeout (120s)                             │ │
│  │ 14:25:10  [INFO] Queue depth: 60 pending                              │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  [Q]uit  [P]ause  [R]efresh  [A]gents  [Q]ueue  Refresh: 5s                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step 3: Data Refresh Loop (8K tokens)
Create live update mechanism:

```python
class Dashboard:
    def __init__(self, refresh_interval=5):
        self.refresh_interval = refresh_interval
        self.running = True
        self.paused = False
        self.history = []  # Store last 60 data points

    def run(self):
        """Main dashboard loop"""
        layout = make_layout()

        with Live(layout, refresh_per_second=4, screen=True) as live:
            while self.running:
                if not self.paused:
                    data = self.collect_data()
                    self.history.append(data)
                    self.history = self.history[-60:]  # Keep last hour

                    layout = self.update_layout(layout, data)
                    live.update(layout)

                time.sleep(self.refresh_interval)

    def collect_data(self):
        """Collect current system state"""
        return {
            'timestamp': datetime.now(),
            'health_score': calculate_health_score(),
            'queue': collect_queue_stats(),
            'agents': collect_agent_stats(),
            'events': collect_recent_events(5)
        }
```

### Step 4: Sparklines (6K tokens)
Generate sparkline characters from history:

```python
def sparkline(values, width=40):
    """Generate sparkline string from values"""
    if not values:
        return " " * width

    blocks = " ▁▂▃▄▅▆▇█"
    min_val = min(values)
    max_val = max(values)

    if max_val == min_val:
        return "█" * width

    # Sample to fit width
    step = len(values) / width
    result = []

    for i in range(width):
        idx = int(i * step)
        val = values[idx]
        normalized = (val - min_val) / (max_val - min_val)
        block_idx = int(normalized * (len(blocks) - 1))
        result.append(blocks[block_idx])

    return "".join(result)
```

### Step 5: Interactive Controls (5K tokens)
Handle keyboard input:

```python
def handle_input(self):
    """Handle keyboard input without blocking"""
    import select
    import sys
    import termios
    import tty

    # Set terminal to raw mode for single character input
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        if select.select([sys.stdin], [], [], 0)[0]:
            char = sys.stdin.read(1)

            if char == 'q':
                self.running = False
            elif char == 'p':
                self.paused = not self.paused
            elif char == 'r':
                self.refresh_now = True
            elif char == 'a':
                self.focus = 'agents'
            elif char == 'q':
                self.focus = 'queue'
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
```

### Step 6: Color Coding (4K tokens)
Apply colors based on health:

```python
def get_health_color(score):
    if score >= 90:
        return "green"
    elif score >= 75:
        return "yellow"
    elif score >= 60:
        return "orange"
    else:
        return "red"

def get_agent_status_color(agent):
    if agent.is_online():
        return "green"
    elif agent.is_stale():
        return "red"
    else:
        return "yellow"
```

### Step 7: Graceful Exit (4K tokens)
Handle terminal resize and cleanup:

```python
def on_resize(self, signum, frame):
    """Handle terminal resize"""
    self.needs_redraw = True

def cleanup(self):
    """Restore terminal on exit"""
    console.clear()
    console.show_cursor(True)
    print("Dashboard closed.")
```

---

## Files to Create

1. `~/.blackbox5/bin/bb5-dashboard` (executable)

---

## Usage Examples

```bash
# Start dashboard
bb5-dashboard

# Custom refresh rate
bb5-dashboard --refresh 10

# Focus on specific component
bb5-dashboard --focus agents
```

---

## Interactive Keys

| Key | Action |
|-----|--------|
| `q` | Quit |
| `p` | Pause/resume refresh |
| `r` | Force refresh now |
| `a` | Focus on agents panel |
| `q` | Focus on queue panel |
| `↑/↓` | Scroll focused panel |

---

## Testing

```bash
# Test dashboard
./bb5-dashboard

# Test with different refresh rates
./bb5-dashboard --refresh 2
./bb5-dashboard --refresh 10

# Test resize handling
# (resize terminal while running)
```

---

## Definition of Done

- [ ] Dashboard displays live data
- [ ] Refreshes every 5 seconds
- [ ] Sparklines show trends
- [ ] Colors indicate health status
- [ ] Interactive keys work
- [ ] Handles terminal resize
- [ ] Graceful exit on 'q'
- [ ] No flickering or display artifacts
