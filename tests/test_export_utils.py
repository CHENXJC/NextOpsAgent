from next_ops.export_utils import (
    ensure_output_dir,
    generate_report_filename,
    save_text_report,
)


def test_generate_report_filename_uses_single_extension():
    filename = generate_report_filename("demo_report", ".html")
    assert filename.startswith("demo_report_")
    assert filename.endswith(".html")
    assert not filename.endswith("..html")


def test_ensure_output_dir_creates_directory(tmp_path):
    output_dir = tmp_path / "nested" / "outputs"
    result = ensure_output_dir(str(output_dir))
    assert result.exists()
    assert result.is_dir()


def test_save_text_report_writes_utf8_text(tmp_path):
    output_dir = tmp_path / "reports"
    report_path = save_text_report(
        "Hello UTF-8 中文",
        filename_prefix="test_report",
        extension="md",
        output_dir=str(output_dir),
    )
    assert report_path.exists()
    assert report_path.read_text(encoding="utf-8") == "Hello UTF-8 中文"
