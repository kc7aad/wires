# Wires - Game Mechanics & Physics

## Core Concepts

### Wire Structure
Each wire is composed of a series of points connected in sequence:
- **Points:** Individual coordinates along the wire path
- **Segments:** Connections between consecutive points
- **Length:** Total distance from start to end (defines number of points)

```
Wire = [Point(0), Point(1), Point(2), ... Point(N)]
```

### Wire Properties
```python
wire = Wire(
    wire_id=0,           # Unique identifier
    color=(1, 0, 0, 1),  # RGBA color
    length=200,          # Total wire length in pixels
    num_segments=30      # Number of points (resolution)
)
```

## Physics System

### 1. Wire Tangling

Wires are tangled by simulating proximity-based interactions:

```python
def apply_tangles(self, other_wires, intensity=1.0):
    for point in self.points:
        for other_point in other_wires:
            distance = point.distance_to(other_point)
            if distance < 30 * intensity:
                # Push points apart
                angle = atan2(dy, dx)
                push_distance = (30 * intensity - distance) * 0.5
                point.x += cos(angle) * push_distance
                point.y += sin(angle) * push_distance
```

**Parameters:**
- `intensity`: Controls how strong the tangling is (0.5 = loose, 2.0 = tight)
- `threshold`: Distance at which wires "feel" each other (30px default)
- `push_distance`: How far apart points are pushed (proportional to overlap)

### 2. Drag Mechanics

When a player touches a wire:

1. **Detection** - Find the closest point on any wire within 40px
2. **Drag Point** - Apply force to that point
3. **Influence Falloff** - Nearby points feel proportional force
   ```python
   influence = max(0, 1 - (distance_to_drag_point / 5.0))
   ```
4. **Damping** - Movement is reduced by 20% for smooth control
   ```python
   point.x += dx * influence * 0.8
   ```

**Why the falloff?**
- Makes wires bend naturally
- Prevents wires from becoming stiff or unrealistic
- Allows localized untangling

### 3. Untangle Detection

A wire is considered untangled when:

```python
untangled_count = 0
for point_i in self.points:
    for point_j in other_wire.points:
        if distance < 25:  # Overlap threshold
            untangled_count += 1

wire.untangled = (untangled_count < 5)
```

**Criteria:**
- **Overlap Threshold:** 25px (wires must be separated by this distance)
- **Tolerance:** Allows up to 4 intersection points per wire
- **Global Check:** All wires must be untangled simultaneously

## Difficulty System

### Level Scaling

Each level increases difficulty through multiple parameters:

```python
difficulty_params = {
    1: {
        'num_wires': 3,
        'tangle_intensity': 0.5,    # Loose tangles
        'wire_length_min': 150,
        'wire_length_max': 250
    },
    5: {
        'num_wires': 6,
        'tangle_intensity': 1.5,    # Very tight tangles
        'wire_length_min': 300,
        'wire_length_max': 450      # Much longer wires
    }
}
```

### Why Each Parameter Matters

| Parameter | Level 1 | Level 5 | Effect |
|-----------|---------|---------|--------|
| **Wires** | 3 | 6 | More to track; more intersections |
| **Length** | 150-250px | 300-450px | Longer paths = more tangles |
| **Intensity** | 0.5 | 1.5 | Stronger physics = harder to move wires |
| **Complexity** | Low | High | Combined effect: 3x harder |

## Wire Generation Algorithm

### Initialization Phase

```python
def initialize_points(start_x, start_y):
    for i in range(num_segments + 1):
        noise_x = random.uniform(-10, 10)
        noise_y = random.uniform(-10, 10)
        
        x = current_x + noise_x
        y = current_y + segment_length + noise_y
        
        points.append(Point(x, y))
```

**Result:** Slightly wavy initial wires (not perfectly straight)

### Tangling Phase

Applied multiple times per level:

```python
for iteration in range(int(num_wires * 2 * intensity)):
    for wire in wires:
        wire.apply_tangles(other_wires, intensity)
```

**Formula:** `num_iterations = num_wires × 2 × intensity`
- Level 1: 3 × 2 × 0.5 = 3 iterations
- Level 5: 6 × 2 × 1.5 = 18 iterations

More iterations = more complex tangles

## Rendering Pipeline

### Frame Update (60 FPS)
```
1. Process touch input → update wire positions
2. Apply physics → check wire collisions
3. Detect untangling → update game state
4. Render → draw wires to canvas
```

### Visual Representation

Each wire is drawn as:

