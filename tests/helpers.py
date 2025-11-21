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
