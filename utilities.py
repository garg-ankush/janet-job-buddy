import urllib.parse

def generate_job_search_link(keywords):
    base_url = "https://www.indeed.com/jobs"

    encoded_keywords = urllib.parse.quote(keywords)

    query_params = {
        "q": encoded_keywords,
    }

    search_url = base_url + "?" + urllib.parse.urlencode(query_params)

    return search_url

def main():
    print("Welcome to the Job Search Link Generator!")
    keywords = input("Enter job keywords: ")

    search_link = generate_job_search_link(keywords, location)
    print("Search Link: ", search_link)

if __name__ == '__main__':
    main()

