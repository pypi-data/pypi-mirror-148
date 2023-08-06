cobrseo
=======

.. image:: https://img.shields.io/badge/pypi-v0.0.1-blue
    :target: https://test.pypi.org/project/cobrseo/
        :alt: Latest version

How to install
--------------

::

    pip install -i https://test.pypi.org/simple/ cobrseo==0.0.1

Package structure 
-----------------

::

   cobrseo
   └───json
   │   └───serp_processing
   │        │   read_json()
   │        │   get_keyword()
   │        │   get_urls_by_item_type()
   │        │   get_organic_info()
   │        │   get_related_searches()
   │        │   get_people_also_ask()
   │   
   └───crawler
   │   └───crawler3k
   │        │   crawl_article()
   │        │   get_content_from_urls()
   |
   └───api
       └───dataforseo_organic
            │   save_dataforseo_organic_serps()


A Glance:
=========

SERP PROCESSING:
----------------

Get organic items with the most important information:

.. code-block:: pycon

   >>> from cobrseo.json.serp_processing import get_organic_info
   >>> json_path = './007b1216b666d5dbe4b1b00a3b760eb4.json'

   >>> get_organic_info(json_path)
   {0: {'domain': 'usa.kaspersky.com', 'title': 'Your mobile security & privacy covered - Kaspersky', 'url': 'https://usa.kaspersky.com/android-security', 'description': 'Antivirus. Protects you from viruses and malware on your Android devices by detecting, isolating and removing threats · Automatic scan. Continuously scans for\xa0...', 'date': None}, 
   1: {'domain': 'play.google.com', 'title': 'Kaspersky Security & VPN - Apps on Google Play', 'url': 'https://play.google.com/store/apps/details?id=com.kms.free&hl=en_US&gl=US', 'description': 'Free antivirus and phone security for Android™ devices from Kaspersky Kaspersky Security & VPN for Android is a FREE-to-download antivirus solution that\xa0...', 'date': None}, 
   2: {'domain': 'www.tomsguide.com', 'title': "Kaspersky Mobile Antivirus Review: Short on Features - Tom's ...", 'url': 'https://www.tomsguide.com/reviews/kaspersky-mobile-security', 'description': 'Kaspersky has one of the most complete sets of free anti-theft tools. As a freemium antivirus app, Kaspersky gives you the same antivirus engine\xa0...', 'date': '2019-10-25 00:00:00 +00:00'}, 
   3: {'domain': 'kaspersky-mobile-security.en.uptodown.com', 'title': 'Kaspersky Mobile Security for Android - Download the APK ...', 'url': 'https://kaspersky-mobile-security.en.uptodown.com/android', 'description': 'Kaspersky Mobile Security is a security tool for smartphones that goes much further than a simple antivirus, offering absolutely everything that an Android\xa0...', 'date': None}, 
   4: {'domain': 'apps.apple.com', 'title': 'Kaspersky Security & VPN on the App Store', 'url': 'https://apps.apple.com/us/app/kaspersky-security-vpn/id1089969624', 'description': 'Kaspersky Security & VPN includes premium apps & features designed to work beautifully on your iPhones and iPads. From security essentials\xa0...', 'date': '2022-03-31 00:00:00 +00:00'}, 
   5: {'domain': 'www.safetydetectives.com', 'title': 'Kaspersky Antivirus Review — Is It Safe to Use in 2022?', 'url': 'https://www.safetydetectives.com/best-antivirus/kaspersky/', 'description': 'That said, I still think Kaspersky Total Security is a good internet security suite overall. It has a high-quality antivirus scanner,\xa0...', 'date': None}, 
   6: {'domain': 'ltonlinestore.com', 'title': '1 Device, 1 Year, Kaspersky internet Security, For Android', 'url': 'https://ltonlinestore.com/1-Device-1-Year-Kaspersky-internet-Security-For-Android-p73383495', 'description': 'Mobile protection for your mobile life · Premium protection against mobile malware · Immediate response to new threats · Detection of fraudulent and malicious\xa0...', 'date': None}, 
   7: {'domain': 'www.pcmag.com', 'title': 'The Best Android Antivirus Apps for 2022 | PCMag', 'url': 'https://www.pcmag.com/picks/the-best-android-antivirus-apps', 'description': 'Kaspersky Internet Security includes a comprehensive Android security suite. It scans for malware on demand and in real time, and keeps you from visiting\xa0...', 'date': None}}


Get all organic urls. You can specify domains, that should not be included:

- by default ``url_stoplist=['google.com','facebook.com','instagram.com']``
- Available item types: ``'organic'`` and ``'news_search'``

.. code-block:: pycon

   >>> from cobrseo.json.serp_processing import get_urls_by_item_type
   >>> get_urls_by_item_type(json_path, 'organic')
   ['https://usa.kaspersky.com/android-security', 
   'https://www.tomsguide.com/reviews/kaspersky-mobile-security', 
   'https://kaspersky-mobile-security.en.uptodown.com/android', 
   'https://apps.apple.com/us/app/kaspersky-security-vpn/id1089969624', 
   'https://www.safetydetectives.com/best-antivirus/kaspersky/', 
   'https://ltonlinestore.com/1-Device-1-Year-Kaspersky-internet-Security-For-Android-p73383495', 
   'https://www.pcmag.com/picks/the-best-android-antivirus-apps']

   >>> get_urls_by_item_type(json_path, 'organic', url_stoplist=['kaspersky.com'])
   ['https://play.google.com/store/apps/details?id=com.kms.free&hl=en_US&gl=US', 
   'https://www.tomsguide.com/reviews/kaspersky-mobile-security', 
   'https://kaspersky-mobile-security.en.uptodown.com/android', 
   'https://apps.apple.com/us/app/kaspersky-security-vpn/id1089969624',
   'https://www.safetydetectives.com/best-antivirus/kaspersky/', 
   'https://ltonlinestore.com/1-Device-1-Year-Kaspersky-internet-Security-For-Android-p73383495', 
   'https://www.pcmag.com/picks/the-best-android-antivirus-apps']



