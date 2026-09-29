#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
import yaml
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = ROOT_DIR / "templates"
STYLE_DIR = ROOT_DIR / "styles"


def load_config(path: Path) -> dict[str, Any]:
    """Load and validate the YAML configuration."""

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if "resume" not in config:
        raise ValueError("Configuration must contain a [resume] section.")

    resume = config["resume"]

    if "name" not in resume:
        raise ValueError("The [resume] section must contain a 'name'.")

    if "sections" not in config:
        raise ValueError("Configuration must contain at least one [[sections]] entry.")

    return config


def load_css() -> str:
    """Load the CSS and return it as a string."""

    css_path = STYLE_DIR / "resume.css"

    if not css_path.exists():
        raise FileNotFoundError(f"CSS file not found: {css_path}")

    return css_path.read_text(encoding="utf-8")


def create_environment() -> Environment:
    """Create the Jinja2 template environment."""

    return Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_html(config: dict[str, Any]) -> str:
    """Render the resume configuration into standalone HTML."""

    environment = create_environment()
    template = environment.get_template("resume.html.j2")

    css = load_css()

    return template.render(
        resume=config["resume"],
        sections=config["sections"],
        css=css,
    )


def default_output_path(
    config_path: Path,
    output_format: str,
) -> Path:
    """Generate a sensible output filename."""

    resume_name = config_path.stem

    extension = {
        "html": ".html",
        "pdf": ".pdf",
    }[output_format]

    return config_path.parent / f"{resume_name}{extension}"


def write_html(html: str, output_path: Path) -> None:
    """Write rendered HTML to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


def write_pdf(html: str, output_path: Path) -> None:
    """Render HTML using Chromium and save it as a PDF."""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "PDF generation requires Playwright. "
            "Install dependencies with 'pip install -r requirements.txt' "
            "and then run 'playwright install chromium'."
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        try:
            page = browser.new_page()

            page.set_content(
                html,
                wait_until="load",
            )

            # The resume CSS is designed to look the same on screen and
            # when printed.
            page.emulate_media(media="screen")

            page.pdf(
                path=str(output_path),
                prefer_css_page_size=True,
                print_background=True,
                margin={
                    "top": "0",
                    "right": "0",
                    "bottom": "0",
                    "left": "0",
                },
            )
        finally:
            browser.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a resume from a YAML configuration file."
    )

    parser.add_argument(
        "config",
        type=Path,
        help="Path to the YAML resume configuration.",
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=("html", "pdf"),
        default="html",
        help="Output format. Defaults to html.",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output filename. Defaults to <config-name>.<format>.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        html = render_html(config)

        output_path = args.output or default_output_path(
            args.config,
            args.format,
        )

        if args.format == "html":
            write_html(html, output_path)
        else:
            write_pdf(html, output_path)

        print(f"Generated {args.format.upper()}: {output_path}")
        return 0

    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
