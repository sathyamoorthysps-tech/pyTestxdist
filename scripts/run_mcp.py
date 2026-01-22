import subprocess
import sys
from pathlib import Path
import os
import re

ROOT = Path(__file__).parent.parent
CONTEXT_FILE = ROOT / "mcp" / "context.yaml"


def simple_yaml_parse(path: Path):
    """Very small YAML-ish parser for our simple `context.yaml` structure.
    Falls back when PyYAML isn't available.
    Only supports the keys present in our context file (flat and one nested dict for viewport).

    Improvements:
    - Support list items (lines starting with '-') under a nested key
    - Attempt JSON decoding for scalar values (so strings like '["--no-sandbox"]' are parsed to lists)
    """
    import json

    result = {}
    current_section = None
    last_key = None
    last_key_indent = None

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip('\n')
            if not line.strip() or line.strip().startswith('#'):
                continue

            line_indent = len(line) - len(line.lstrip(' '))
            # list item handling (e.g., '  - --no-sandbox')
            li = re.match(r"^\s*-\s*(.*)$", line)
            if li and current_section and last_key is not None and line_indent > last_key_indent:
                raw_value = li.group(1).strip()
                if raw_value.lower() in ("true", "false"):
                    val = raw_value.lower() == "true"
                else:
                    try:
                        val = int(raw_value)
                    except:
                        try:
                            val = json.loads(raw_value)
                        except Exception:
                            val = raw_value.strip().strip('"').strip("'")
                result.setdefault(current_section, {}).setdefault(last_key, []).append(val)
                continue

            # detect top-level key
            m = re.match(r"^(\s*)([a-zA-Z0-9_\-]+):(?:\s*(.*))?$", line)
            if not m:
                continue
            indent, key, value = m.groups()
            indent_level = len(indent)

            if indent_level == 0:
                # top-level
                current_section = key
                last_key = None
                last_key_indent = None
                if value is None or value == "":
                    # start a dict
                    result[key] = {}
                else:
                    # scalar at top-level; attempt bool/int/json
                    raw_value = value.strip()
                    if raw_value.lower() in ("true", "false"):
                        val = raw_value.lower() == "true"
                    else:
                        try:
                            val = int(raw_value)
                        except:
                            try:
                                val = json.loads(raw_value)
                            except Exception:
                                val = raw_value.strip().strip('"').strip("'")
                    result[key] = val
            else:
                # nested value
                if current_section is None:
                    continue
                # For viewport, further nesting
                sub_match = re.match(r"^\s*([a-zA-Z0-9_\-]+):(?:\s*(.*))?$", line)
                if not sub_match:
                    continue
                skey, svalue = sub_match.groups()
                last_key = skey
                last_key_indent = indent_level
                if current_section == "playwright" and skey == "viewport":
                    # viewport is likely followed by indented width/height lines; handle above
                    result.setdefault("playwright", {}).setdefault("viewport", {})
                    # viewport isn't a list, so clear last_key
                    last_key = None
                    last_key_indent = None
                    continue
                # handle list or scalar where svalue is empty
                if svalue is None or svalue == "":
                    # Initialize as an empty list to accept subsequent '- item' lines
                    result.setdefault(current_section, {})[skey] = []
                    continue
                # parse scalar; attempt bool/int/json
                raw_value = svalue.strip()
                if raw_value.lower() in ("true", "false"):
                    sval = raw_value.lower() == "true"
                else:
                    try:
                        sval = int(raw_value)
                    except:
                        try:
                            sval = json.loads(raw_value)
                        except Exception:
                            sval = raw_value.strip().strip('"').strip("'")
                if current_section == "playwright" and skey in ("width", "height"):
                    result.setdefault("playwright", {}).setdefault("viewport", {})[skey] = sval
                else:
                    result.setdefault(current_section, {})[skey] = sval

    return result


try:
    import yaml

    def load_context():
        if not CONTEXT_FILE.exists():
            print(f"Context file not found at {CONTEXT_FILE}")
            sys.exit(1)
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
except Exception:
    def load_context():
        if not CONTEXT_FILE.exists():
            print(f"Context file not found at {CONTEXT_FILE}")
            sys.exit(1)
        print("PyYAML not available; using simple parser for mcp/context.yaml")
        return simple_yaml_parse(CONTEXT_FILE)


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