Get keyword from json-serp:

.. code-block:: pycon

   >>> from cobrseo.json.serp_processing import get_keyword
   >>> get_keyword(json_path)
   'kaspersky mobile antivirus'


Get related searches:

.. code-block:: pycon

   >>> from cobrseo.json.serp_processing import get_related_searches
   >>> get_related_searches(json_path)
   ['kaspersky mobile antivirus free', 
   'kaspersky mobile antivirus cracked apk', 
   'kaspersky mobile antivirus apk', 
   'kaspersky mobile security android', 
   'kaspersky mobile antivirus download', 
   'kaspersky mobile security activation key',
   'kaspersky free antivirus', 
   'kaspersky mobile antivirus review']
 
Get people aslo ask:

.. code-block:: pycon

   >>> from cobrseo.json.serp_processing import get_people_also_ask
   >>> get_people_also_ask(json_path)
   {'questions': ['Is Kaspersky antivirus good for mobile?', 'Is Kaspersky free for mobile?', 'Which antivirus is best for mobile?', 'Do I need Kaspersky on my Android?'], 
   'urls': ['https://www.pcmag.com/reviews/kaspersky-internet-security-for-android', 'https://www.safetydetectives.com/blog/best-really-free-antivirus-programs-for-android/', 'https://www.tomsguide.com/best-picks/best-android-antivirus', 'https://support.kaspersky.com/consumer/products/Kaspersky_Internet_Security_for_Android'], 
   'descriptions': ["The Bottom Line. Kaspersky Internet Security offers Android users top-tier malware protection, great anti-phishing protection, and tools to secure and recover lost and stolen phones. But some features didn't work as advertised in our hands-on testing. Sep 30, 2015", "Kaspersky Security Free — Easy to Use with Decent On-Demand Virus Scanning. Kaspersky Security Free is a decent free internet security app for Android users — and because it only provides a couple of free features, it's very easy to use.", 'Bitdefender Mobile Security. Best paid option. ...\nNorton Mobile Security. Specifications. ...\nAvast Mobile Security. Specifications. ...\nKaspersky Mobile Antivirus. Specifications. ...\nLookout Security & Antivirus. Specifications. ...\nMcAfee Mobile Security. Specifications. ...\nGoogle Play Protect. Specifications.', 'Kaspersky Internet Security for Android provides comprehensive protection for your mobile devices. Along with providing protection against viruses and other malware, the app protects your internet connection, the data on your device, access to other apps, and also allows you to block unwanted calls.']}





CRAWLER
-------

Crawling list of urls:

.. code-block:: pycon

   def get_content_from_urls(urls: List[str], lang: List[str]=['en'],  words_limit: tuple=(0,10000), json_path: str='file') -> List[str]

    """Advanced crawler. 

    Returns the list of content from crawled urls.

    Args:
        urls (List[str]): Urls to be crawled.
        lang (List[str]): Selected languages.
        words_limit (tuple): Minimum and maximum word limit for article length.
        json_path (str): Name of json file with SERP for logging purpose.

    Returns:
        list: List of crawled urls.
    """


.. code-block:: pycon

   >>> from cobrseo.crawler.crawler3k import get_content_from_urls
   >>> urls = ['https://www.pcmag.com/reviews/kaspersky-internet-security-for-android', 
   'https://www.safetydetectives.com/blog/best-really-free-antivirus-programs-for-android/', 
   'https://www.tomsguide.com/best-picks/best-android-antivirus', 
   'https://support.kaspersky.com/consumer/products/Kaspersky_Internet_Security_for_Android']

   >>> len(get_content_from_urls(urls))
   4



API
---

.. code-block:: pycon

   >>> from cobrseo.api.dataforseo_organic import save_dataforseo_organic_serps
   >>> keywords = ['Industroyer', 'blackcat', 'revil', 'Moncler', 'Conti ransomware']
   >>> destination_path = './serps'
   >>> check_kw_paths = ['./serps']
   >>> token = 'API_KEY'

   >>> save_dataforseo_organic_serps(
			keywords, 
			destination_path,
			check_kw_paths,
			token
		)
   [{'keyword': 'revil', 'path': './serps/d1c0dd7a20099294bfe3dba2c0b4e507.json'},
   {'keyword': 'blackcat', 'path': './serps/5c55d71b4c47d141072cf0540c046d07.json'},
   {'keyword': 'Industroyer', 'path': './serps/492ed356c6aa5e4bd9de4a81b4fa2add.json'},
   {'keyword': 'Conti ransomware', 'path': './serps/6ba632a49d9e504bad1fde6f9281a2db.json'},
   {'keyword': 'Moncler', 'path': './serps/faf6dd008e4b7640583c95e1cbbf1533.json'}]

