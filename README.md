# Log Analysis Project

## Task

The task of this project is to create a Python-based reporting tool.
The latter prints out reports based on the data in the postgres database.
For accessing the postges database the handy module `psycopg2` is used.

The main goal of the reporting tool is to produce output that helps us to answer the following three questions:

 * What are the most popular three articles of all time?
 * Who are the most popular article authors of all time?
 * On which days did more than 1% of requests lead to errors?


## Installation

1) Git clone this repo using the command below:

``` 
git clone https://github.com/lexruee/nd004-p1
```

Please note that this repository contains an adjusted version of the Vagrantfile from Udacity to run the reporting tool.
The original file can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip).

2) Change into the directory `nd004-p1`

3) Download the `newsdata` database and unzip it using the commands below:

```
curl -L -o newsdata.zip https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
unzip newsdata.zip
```

4) Run `vagrant up` to download and start the Vagrant VM for this repository.
This command also creates the `news` database.

5) Next, run `vagrant ssh` to ssh into the VM.

6) Once inside the VM, run the following command to populate the database with the news data:

```
psql news -f /vagrant/newsdata.sql
```


7) Lastly, create the views listed in section `View code` by running the following command:

```
psql news -f /vagrant/reporting_tool/views.sql
```

## Running the reporting tool

1) Inside the VM, use the command `python /vagrant/reporting_tool/app.py` to run 
the reporting tool to answer the three questions of the task description.

2) Once finished, the program should haved produced the same output
as the one in the file `output.txt`.

3) Finnaly, leave the VM and shut it down using `vagrant halt`.


## View code

The following views were created to simplify the SQL queries and to keep the python code as simple as possible. 
See file `reposting_tool/views.sql`.

The listing below contains the necessary code to create the views:

```
create view popular_articles as
	select articles.title, count(articles.title) as views 
		from articles inner join log 
			on ('/article/'|| articles.slug) = log.path 
				group by articles.title
					order by views desc;

create view popular_authors as
	select authors.name, count(authors.name) as views 
		from articles, authors, log 
			where articles.author = authors.id 
				and ('/article/'|| articles.slug) = log.path 
					group by authors.name
						order by views desc;

create view requests_per_day as
	select to_char(time,'FMMonth DD, YYYY') as day, count(*) as requests 
		from log group by to_char(time,'FMMonth DD, YYYY');

create view request_errors_per_day as 
	select to_char(time,'FMMonth DD, YYYY') as day, count(status) as errors 
		from log where status <> '200 OK' 
			group by to_char(time,'FMMonth DD, YYYY');

create view request_percent_errors_per_day as
	select request_errors_per_day.day, requests, errors, (100.0 * errors/requests) as percent_error
		from request_errors_per_day, requests_per_day 
			where request_errors_per_day.day = requests_per_day.day;
```

