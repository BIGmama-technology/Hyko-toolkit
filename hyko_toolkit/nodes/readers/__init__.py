"""register all apis"""
from .sheets.metadata import input_node as input_node  # noqa: F811
from .web_scraping.beautifulsoup_transformer.metadata import func as func  # noqa: F811
from .web_scraping.html2text_transformer.metadata import func as func  # noqa: F811
from .web_scraping.scrapy_crawler.metadata import func as func  # noqa: F811
from .web_search.arxiv_api.metadata import func as func  # noqa: F811
from .web_search.bing_serpapi.metadata import func as func  # noqa: F811
from .web_search.duckduckgo_search.metadata import func as func  # noqa: F811
from .web_search.duckduckgo_serpapi.metadata import func as func  # noqa: F811
from .web_search.wikipedia_api.metadata import func as func  # noqa: F811
from .web_search.wikipedia_search.metadata import func as func  # noqa: F811
