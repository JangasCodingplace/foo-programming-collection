# CSV Customer File Generator - Python simple Approach

This project is a data generator designed to work with the
[csv-customer-extractor](./../../csv-customer-extractor/README.md)
project. Its purpose is to generate CSV files in different sizes
that can be used for testing and experimentation with the
[csv-customer-extractor](./../../csv-customer-extractor/README.md)
project.


## Setup

The script uses Python 3.9. No library needs to be installed.


## Usage

To run the script, navigate to the directory where the script is 
located and execute the following command:
```bash
python customer_file_generator.py
```

By default, the script generates 100 different articles and customers 
with 10,000 rows for a one-year period between 2022-01-01 and 
2023-01-01. The output CSV file is saved in the output directory.

To customize the script's behavior, you can use the following 
command-line arguments:

- `--target`: the target directory for the generated CSV file. 
  **default**: `./output`
- `--article-count`: the number of different article numbers that get 
  generated. **default** `100`.
- `--customer-count`: the number of different customers that get 
  generated. **default** `100`.
- `--min-date`: the minimum date for order generation. Should have the
  format YYYY-mm-dd. **default** `2022-01-01`.
- `--max-date`: the maximum date for order generation. Should have the
   format YYYY-mm-dd. **default** `2023-01-01`.
- `--row-count`: the row count for order generation. 
  **default** `10.000`.

For example, to generate 50,000 rows of customer orders for a two-year
period between 2021-01-01 and 2023-01-01, and save the output file in
the my_output directory, you can use the following command:

```bash
python customer_file_generator.py \
  --target my_output \
  --min-date 2021-01-01 \
  --max-date 2023-01-01 \
  --row-count 50000
```

## Output
The script generates a CSV file with the following columns:

- `CustomerId`: the ID of the customer who placed the order.
- `ArticleId`: the ID of the article that was ordered.
- `OrderId`: the ID of the order.
- `Timestamp`: the timestamp of the order in seconds since the epoch.

The CSV file is saved in the directory specified by the 
`--target command-line` argument. The file is named 
`customer-orders.csv`.
