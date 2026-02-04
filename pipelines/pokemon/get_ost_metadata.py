'''
Steps:

1. Extract
    - Download page wikitext from API endpoint: https://bulbapedia.bulbagarden.net/w/api.php?action=expandtemplates&text={{:List_of_Pok%C3%A9mon_music_CDs}}&prop=wikitext&format=json
    - Parse JSON and extract value from `$.expandtemplates.wikitext` (JSONPath)
    - Parse table (it's actually a nested table, so parse the inner table - the syntax is simple)

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


def main() -> None:
    pass


if __name__ == "__main__":
    main()