```python
# Line connecting all points
Line(points=[x0, y0, x1, y1, ...], width=3)

# Start point (bright circle)
Ellipse(pos=(x-8, y-8), size=(16, 16), color=wire_color)

# End point (dimmer circle)
Ellipse(pos=(x-6, y-6), size=(12, 12), color=wire_color)
```

**Why two endpoints?**
- Helps player visualize wire direction
- Start (bright) → End (dim) shows wire flow
- Makes it clearer which end is which for longer wires

## Performance Optimization

### Complexity Analysis

**Time per frame:**
- Touch handling: O(1)
- Point-to-point distance: O(n²) where n = points per wire
- Untangle detection: O(w²n²) where w = number of wires
- Rendering: O(w × n)

**Optimization strategies:**
- Use 30 segments per wire (good balance of smoothness vs speed)
- Check untangle every 10 frames, not every frame
- Cache distance calculations where possible

### Mobile Performance

Tested configurations:
- **Device:** Android 6.0+ with 2GB RAM
- **Target FPS:** 60 (logic), 10 (UI updates)
- **Memory:** ~50MB per game session

## Customization Guide

### Modify Wire Physics

**Make wires stretchier (easier):**
```python
influence = max(0, 1 - (distance / 8.0))  # More points affected
point.x += dx * influence * 0.95           # Less damping
```

**Make wires stiffer (harder):**
```python
influence = max(0, 1 - (distance / 3.0))  # Fewer points affected
point.x += dx * influence * 0.6            # More damping
```

### Adjust Difficulty

**For each level:**
```python
# Current
'tangle_intensity': 0.5 + (level * 0.25)

# Make it harder
'tangle_intensity': 0.5 + (level * 0.4)

# Make it easier
'tangle_intensity': 0.3 + (level * 0.15)
```

### Change Wire Colors

Edit the `wire_colors` list:
```python
self.wire_colors = [
    (1, 0, 0, 1),      # Red
    (0, 1, 0, 1),      # Green
    (0, 0, 1, 1),      # Blue
    # Add more colors here
]
```

### Add More Levels

Add to `get_difficulty_params()`:
```python
6: {
    'num_wires': 7,
    'tangle_intensity': 1.8,
    'wire_length_min': 350,
    'wire_length_max': 500
}
```

Then update `QUICKSTART.md` and menu to reference level 6.

## Testing & Tuning

### Manual Testing Checklist

- [ ] Wires start visibly tangled
- [ ] Dragging a wire affects only nearby points
- [ ] Wires resist passing through each other
- [ ] Untangle detection triggers correctly (no false positives)
- [ ] Each level is progressively harder
- [ ] Game runs at 60 FPS on target device

### Performance Profiling

To check FPS on desktop:
```python
Clock.schedule_interval(print_fps, 1)

def print_fps(dt):
    fps = 1 / dt if dt > 0 else 0
    print(f"FPS: {fps:.1f}")
```

### Difficulty Balance

Test using:
- **Easy enough?** Can beat level 1 in < 1 minute
- **Hard enough?** Level 5 takes 5-10 minutes
- **Fair?** Solutions always exist (no impossible tangles)

## Advanced Physics

### Future Enhancements

**Realistic Wire Physics:**
```python
# Add spring forces between points
spring_force = (target_distance - current_distance) * stiffness
point.x += spring_force * cos(angle)
point.y += spring_force * sin(angle)
```

**Collision System:**
```python
# Prevent wires from overlapping
for point_i in wire1.points:
    for point_j in wire2.points:
        if distance < min_separation:
            # Push apart with more force
            separate_points(point_i, point_j)
```

**Gravity & Inertia:**
```python
# Add weight to make wires feel physical
velocity_x += acceleration_x * dt
point.x += velocity_x * dt
```

## Debugging

### Common Physics Issues

**Problem:** Wires won't separate
- Check `tangle_intensity` - might be too high
- Reduce `threshold` in `apply_tangles()` to 20px
- Increase damping in `drag()` to 0.6

**Problem:** Wires feel too "sticky"
- Reduce `influence` falloff distance
- Increase damping (multiply by 0.95 instead of 0.8)

**Problem:** Wires glitch/teleport**
- Reduce `segment_length` to create more points
- Lower `push_distance` multiplier in tangling

## Summary

The Wires game uses:
1. **Point-based representation** for flexible wire shapes
2. **Proximity physics** for natural tangling
3. **Inverse distance damping** for smooth drag handling
4. **Overlap detection** to verify untangling
5. **Scaled difficulty** to challenge players progressively

This creates a physics-like system without heavy 3D simulation, perfect for mobile!
