# Token Piggy Bank — Portable One-Shot Installation Guide

This guide provides one-shot instructions for installing and integrating the **Token Piggy Bank** quota governor and visual telemetry dashboard into any agent fleet or web dashboard.

---

## 1. Quick Install (Static Frontend + Backend Adapter)

The Token Piggy Bank runs with **zero external runtime dependencies** (pure vanilla HTML5/SVG/ES6) backed by a JSON telemetry contract.

### Step 1: Copy Visual Dashboard Component

Include the SVG container and script in your dashboard page:

```html
<div class="piggy-container">
  <div class="piggy-header">
    <span id="ws-today" class="metric-value">0</span> tokens today
    (<span id="ws-left" class="metric-sub">0 remaining</span> / <span id="ws-total">0 limit</span>)
  </div>
  <svg id="ocean-svg" viewBox="0 0 720 360" class="ocean-viewport">
    <defs>
      <linearGradient id="ocean-grad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#0f2027"/>
        <stop offset="50%" stop-color="#203a43"/>
        <stop offset="100%" stop-color="#2c5364"/>
      </linearGradient>
    </defs>
    <rect width="720" height="360" fill="url(#ocean-grad)"/>
    <path id="wave-path-back" fill="rgba(255,255,255,0.08)"/>
    <path id="wave-path" fill="rgba(255,255,255,0.15)"/>
    <g id="wave-foam"></g>
    <g id="wave-labels"></g>
    <g id="seabed-coins"></g>
  </svg>
</div>
<script src="assets/js/piggy.js"></script>
```

### Step 2: Telemetry Data Contract (`tokens.json`)

Publish the telemetry state file at `data/tokens.json`:

```json
{
  "updated_at": "2026-08-21T20:45:00Z",
  "verification_state": "VERIFIED",
  "current_window": {
    "window_hours": 24,
    "used": 142500,
    "available": 857500,
    "total": 1000000,
    "reset": "2026-08-22T00:00:00Z"
  },
  "burn_pacing": {
    "ratio": 0.85,
    "status": "on_pace",
    "reserve_floor_pct": 20.0
  },
  "history": [
    { "date": "2026-08-15", "used": 210000 },
    { "date": "2026-08-16", "used": 185000 },
    { "date": "2026-08-17", "used": 320000 },
    { "date": "2026-08-18", "used": 140000 },
    { "date": "2026-08-19", "used": 290000 },
    { "date": "2026-08-20", "used": 245000 },
    { "date": "2026-08-21", "used": 142500 }
  ],
  "milestones": {
    "coin_denomination": 250000,
    "total_spent_tokens": 1532500,
    "seabed_coin_count": 6
  }
}
```

---

## 2. Backend Governor Integration

Integrate the quota checks into your dispatch loop before invoking LLMs:

```python
import json
from pathlib import Path

def check_quota_governor(data_path: Path, requested_tier: str = "balanced") -> bool:
    data = json.loads(data_path.read_text())
    pacing = data.get("burn_pacing", {})
    ratio = pacing.get("ratio", 1.0)

    # Circuit breaker
    if ratio > 2.0:
        return False

    # Downgrade / reserve enforcement
    if ratio > 1.5 and requested_tier == "premium":
        return False

    return True
```

---

## 3. Verification & Validation

1. Run repository validation:
   ```bash
   ./validate.sh
   ```
2. Verify visual telemetry rendering in the dashboard.
3. Assert that no secrets, tokens, or absolute local user home paths are hardcoded.
