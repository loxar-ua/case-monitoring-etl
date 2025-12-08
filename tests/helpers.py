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

        "https://tyzhden.ua/wp-sitemap.xml":"tyzhden/wp-sitemap.xml",
        "https://tyzhden.ua/wp-sitemap-posts-post-118.xml":"tyzhden/wp-sitemap-posts-post-118.xml",
        "https://tyzhden.ua/wp-sitemap-posts-post-123.xml":"tyzhden/wp-sitemap-posts-post-123.xml",
        "https://tyzhden.ua/wp-sitemap-posts-post-124.xml":"tyzhden/wp-sitemap-posts-post-124.xml",
        "https://tyzhden.ua/svidchennia-1933-ho/":"tyzhden/https_tyzhden.uasvidchennia-1933-ho.html",
        "https://tyzhden.ua/v-tyshi-lopotinnia-praporiv/":"tyzhden/https_tyzhden.uav-tyshi-lopotinnia-praporiv.html",

        "https://nashigroshi.org/sitemap.xml": "nashi_groshi/sitemap.xml",
        "https://nashigroshi.org/sitemap-pt-post-2025-10.xml": "nashi_groshi/sitemap-pt-post-2025-10.xml",
        "https://nashigroshi.org/sitemap-pt-post-2025-11.xml": "nashi_groshi/sitemap-pt-post-2025-11.xml",
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

        "https://texty.org.ua/sitemap.xml":
        "texty/sitemap.xml",
        "https://texty.org.ua/sitemap-articles.xml":
        "texty/articles.xml",
        "https://texty.org.ua/articles/116355/korupcijni-nebesa-hrushevskoho-9a-istoriya-skandalnoho-budivnyctva-j-meshkanciv/":
        "texty/article.html",


        "https://www.pravda.com.ua/sitemap/sitemap-archive.xml":
        "pravda/www_pravda_com_ua_sitemap_sitemap-archive.xml",
        "https://www.pravda.com.ua/sitemap/sitemap-2025-12.xml.gz":
        "pravda/https_www_pravda_com_ua_sitemap_sitemap-2025-12.xml.gz",
       "https://www.pravda.com.ua/news/2025/12/01/8009697/":
        "pravda/https_www_pravda_com_uanews202512018009697.html",
        "https://www.pravda.com.ua/news/2025/12/01/8009694/":
        "pravda/https_www_pravda_com_uanews202512018009694.html",


        'https://hromadske.ua/sitemap.xml':
        "hromadske/sitemap.xml",
        'https://hromadske.ua/sitemaps/posts/2025/12.xml':
        'hromadske/https_hromadske_ua_sitemaps_posts_2025_12.xml',
        "https://hromadske.ua/svit/255883-v-universyteti-ssha-ziavytsia-tsilyy-kurs-pro-muzychnu-karyeru-k-pop-artysta":
        "hromadske/https_hromadske_ua_svit_255883-v-universyteti-ssha-ziavytsia-tsilyy-kurs-pro-muzychnu-karyeru-k-pop-artysta.html",


        "https://babel.ua/sitemap_full.xml":
        "babel/sitemap_full.xml",
        "https://babel.ua/ukrainian/default/2025/11-12-11-26.xml":
        "babel/11-12-11-26.xml",
        "https://babel.ua/news/122971-turechchina-pidtverdila-zagibel-20-viyskovih-pid-chas-avariji-litaka-c-130":
        "babel/122971-turechchina-pidtverdila-zagibel-20-viyskovih-pid-chas-avariji-litaka-c-130.html",

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
        mock_response._content = b''

    return mock_response
