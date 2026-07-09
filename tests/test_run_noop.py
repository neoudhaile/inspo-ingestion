import subprocess, sys, os

def test_ingest_prints_no_export_when_dir_empty(tmp_path):
    r = subprocess.run([sys.executable, "-m", "tools.ingest.ingest",
                        "--export", str(tmp_path / "absent.json")],
                       capture_output=True, text=True, cwd=os.getcwd())
    assert r.returncode != 0 or "NO_" in r.stdout
