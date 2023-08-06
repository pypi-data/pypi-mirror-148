from pathlib import Path
from pip._internal.req import parse_requirements
from setuptools import setup


VERSION = "0.0.13"
this_directory = Path(__file__).parent
with open(this_directory / "README-public.md", encoding="utf8") as file_handle:
    long_description = file_handle.read()

# pylint: disable=no-value-for-parameter
setup(
    name="sqlalchemycollector",
    version=VERSION,
    author="Metis dev",
    author_email="devops@metisdata.io",
    description="Metis log collector for Flask and SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metis-data/sqlalchemy_collector",
    project_urls={
        "Bug Tracker": "https://github.com/metis-data/sqlalchemy_collector/issues"
    },
    license="",
    packages=["sqlalchemycollector"],
    install_requires=[
        'opentelemetry-api',
        'opentelemetry-sdk',
        'sqlalchemy',
        'flask',
        'requests',
        'six',
        'opentelemetry-instrumentation-sqlalchemy',
        'opentelemetry-instrumentation-flask',
        'opentelemetry-instrumentation-requests',
        'sentry_sdk'
    ],
)
