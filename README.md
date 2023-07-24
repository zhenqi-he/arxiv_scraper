# arxiv_scraper

This repo is developed based on the guide in the official Arxiv website [here](https://info.arxiv.org/help/api/user-manual.html)

Run the following code to start fetching paper published within start_date to end_date under the designed category.
```bash
python arxiv_scraper.py --start_date='2022-01-01' --end_date='2023-06-30' --category='cs.AI'
```

The available options for sub-category under computer science (cs) are under [cs_category.txt](cs_category.txt)

