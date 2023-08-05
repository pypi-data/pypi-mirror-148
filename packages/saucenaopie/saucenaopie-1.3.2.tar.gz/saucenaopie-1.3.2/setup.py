# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saucenaopie', 'saucenaopie.client', 'saucenaopie.types']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'saucenaopie',
    'version': '1.3.2',
    'description': 'Modern and easy-to-use Python implementation for the SauceNao API, with Pydantic and full asyncio support.',
    'long_description': '# SauceNaoPie\n\n[![GitHub](https://img.shields.io/github/license/WhiteMemory99/saucenaopie)](https://github.com/WhiteMemory99/saucenaopie/blob/main/LICENSE)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/saucenaopie)](https://pypi.org/project/saucenaopie/)\n\nModern and easy-to-use Python implementation for the **SauceNao API**, with Pydantic and full\nasyncio support, inspired by [PySauceNao](https://github.com/FujiMakoto/pysaucenao).\n\n* [Installation](#installation)\n* [Overview](#overview)\n* [Writing your first code](#writing-your-first-code)\n* [Advanced usage](#advanced-usage)\n* [Error handling](#error-handling)\n\n## Installation\n\n**[Python 3.8](https://www.python.org)** or above is required.\n\n```\n$ pip install saucenaopie\n```\n\n## Overview\n\nI think you all know that the SauceNao API leaves very much to be desired.  \nEven so, I tried to make this wrapper as user-friendly as I could. As for benefits:\n\n* Thanks to Pydantic and some serious work on type checking, you can get the fullest, safest and\n  the most precise code completion possible in IDEs. The library is also well-documented.\n* The SauceNao results have been divided into 5 types to make it easier to use - TwitterSauce,\n  BooruSauce, VideoSauce, MangaSauce and ArtSauce. Each one has slightly different fields.\n* Built-in methods to filter results as you see fit. More in [advanced usage](#advanced-usage).\n* Results are sorted by similarity before they are given to you.\n* Searching supports BytesIO objects, file paths and URLs.\n* Almost every SauceNao error is handled and represented.\n* The SauceNao DB indexes are fully represented in this library as a helpful object. Thanks to\n  that, you can see, get, and use any SauceNao index with ease, and do stuff like getting the index\n  name by its ID, getting indexes by a certain result type or all the available indexes altogether.\n  Read more\n  in [the sources](https://github.com/WhiteMemory99/saucenaopie/tree/main/saucenaopie/helper.py).\n\n## Writing your first code\n\nBoth async and sync clients are equally supported and well-made.\n\n<details>\n  <summary>Sync client</summary>\n\n```python\nfrom saucenaopie import SauceNao\n\n\ndef main():\n    client = SauceNao(api_key="api_key")\n    sauce = client.search(  # Also, you can pass BytesIO or a file path\n        "http://img10.joyreactor.cc/pics/post/full/iren-lovel-Anime-Art-artist-AO-6216329.jpeg",\n        from_url=True\n    )\n    for result in sauce.results:\n        print(result.data.first_url)  # Quickly get the first url from the result, can be None\n        print(f"{result.index.name} - {result.similarity:.1f}%")\n        \n    client.close()  # Close the connection\n\n\nif __name__ == "__main__":\n    main()\n```\n\n</details>\n<details>\n  <summary>Async client</summary>\n\n```python\nimport asyncio\nfrom saucenaopie import AsyncSauceNao\n\n\nasync def main():\n    client = AsyncSauceNao(api_key="api_key")\n    sauce = await client.search(  # Also, you can pass BytesIO or a file path\n        "http://img10.joyreactor.cc/pics/post/full/iren-lovel-Anime-Art-artist-AO-6216329.jpeg",\n        from_url=True\n    )\n    for result in sauce.results:\n        print(result.data.first_url)  # Quickly get the first url from the result, can be None\n        print(f"{result.index.name} - {result.similarity:.1f}%")\n        \n    await client.close()  # Close the connection\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n</details>\n\nTo learn more, you can either scroll down to the advanced usage section or see\nthe [examples folder](https://github.com/WhiteMemory99/saucenaopie/tree/main/examples) to look at\nreal-life examples.\n\n## Advanced usage\n\nNow let\'s pretend that we did a search.\n\n```python\ndef main():\n    client = SauceNao(api_key="api_key")\n    sauce = await client.search("path_to_the_file")\n```\n\nIf the search was successful, we get a SauceResponse object that contains 3 fields:\n\n* `header` - information about the current query, such as the minimum result similarity and total\n  number of results.\n* `account_info` - information about your SauceNao account, like your current limits, account type\n  and user_id.\n* `results` - a list of results, each result has source data that can be one of 5 types, result\n  similarity percent, index object and thumbnail.\n\nLet\'s find out how we can filter our results to make the library give us some specific data. We\'ll\nlook for Pixiv results.\n\n```python\nfrom saucenaopie.helper import SauceIndex\nfrom saucenaopie.types.sauce import ArtSauce  # just for reference\n\n\n...\nfor result in sauce.filter_results_by_index(SauceIndex.PIXIV):\n    # Every result 100% belongs to Pixiv (ArtSauce type)\n    print(f"{result.data.first_url} - {result.similarity:.1f}%")\n\n# And another way to do the same thing\nfor result in sauce.results:  # or sauce.filter_results_by_type(ArtSauce)\n    if result.index.id == SauceIndex.PIXIV:\n        print(f"Pixiv result: {result.data.first_url} - {result.similarity:.1f}%")\n```\n\nBy default, saucenaopie sorts results by similarity, but it does not filter unlikely ones that have\nlow similarity. To learn the way to do that along with some bonuses, look at the example below.\n\n```python\n...\nfrom saucenaopie.types.sauce import MangaSauce\n\n\n...\nfor result in sauce.get_likely_results():  # Only results with good similarity\n    print(\n        f"{result.index} or {result.index.clean_name} is a human readable index title, like Pixiv.")\n    if result.index.id in SauceIndex.get_manga_indexes():\n        print("This result belongs to a manga source, like MangaDex.")\n    if isinstance(result.data, MangaSauce):\n        print("This result belongs to a manga source x2.")\n```\n\nAt this point you should have a good idea on how you can filter the results.  \nNext we\'ll discuss more complex searching queries.\n\n```python\nclient.search(\n    "path_to_the_file",\n    result_limit=5,\n    # You can limit results, 8 by default.\n    # Just note that SauceNao DOES NOT \n    # sort the results by similarity before sending them to you.\n    # In other words, you might get the worst possible garbage.\n    index=SauceIndex.ALL,\n    # We can provide a specific index to search from.\n    # By default, all of them are in use.\n    max_index=SauceIndex.YANDERE,  # NOTE: Broken by now\n    # Yandere is 11th in the index list, this will EXCLUDE all the indexes that are higher.\n    min_index=SauceIndex.DOUJINSHI_DB,  # NOTE: Broken by now\n    # The same principle as above, just vice versa.\n)\n```\n\nThat\'s all. If you still have questions, you can browse the library source code or use your IDE\ncapabilities.  \nDon\'t forget to handle exceptions. By the way, this leads us to the last topic - **error handling**.\n\n## Error handling\n\nAll the SauceNao exceptions are inherited from SauceNaoError, so you can use this whenever you just\nwant to catch everything. For other exceptions,\nsee [this file](https://github.com/WhiteMemory99/saucenaopie/tree/main/saucenaopie/exceptions.py).  \nYou should also know that some exceptions contain additional helpful data:\n\n```python\nfrom saucenaopie import SauceNao\nfrom saucenaopie.exceptions import LimitReached\n\n\ndef main():\n    client = SauceNao(api_key="api_key")\n\n    try:\n        client.search("...")\n    except LimitReached as ex:\n        # Free account has 8 requests per 30 sec and 200 per 24 hours\n        print(f"Daily requests left: {ex.long_remaining}.")\n        print(f"30 second requests left: {ex.short_remaining}.")\n```',
    'author': 'WhiteMemory99',
    'author_email': 'lisen1510@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WhiteMemory99/saucenaopie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
