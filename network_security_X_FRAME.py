import requests

def check_x_frame_options(url):
    potential_weaknesses=0
    try:
        # Attempt a HEAD request to avoid downloading the entire page
        try:
            response = requests.head(url, timeout=10)
            # Some servers might not handle HEAD well; fallback to GET if needed.
            if response.status_code >= 400:
                response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            response = requests.get(url, timeout=10)

        # Check for the X-Frame-Options header (headers are case-insensitive)
        x_frame_options = response.headers.get('X-Frame-Options')
        if x_frame_options:
            print(f"✅ {url}:\n\t X-Frame-Options header: {x_frame_options}\n")
           
        else:
            print(f"❌ {url}:\n\t X-Frame-Options header not found.\n")
            potential_weaknesses+=1
    except Exception as e:
        print(f"❌ Error checking {url}:\n\t {e}\n")
        potential_weaknesses+=1

    return potential_weaknesses

# Iterate over the list and check each URL
def checking_x_frame(urls):
    for url in urls:
        check_x_frame_options(url)
