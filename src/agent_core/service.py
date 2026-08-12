"""FastAPI app for every agent: health/metrics, the /run endpoint, and a small
built-in **test console** at ``/`` so any agent is testable in a browser.

Heavy deps (fastapi/uvicorn) are imported lazily so ``import agent_core`` works
without them; they're only needed when an agent actually serves.
"""
from __future__ import annotations

from . import monitoring
from .intake import Intake
from .manager import RunManager


def create_app(agent):
    from fastapi import Body, FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI(title=agent.name)
    manager = RunManager(agent)
    intake = Intake()

    @app.get("/healthz")
    def healthz():
        return monitoring.healthz()

    @app.get("/readyz")
    def readyz():
        return {"status": "ready", "agent": agent.name}

    @app.get("/metrics")
    def metrics():
        return monitoring.metrics()

    @app.post("/run")
    def run(payload: dict = Body(..., examples=[{"input": "echo hello"}])):
        # Arbitrary JSON body (input, plus any extra keys like repo_url).
        return manager.run_once(intake.accept(payload))

    @app.get("/", response_class=HTMLResponse)
    def console():
        return _CONSOLE_HTML.replace("__AGENT__", agent.name)

    return app


def serve(agent, host: str = "0.0.0.0", port: int = 8080) -> None:
    import uvicorn

    uvicorn.run(create_app(agent), host=host, port=port)


# A tiny self-contained test console served at GET / — no build step, no CDN.
_CONSOLE_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__AGENT__ · test console</title>
<style>
  :root { color-scheme: light dark; }
  body { font: 15px/1.5 system-ui, sans-serif; max-width: 760px; margin: 2rem auto;
         padding: 0 1rem; }
  h1 { font-size: 1.3rem; margin: 0 0 .25rem; }
  h1 span { font-weight: 400; opacity: .55; }
  .links { opacity: .7; font-size: .85rem; margin-bottom: 1rem; }
  textarea { width: 100%; min-height: 92px; font: 13px ui-monospace, monospace;
             padding: .6rem; box-sizing: border-box; border-radius: 8px;
             border: 1px solid #8884; background: #8881; }
  button { margin-top: .6rem; padding: .5rem 1.1rem; font-size: .95rem; cursor: pointer;
           border: 0; border-radius: 8px; background: #3b82f6; color: #fff; }
  pre { margin-top: 1rem; padding: .8rem; background: #8881; border-radius: 8px;
        white-space: pre-wrap; word-break: break-word; min-height: 2rem; }
</style></head>
<body>
  <h1>__AGENT__ <span>· test console</span></h1>
  <div class="links">POST to <code>/run</code> &nbsp;·&nbsp;
    <a href="/docs">/docs</a> &nbsp;·&nbsp; <a href="/healthz">/healthz</a></div>
  <textarea id="in">{"input": "echo hello"}</textarea><br>
  <button id="go">Run &#9654;</button>
  <pre id="out">Response will appear here.</pre>
  <script>
    const btn = document.getElementById('go'),
          out = document.getElementById('out'),
          inp = document.getElementById('in');
    btn.onclick = async () => {
      const raw = inp.value.trim();
      let body;
      try { body = JSON.parse(raw); } catch (e) { body = { input: raw }; }
      out.textContent = 'Running...';
      btn.disabled = true;
      try {
        const r = await fetch('/run', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify(body),
        });
        const t = await r.text();
        let pretty; try { pretty = JSON.stringify(JSON.parse(t), null, 2); } catch { pretty = t; }
        out.textContent = (r.ok ? '' : 'HTTP ' + r.status + '\\n') + pretty;
      } catch (e) { out.textContent = 'Error: ' + e; }
      finally { btn.disabled = false; }
    };
  </script>
</body></html>
"""
