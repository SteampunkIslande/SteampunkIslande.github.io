import markdown

AUTHOR = "Charles Monod-Broca"
SITENAME = "Let's tame that python together"

PATH = "content"

THEME = "pelican-clean-blog"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "fr"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

OUTPUT_PATH = "docs/"

# SITEURL = "https://steampunkislande.github.io"
SITEURL = ""

MARKDOWN = {
    "extensions": [
        "markdown_include.include",
        "markdown_link_attr_modifier",
        "pymdownx.highlight",
        "markdown_fenced_code_tabs",
    ],
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown_link_attr_modifier": {
            "new_tab": "on",
            "no_referrer": "external_only",
            "auto_title": "on",
        },
        "markdown_fenced_code_tabs": {
            "single_block_as_tab": False,
            "active_class": "active",
            "template": "default",
        },
    },
    "output_format": "html5",
}
