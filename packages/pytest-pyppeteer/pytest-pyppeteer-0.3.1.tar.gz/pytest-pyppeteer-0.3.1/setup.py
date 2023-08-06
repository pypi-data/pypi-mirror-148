# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_pyppeteer']

package_data = \
{'': ['*']}

install_requires = \
['cssselect>=1.1.0,<2.0.0',
 'lxml>=4.7.1,<5.0.0',
 'pyppeteer>=1.0.2,<2.0.0',
 'pytest>=6.2.5,<7.0.0']

entry_points = \
{'pytest11': ['pyppeteer = pytest_pyppeteer.plugin']}

setup_kwargs = {
    'name': 'pytest-pyppeteer',
    'version': '0.3.1',
    'description': 'A plugin to run pyppeteer in pytest',
    'long_description': '# pytest-pyppeteer\n\nA plugin to run [pyppeteer](https://github.com/pyppeteer/pyppeteer) in pytest.\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-pyppeteer)\n[![GitHub issues](https://img.shields.io/github/issues-raw/luizyao/pytest-pyppeteer)](https://github.com/luizyao/pytest-pyppeteer/issues)\n[![PyPI](https://img.shields.io/pypi/v/pytest-pyppeteer)](https://pypi.org/project/pytest-pyppeteer/)\n[![Downloads](https://pepy.tech/badge/pytest-pyppeteer)](https://pepy.tech/project/pytest-pyppeteer)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# Installation\n\nYou can install pytest-pyppeteer via [pip](https://pypi.org/project/pip/):\n\n```bash\n$ pip install pytest-pyppeteer\n```\n\nor install the latest one on Github:\n\n```bash\npip install git+https://github.com/luizyao/pytest-pyppeteer.git\n```\n\n# Quickstart\n\nFor example, **The Shawshank Redemption** deserves a 9.0 or higher rating on [douban.com](https://movie.douban.com).\n\n```python\nfrom dataclasses import dataclass\n\n\n@dataclass(init=False)\nclass Elements:\n    """Collect locators of page objects, no matter XPath or CSS Selector."""\n\n    # query input\n    query = "#inp-query"\n\n    # search button\n    apply = ".inp-btn > input:nth-child(1)"\n\n    # the first result\n    first_result = "#root > div > div > div > div > div:nth-child(1) > div.item-root a.cover-link"\n\n    # rating\n    rating = "#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong"\n\n\nasync def test_lifetimes(browser):\n    page = await browser.new_page()\n    await page.goto("https://movie.douban.com/")\n\n    await page.type(Elements.query, "The Shawshank Redemption")\n    await page.click(Elements.apply)\n\n    await page.waitfor(Elements.first_result)\n    await page.click(Elements.first_result)\n\n    await page.waitfor(Elements.rating)\n    rating = await page.get_value(Elements.rating)\n\n    assert float(rating) >= 9.0\n```\n\n![quickstart](images/quickstart.gif)\n\n# Usage\n\n## Fixtures\n\n### `browser` fixture\n\nProvide an `pyppeteer.browser.Browser` instance with a new method `new_page()`, like `pyppeteer.browser.Browser.newPage()`, `new_page()` could create a `pyppeteer.page.Page` instance.\n\nBut the `pyppeteer.page.Page` instance created by `new_page()` has some new methods:\n\n| Method        | Type     |\n| ------------- | -------- |\n| query_locator | New      |\n| waitfor       | New      |\n| click         | Override |\n| type          | Override |\n| get_value     | New      |\n\nFor example, you can query an element by css or xpath in the same method `query_locator` instead of original `querySelector` and `xpath`.\n\n> More details check with [page.py](src/pytest_pyppeteer/page.py) in the source code.\n\n### `browser_factory` fixture\n\nProvide to create an `pyppeteer.browser.Browser` instance.\n\nFor example, query the **The Shawshank Redemption**’s movie and book rating on [douban.com](https://movie.douban.com/) at the same time, then compare them.\n\n```python\nimport asyncio\nfrom dataclasses import dataclass\n\n\n@dataclass\nclass Elements:\n    query = "#inp-query"\n    apply = ".inp-btn > input:nth-child(1)"\n\n\n@dataclass\nclass BookElements(Elements):\n    url = "https://book.douban.com/"\n\n    result = \'(//*[@class="item-root"])[1]/a\'\n    rating = "#interest_sectl > div > div.rating_self.clearfix > strong"\n\n\n@dataclass\nclass MovieElements(Elements):\n    url = "https://movie.douban.com/"\n\n    result = "#root > div > div > div > div > div:nth-child(1) > div.item-root a.cover-link"\n    rating = "#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong"\n\n\nasync def query_rating(browser, name: str, elements: "Elements"):\n    page = await browser.new_page()\n\n    await page.goto(elements.url)\n\n    await page.type(elements.query, name)\n    await page.click(elements.apply)\n\n    await page.waitfor(elements.result)\n    await page.click(elements.result)\n\n    await page.waitfor(elements.rating)\n    rating = await page.get_value(elements.rating)\n    return rating\n\n\nasync def test_multiple_browsers(browser_factory):\n    browser1 = await browser_factory()\n    browser2 = await browser_factory()\n\n    movie_rating, book_rating = await asyncio.gather(\n        query_rating(browser1, "The Shawshank Redemption", MovieElements),\n        query_rating(browser2, "The Shawshank Redemption", BookElements),\n    )\n\n    assert movie_rating == book_rating\n```\n\n![multiple_browsers](images/multiple_browsers.gif)\n\n## Command line options\n\n### `--executable-path`\n\nYou can specify the Chromium or Chrome executable path. Otherwise I will use the default install path of Chrome in current platform.\n\nFor other platforms, pyppeteer will downloads the recent version of Chromium when called first time. If you don’t prefer this behavior, you can specify an exact path by override this fixture:\n\n```python\n@pytest.fixture(scope="session")\ndef executable_path(executable_path):\n    return executable_path or "path/to/Chrome/or/Chromium"\n```\n\n### `--headless`\n\nRun browser in headless mode.\n\n### `--args`\n\nAdditional args to pass to the browser instance.\n\nFor example, specify a proxy:\n\n```bash\n$ pytest --args proxy-server "localhost:5555,direct://" --args proxy-bypass-list "192.0.0.1/8;10.0.0.1/8"\n```\n\nOr by override the `args` fixture:\n\n```python\n@pytest.fixture(scope="session")\ndef args(args) -> List[str]:\n    return args + [\n        "--proxy-server=localhost:5555,direct://",\n        "--proxy-bypass-list=192.0.0.1/8;10.0.0.1/8",\n    ]\n```\n\n### `--window-size`\n\nThe default browser size is 800\\*600, you can use this option to change this behavior:\n\n```bash\n$ pytest --window-size 1200 800\n```\n\n`--window-size 0 0` means to starts the browser maximized.\n\n### `--slow`\n\nSlow down the pyppeteer operate in milliseconds. Defaults to `0.0`.\n\n## Markers\n\n### `options`\n\nYou can override some command line options in the specified test.\n\nFor example, auto-open a DevTools panel:\n\n```python\nimport asyncio\n\nimport pytest\n\n\n@pytest.mark.options(devtools=True)\nasync def test_marker(browser):\n    await browser.new_page()\n    await asyncio.sleep(2)\n```\n\n![options marker](images/options_marker.gif)\n\n# License\n\nDistributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, pytest-pyppeteer is free and open source software.\n\n# Issues\n\nIf you encounter any problems, please [file an issue](https://github.com/luizyao/pytest-pyppeteer/issues) along with a detailed description.\n',
    'author': 'Luiz Yao',
    'author_email': 'luizyao@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/luizyao/pytest-pyppeteer/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
