# Input analytics — free setup (Google Sheets)

Stores every visitor scenario (income amounts, state, options — never identity) in a
Google Sheet you own. Zero cost, no third-party signup.

## Setup (~5 minutes)

1. Create a new Google Sheet (e.g. "TakeHome inputs").
2. In the Sheet: **Extensions → Apps Script**. Delete the sample code and paste the
   contents of `apps-script.gs`. Save.
3. **Deploy → New deployment → Web app**:
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click Deploy, authorize, and copy the web app URL (ends in `/exec`).
4. In `docs/index.html` (and `prototype/takehome-map.html` to keep them in sync),
   find `const ANALYTICS_ENDPOINT = '';` and paste the URL between the quotes.
5. Commit and push. Rows appear in the `inputs` sheet as visitors use the site.

## What gets recorded

One row per event — `scenario` (3 s after the user stops typing), `share`, `tab`,
`leave` — containing: timestamp, a random per-visit session id, tax year, selected
state, and the scenario inputs as JSON. No names, emails, IPs*, or accounts.

\* Apps Script does not expose the sender's IP to your code, and nothing else here
collects it.

## Privacy obligations (do these before real traffic)

- The site footer already discloses the collection — keep it visible.
- Income figures are sensitive: don't share the raw sheet publicly, and consider a
  simple privacy-policy page if traffic grows (required for AdSense/affiliate
  programs anyway).
- Sends are capped at ~40 per visit; Apps Script free quotas comfortably handle
  tens of thousands of rows/day. If you outgrow it, swap the endpoint for a
  Supabase/Cloudflare Worker URL — the site-side code needs no other change.

## Testing

After deploying, run in a browser console on your site:

```js
fetch('YOUR_EXEC_URL', { method: 'POST', body: JSON.stringify({ sid: 'test', event: 'scenario', year: 2026, state: 'TX', inputs: { w2: 1 } }) })
```

A row should appear in the sheet within seconds.
