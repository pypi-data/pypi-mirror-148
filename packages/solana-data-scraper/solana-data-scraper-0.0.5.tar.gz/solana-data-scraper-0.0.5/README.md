# Scrape Solana Blockchain Data

This python library scrapes blockchain from https://bitquery.io/ from their GraphQL endpoints.

This requires you to supply your own Bitquery API token.

Copyright (c) 2022 Friktion Labs

# Setup

1. `pip3 install solquery`
2. Create an account at https://bitquery.io/
3. Retrieve API Key
4. In command line, `export BITQUERY_API_KEY=XXXXXXX`
5. `python3 solquery/example_query.py`

# Functionalities

- Queries Bitquery for blockchain data
- Batches queries to get around compute limits
- Returns output as a pandas dataframe or saves data to a specified csv
