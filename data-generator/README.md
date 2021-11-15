Data Generator

It Reads the data present in data folder

Assuming the format of CSV files agreed upon
Encoding as UTF-8


if you need you can define another location in config with key `location`

`interval` is the delay interval after which we can send the next message



Design :

Read Data => Fill Queue [ one pipeline]
Schedule  drain from Queue => DataSource [second pipeline]


Assuming Data-generator will read from file currently or any remote file system and fill Queue .
currently we have static data but same can be modified to read continuous data and fill app Queue.

Queue can be drained to data source with specified interval





* Note
I am dropping error columns for this MVP
