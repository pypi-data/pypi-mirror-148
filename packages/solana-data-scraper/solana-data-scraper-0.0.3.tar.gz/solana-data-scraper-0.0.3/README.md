# Scrape Solana Blockchain Data

This python library scrapes blockchain from https://bitquery.io/ from their GraphQL endpoints.

This requires you to supply your own Bitquery API token.

# Setup

1. Create an account at https://bitquery.io/
2. Retrieve API Key
3. `export BITQUERY_API_KEY=XXXXXXX`

# Functionalities

- Queries Bitquery for blockchain data
- Batches queries to get around compute limits.
- Returns output as a pandas dataframe or saves data to a csv
