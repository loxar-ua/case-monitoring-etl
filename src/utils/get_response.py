import requests

import random
import time

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0 (compatible; PublicMonitorBot/1.0; +https://github.com/loxar-ua/.github)'
}

TIMEOUT = 30


def get_response(url: str) -> requests.Response | None:
    """This function is used to get the response from url
    with additional error handling for timeouts, problems with connections, http errors,
    blocking, etc."""

    response = None

    # To be not blocked we should have random delay
    delay = random.uniform(0.5, 1)
    time.sleep(delay)

    try:
        response = requests.get(
            url=url,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        content = response.text

        if "Cloudfare" in content or "Sorry, you have been blocked" in content:
            # TODO: log this
            response = None
            print(f"Request have been blocked for {url}")

    except requests.exceptions.Timeout as e:
        # TODO: log this
        print(f"Request timed out for {url}: {e}")

    except requests.exceptions.ConnectionError as e:
        # TODO: log this
        print(f"Connection error for {url}: {e}")

    except requests.exceptions.HTTPError as e:
        # TODO: log this
        print(f"Http error for {url}: {e}")

    except requests.exceptions.RequestException as e:
        # TODO: log this
        print(f"An unexpected error occurred for {url}: {e}")

    return response


