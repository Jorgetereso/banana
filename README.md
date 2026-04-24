# BANANA AIRWAYS — Production Portal

Static hub for producing the Banana Airways Steam game.

## Files

- `index.html` — portal landing with 3 link cards (Brief, Timeline, Steam)
- `timeline.html` — 12-week interactive Gantt ending at the prototype milestone
- `styles.css` — shared styling
- `README.md` — this file

No build step, no dependencies. Open `index.html` in a browser locally, or deploy the whole folder to any static host.

## Preview locally

Double-click `index.html`, or run a tiny server from this folder:

```bash
# Python 3
python -m http.server 8000
# then open http://localhost:8000
```

## Deploy options

### Netlify Drop (fastest, no account needed for preview)
1. Go to https://app.netlify.com/drop
2. Drag the `bananaairways` folder onto the page.
3. You get a live URL in ~10 seconds. Share with the team.

### Render Static Site (matches your brief site)
1. Push this folder to a GitHub repo.
2. On Render → New → Static Site → connect the repo.
3. Build command: *(leave empty)*
4. Publish directory: `.` (the repo root)
5. Deploy. Render gives you `<name>.onrender.com`.

### GitHub Pages
1. Push to a GitHub repo.
2. Settings → Pages → Source: `main` branch, `/` root.
3. URL appears at `https://<user>.github.io/<repo>/`.

## Swapping the Steam link

When the Steamworks store page is live, open `index.html` and find the card with `class="card placeholder"`. Replace the `href="#"` with the Steam URL, and remove `class="placeholder"` + the `<span class="badge">Placeholder</span>` line.

## Editing the timeline

All tasks live as `<div class="bar ...">` entries in `timeline.html`. Each bar uses:

```html
<div class="bar COLOR [lane-2]" style="grid-column: N / span M;" title="Tooltip text">
  Task name
</div>
```

- `N` is the grid column (2 = W1, 3 = W2, ..., 13 = W12)
- `M` is the number of weeks the task spans
- `lane-2` places the bar on the second row of that discipline (for parallel tasks)

Discipline color classes: `slate`, `coral`, `purple`, `teal`, `orange`, `green`, `pink`, `blue`, `gold`, `milestone`.

The TODAY vertical marker auto-positions based on the real date relative to the 12-week window (Apr 20 2026 → Jul 12 2026). Change `START` in the inline script at the bottom of `timeline.html` if you reschedule.

## Prototype scope recap

**M0 — Scope lock (end W2, May 3):** GDD v1, Unity project live, pipeline doc.
**M1 — Art bible (end W4, May 17):** Style frames + hero turnaround + brand kit approved.
**M2 — First playable (end W8, Jun 14):** Hero crew rigged and moving in cabin blockout, Attend loop playable.
**M3 — PROTOTYPE (end W12, Jul 12):** Vertical slice — 1 hero crew, textured cabin, Attend + Repair, final HUD, scratch VO, local co-op.

Out of prototype scope: netcode, Defend + Fly pillars, character variety beyond hero, final VO beyond hero lines, Steam storefront polish.
