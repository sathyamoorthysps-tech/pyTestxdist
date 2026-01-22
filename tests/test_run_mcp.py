import textwrap
from scripts.run_mcp import simple_yaml_parse


def test_simple_yaml_parse_json_args(tmp_path):
    data = textwrap.dedent('''
    playwright:
      args: ["--no-sandbox"]
      headless: true
    ''')
    p = tmp_path / "context_json.yaml"
    p.write_text(data)

    parsed = simple_yaml_parse(p)
    assert "playwright" in parsed
    assert isinstance(parsed["playwright"]["args"], list)
    assert parsed["playwright"]["args"] == ["--no-sandbox"]
    assert parsed["playwright"]["headless"] is True


def test_simple_yaml_parse_yaml_list(tmp_path):
    data = textwrap.dedent('''
    playwright:
      args:
        - --no-sandbox
        - --disable-gpu
    ''')
    p = tmp_path / "context_yaml_list.yaml"
    p.write_text(data)

    parsed = simple_yaml_parse(p)
    assert parsed["playwright"]["args"] == ["--no-sandbox", "--disable-gpu"]


def test_simple_yaml_parse_numbers_and_bool(tmp_path):
    data = textwrap.dedent('''
    playwright:
      timeout_ms: 60000
      no_sandbox: true
    ''')
    p = tmp_path / "context_nums.yaml"
    p.write_text(data)

    parsed = simple_yaml_parse(p)
    assert parsed["playwright"]["timeout_ms"] == 60000
    assert parsed["playwright"]["no_sandbox"] is True
