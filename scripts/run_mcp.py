import subprocess
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTEXT_FILE = ROOT / "mcp" / "context.yaml"


def load_context():
    if not CONTEXT_FILE.exists():
        print(f"Context file not found at {CONTEXT_FILE}")
        sys.exit(1)
    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_pytest_cmd(ctx):
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--alluredir=allure-results/mcp", "--tb=short"]
    shards = ctx.get("execution", {}).get("shards", 1)
    if shards and shards > 1:
        # Use pytest-xdist for parallelism
        cmd.extend(["-n", str(shards)])
    return cmd


def main():
    ctx = load_context()
    print("MCP Context:", ctx)

    # Export Playwright env vars so browser_factory picks them up
    pw = ctx.get("playwright", {})
    if pw:
        import os

        os.environ.setdefault("PW_HEADLESS", str(pw.get("headless", True)))
        os.environ.setdefault("PW_NO_SANDBOX", str(pw.get("no_sandbox", False)))
        os.environ.setdefault("PW_TIMEOUT_MS", str(pw.get("timeout_ms", 30000)))
        vw = pw.get("viewport", {})
        os.environ.setdefault("PW_VIEWPORT_WIDTH", str(vw.get("width", 1920)))
        os.environ.setdefault("PW_VIEWPORT_HEIGHT", str(vw.get("height", 1080)))
        os.environ.setdefault("PW_RESULTS_DIR", pw.get("results_dir", "allure-results/mcp"))

    cmd = build_pytest_cmd(ctx)
    print("Running command:", " ".join(cmd))
    rc = subprocess.call(cmd)
    if rc != 0:
        print(f"Tests failed with exit code {rc}")
        sys.exit(rc)
    print("MCP-run completed successfully.")


if __name__ == "__main__":
    main()
