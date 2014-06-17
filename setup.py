import setuptools


setuptools.setup(
    name="missandei",
    version="0.1.0",
    author="Tom Leach",
    author_email="tom@gc.io",
    description="A dict to dict translation framework",
    license="BSD",
    keywords="dict transformation translation",
    url="http://github.com/gamechanger/missandei",
    packages=["missandei"],
    long_description="Missandei provides a dict-based mechanism for declaring and consuming \"Translators\". Translators can be used to translate a dict in a given known format into a new dict in a different known format.",
    tests_require=['nose']
    )
