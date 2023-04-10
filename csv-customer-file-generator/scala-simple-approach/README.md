# CSV Customer File Generator - Python simple Approach

This project is a data generator designed to work with the
[csv-customer-extractor](./../../csv-customer-extractor/README.md)
project. Its purpose is to generate CSV files in different sizes
that can be used for testing and experimentation with the
[csv-customer-extractor](./../../csv-customer-extractor/README.md)
project.

## Facts

This project includes mixture of imperative and functional Codestyle.

While 100k Rows can be generated < 10 seconds, it's a problem to
generate more than 1 Million rows. Funfact: This isn't a problem in
the [python-simple-approach](./../python-simple-approach) Project.

## Requirements
- Scala 2.13.10
- sbt 1.8.2

This project has no extra dependencies to other projects or libraries.


## Output
By default, the script generates 100 different articles and 10000
customers with 100.000 rows for a one-year period between 2022-01-01
and 2023-01-01. The output CSV file is saved in the `./output/`
directory.

The script generates a CSV file with the following columns:

- `CustomerId`: the ID of the customer who placed the order.
- `ArticleId`: the ID of the article that was ordered.
- `OrderId`: the ID of the order.
- `Timestamp`: the timestamp of the order in seconds since the epoch.
