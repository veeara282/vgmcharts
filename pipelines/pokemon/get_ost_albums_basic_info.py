'''
Download the list of English OST releases from Bulbapedia and transform it into a usable CSV file.

Steps:

1. Extract
    - Download page wikitext from API endpoint: https://bulbapedia.bulbagarden.net/w/api.php?action=expandtemplates&text={{:List_of_Pok%C3%A9mon_music_CDs}}&prop=wikitext&format=json
    - Parse JSON and extract value from `$.expandtemplates.wikitext` (JSONPath)
    - Parse the table of English releases (it's actually a nested table, so parse the inner table - the syntax is simple)
    Note: for now, we won't parse the Japanese release table

The result should look like:

|-
| May 9, 2000
| ''[[Pokémon the First Movie (score)|Pokémon the First Movie]]''
| Score for ''[[M01|Mewtwo Strikes Back]]'' and ''[[PK01|Pikachu's Vacation]]''

2. Transform

We turn 3 columns into 4.

release_date: 2000-05-09
release_title: Pokémon the First Movie
bp_page_title: Pokémon the First Movie (score)
short_description: Score for ''[[M01|Mewtwo Strikes Back]]'' and ''[[PK01|Pikachu's Vacation]]''

3. Load

Output to CSV file (for now) or database (once set up).

'''

from bulba_utils import bp_wikitext_url


def extract():
    ost_list_page_title = "List of Pokémon music CDs"
    api_url = bp_wikitext_url(ost_list_page_title)
    # Stub: just print the URL for now
    print(api_url)


def main() -> None:
    extract()


if __name__ == "__main__":
    main()
