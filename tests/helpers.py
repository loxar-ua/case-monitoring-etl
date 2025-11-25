import requests

from mimetypes import guess_type
from pathlib import Path

TEST_PATH = Path(__file__).resolve().parent
FIXTURE_PATH = TEST_PATH / "fixtures/"

URL_TO_FIXTURE_MAP = {
        "https://bihus.info/afdsfsdf": "bihus_info/block.html",
        "https://bihus.info/sitemap_index.xml": "bihus_info/sitemap_index.xml",
        "https://bihus.info/post-sitemap2.xml": "bihus_info/post-sitemap2.xml",
        "https://bihus.info/post-sitemap3.xml": "bihus_info/post-sitemap3.xml",
        "https://bihus.info/post-sitemap4.xml": "bihus_info/post-sitemap4.xml",

        "https://tyzhden.ua/wp-sitemap.xml":"Tyzhden/wp-sitemap.xml",
        "https://tyzhden.ua/wp-sitemap-posts-post-118.xml":"Tyzhden/wp-sitemap-posts-post-118.xml",
        "https://tyzhden.ua/wp-sitemap-posts-post-123.xml":"Tyzhden/wp-sitemap-posts-post-123.xml",
        "https://tyzhden.ua/wp-sitemap-posts-post-124.xml":"Tyzhden/wp-sitemap-posts-post-124.xml",


        "https://nashigroshi.org/sitemap.xml":"nashi_groshi/sitemap.xml",
        "https://nashigroshi.org/sitemap-pt-post-2025-10.xml":"nashi_groshi/sitemap-pt-post-2025-10.xml",
        "https://nashigroshi.org/sitemap-pt-post-2025-11.xml":"nashi_groshi/sitemap-pt-post-2025-11.xml",

        ("https://bihus.info/ne-bulo-ni-zvuku-ni-svystu-vidrazu-pidnyalas"
        "-velyka-pylyuka-potim-des-za-2-sekundy-posypalys-vikna-na-zhytomyrshhyni"
        "-rosijska-krylata-raketa-rozbyla-shkolu/"):
        ("bihus_info/https___bihus.info_ne-bulo-ni-zvuku-ni-svystu-vidrazu-pidnyalas"
         "-velyka-pylyuka-potim-des-za-2-sekundy-posypalys-vikna-na-zhytomyrshhyni"
         "-rosijska-krylata-raketa-rozbyla-shkolu_.html"),
        ("https://bihus.info/rosijski-vijskovi-na-sumshhyni-zahopyly-zhytlovyj" 
        "-budynok-a-potim-rozstrilyaly-jogo-iz-kulemeta/"):
        ("bihus_info/На Херсонщині ворог вбиває людей, нищить населені пункти, краде авто"
         " та використовує заборонені види озброєння проти цивільних - Bihus.Info.html"),


        "https://tyzhden.ua/svidchennia-1933-ho/":"Tyzhden/https_tyzhden.uasvidchennia-1933-ho.html",
        "https://tyzhden.ua/v-tyshi-lopotinnia-praporiv/":"Tyzhden/https_tyzhden.uav-tyshi-lopotinnia-praporiv.html",

        "https://nashigroshi.org/2025/11/03/enerhoatom-za-19-mil-yoniv-zastrakhuvav-nahliadovu-radu-na-vypadok-areshtiv/":
        "nashi_groshi/https_nashigroshi_org_2025_11_03_enerhoatom-za-19-mil-yoniv-zastrakhuvav-nahliadovu-radu-na-vypadok-areshtiv.html",

        "https://nashigroshi.org/2025/11/03/politsiia-upershe-zamovyla-broneshchyty-velmet-z-likhtariamy-odrazu-na-53-mil-yony/":
        "nashi_groshi/https_nashigroshi_org_2025_11_03_politsiia-upershe-zamovyla-broneshchyty-velmet-z-likhtariamy-odrazu-na-53-mil-yony.html",

        "https://antac.org.ua/sitemap_index.xml":
        "antac/sitemap_index.xml",
        "https://antac.org.ua/news-sitemap2.xml":
        "antac/news-sitemap2.xml",
        "https://antac.org.ua/news-sitemap3.xml":
        "antac/news-sitemap3.xml",
        "https://antac.org.ua/news/shans-dlia-realnoi-sudovoi-reformy-rada-pidtrymala-ochyshchennia-vyshchoi-rady-pravosuddia/":
        "antac/article.html",

        "https://www.chesno.org/sitemap.xml": "chesno/sitemap.xml",
        "https://www.chesno.org/sitemap-posts.xml": "chesno/posts.xml",
        "https://www.chesno.org/post/6645/": "chesno/article.html",

        "https://www.slovoidilo.ua/sitemap_index_uk.xml":"slovo_i_dilo/sitemap_index_uk.xml",
        "https://www.slovoidilo.ua/sitemap/monthly_2025-11_uk.xml":"slovo_i_dilo/monthly_2025-11_uk.xml",

        "https://www.slovoidilo.ua/2025/11/25/novyna/polityka/komandi-trampa-rozpochalasya-pryxovana-borotba-cherez-myrnyj-plan-shhodo-ukrayiny-zmi":
        "slovo_i_dilo/https_www_slovoidilo_ua_2025_11_25_novyna_polityka_komandi-trampa-rozpochalasya-pryxovanarotba-cherez-myrnyj-plan-shhodo-ukrayiny-zmi.html",
        "https://www.slovoidilo.ua/2025/11/25/novyna/polityka/sud-zalyshyv-vartoyu-fihurantku-spravy-midas-ustymenko":
        "slovo_i_dilo/https_www_slovoidilo_ua_2025_11_25_novyna_polityka_sud-zalyshyv-vartoyu-fihurantku-spravy-midas-ustymenko.html",

    }

def create_mock_response(url, *args, **kwargs):
    """
    This is our side_effect.
    It looks up the URL in our map and returns the
    corresponding fixture file, or a 404 if not found.
    """
    filename = URL_TO_FIXTURE_MAP.get(url)

    mock_response = requests.Response()
    mock_response.url = url
    mock_response.status_code = 200

    if filename:
        file_path = FIXTURE_PATH / filename

        with open(file_path, 'rb') as file:
            file_content = file.read()

        mock_response._content = file_content
        mock_response.headers['Content-Type'] = str(guess_type(str(file_path)))
    else:
        print(f'No fixture exists for this: {url}')
        mock_response._content = b''

    return mock_response
