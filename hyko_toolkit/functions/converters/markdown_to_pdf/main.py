import datetime
from io import BytesIO

import markdown
import pygments
from fpdf import FPDF
from metadata import Inputs, Outputs, Params, func
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from hyko_sdk.io import PDF
from hyko_sdk.types import Ext


def format_code_block(code: str, language: str):
    """
    Format code blocks in the markdown to highlight syntax using Pygments.

    Args:
    code (str): The code block content.
    language (str): The programming language of the code block.

    Returns:
    str: The formatted code block as HTML.
    """
    try:
        lexer = get_lexer_by_name(language, stripall=True)
    except ClassNotFound:
        lexer = get_lexer_by_name("text", stripall=True)

    formatter = HtmlFormatter(full=True, linenos="inline", style="solarized-light")
    return pygments.highlight(code, lexer, formatter)


def convert_markdown_to_pdf(markdown_string: str):
    """
    Convert Markdown content to PDF format.

    Args:
    markdown_string (str): The Markdown content to convert.

    Returns:
    bytes: The binary content of the generated PDF.
    """
    # Custom CSS for typography
    css = """
    body {
        font-family: 'Arial', sans-serif;
        font-size: 10pt;
        line-height: 1.6;
        color: #000000;
    }
    a {
        color: #000000; /* Change hyperlink color */
        text-decoration: underline;
    }
    h1 {
        font-size: 24pt; /* Larger font size for h1 */
        color: #000000; /* Darker color for h1 */
    }
    h2 { font-size: 20pt;color: #000000; } /* Slightly larger font size for h2 */
    h3 { font-size: 16pt; color: #000000;} /* Slightly larger font size for h3 */
    h4 { font-size: 14pt; color: #000000;} /* Slightly larger font size for h4 */
    h5, h6 { font-size: 12pt; color: #000000;} /* Slightly larger font size for h5 and h6 */
    pre { font-size: 10pt;color: #000000; } /* Smaller font size for code blocks */
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid #000000;
        padding: 4pt 8pt;
        text-align: left;
    }
    th {
        background-color: #f0f0f0;
        font-weight: bold;
    }
    """

    # Configure markdown to use custom code block formatter and custom CSS
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.extra",
        ],
        extension_configs={
            "markdown.extensions.codehilite": {
                "css_class": "highlight",
                "guess_lang": True,
                "use_pygments": True,
                "pygments_style": "solarized-light",
                "custom_formatter": format_code_block,
            },
            "markdown.extensions.extra": {
                "header_levels": [1, 2, 3, 4, 5, 6],
            },
        },
        output_format="html5",
    )
    md.css = css
    # Convert markdown to HTML
    html = md.convert(markdown_string)

    # Create a PDF object
    pdf = FPDF(format="Letter")
    pdf.add_page()
    title = ""
    if "<h1>" in html:
        title = html.split("<h1>")[1].split("</h1>")[0]
    pdf.set_title(title)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, title, 0, 1, "C")
    pdf.ln(10)  # Add some space after the title

    pdf.set_font("Arial", "", 10)
    pdf.set_y(-15)
    pdf.cell(0, 10, f"Page {pdf.page_no()}", 0, 0, "C")
    # add datetime
    pdf.cell(0, 10, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0, "R")
    pdf.write_html(html)
    buf = BytesIO()
    pdf.output(buf, "F")
    return buf.getvalue()


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    buff = convert_markdown_to_pdf(inputs.markdown_string)
    return Outputs(pdf=PDF(val=buff, obj_ext=Ext.PDF))
