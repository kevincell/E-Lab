## Plan: Add "Meet the Creators" section to the onboarding overview page

### Where it goes
At the bottom of `templates/onboarding/overview.html` — the page that shows after login with Programme Overview, Vision & Mission, PEOs, COs, POs, and the CTA. The new "Meet the Creators" section will be inserted **after the final CTA section** (the `.cta-section` scroll-reveal block, around line 817), so it sits at the very bottom of the page.

This matches what the user described: *"the page after login has like program objective and shit, at the bottom you could add."*

### What it shows
A "Meet the Creators" section with 4 cards, each displaying:
- **Photo** (placeholder avatar — generated initials avatar via CSS, no image files needed for now; easy to swap with real photos later)
- **Name**
- **Branch** (e.g. Computer & Communication Engineering)
- **Batch year** (e.g. 2026)

### Implementation details

**1. Add the section markup in `overview.html`** — a new `<div class="scroll-reveal">` block after the CTA, reusing the existing `.section-card` / `.section-header` / `.section-icon` / `.section-title` design system so it looks native to the page:
- Section icon: 👥
- Section title: "Meet the Creators"
- Subtitle: "The team behind the CCE e-Lab"
- A 4-column responsive grid of creator cards (`.creators-grid`)

Each card:
- Placeholder avatar = a circular div with a colored gradient background and the person's initials (CSS only — no image files). You drop in real photos later by replacing the avatar div with an `<img>`.
- Name (bold)
- Branch
- Batch year (as a badge/pill, reusing `.badge-pill` styling)

I'll use placeholder names (Creator 1–4) and placeholder branch/batch values that you can edit afterward, OR leave clearly-marked TODO spots. I'll set realistic defaults: branch "Computer & Communication Engineering", batch "2026".

**2. Add CSS** — append styles to the `<style>` block in `overview.html` (this page keeps its CSS inline, matching the existing pattern). New classes:
- `.creators-grid` — `repeat(4, 1fr)`, collapses to 2 cols on tablet and 1 col on mobile
- `.creator-card` — glass card matching `.item-card` aesthetic, with hover lift
- `.creator-avatar` — circular gradient avatar with initials, theme-aware
- `.creator-name`, `.creator-branch`, `.creator-batch`
- Full light/dark theme support via `[data-theme="light"]` and `[data-theme="dark"]` overrides, matching the existing dark-theme color scheme (`#9cdef2`, `#e06c75`, `#355a66`, etc.)

**3. Scroll-reveal** — the new block uses the existing `.scroll-reveal` class, so the page's IntersectionObserver already animates it in on scroll. No new JS needed.

### Files touched
- `templates/onboarding/overview.html` — add markup + inline CSS (one file, no new routes/views/Python changes)

### Not touched
- No URL/view changes
- No new template files
- No image files added (placeholders are pure CSS; real photos can be dropped into `static/img/` later and wired in by swapping the avatar `<div>` for an `<img src="{% static 'img/...' %}">`)

### After implementation you can easily:
1. Replace placeholder names with real names
2. Edit branch/batch values
3. Swap the CSS-initials avatar for a real photo by replacing the `.creator-avatar` div with an `<img>`
4. Add social/contact links later if desired