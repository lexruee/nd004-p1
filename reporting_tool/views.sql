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