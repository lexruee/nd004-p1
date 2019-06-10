import pytest
import psycopg2
from decimal import Decimal
from reporting_tool import app

@pytest.fixture
def postgres_connection():
	return psycopg2.connect(dbname='news')

@pytest.fixture
def repository(postgres_connection):
	return app.Repository(postgres_connection)

def test_create_repository(postgres_connection):
	repository = app.Repository(postgres_connection)
	assert repository

def test_get_popular_articles(repository):
	expected_articles = [
		('Candidate is jerk, alleges rival', 338647L),
		('Bears love berries, alleges bear', 253801L),
		('Bad things gone, say good people', 170098L)
	]

	articles = repository.get_popular_articles(limit=3)
	assert type(articles) is list
	assert articles == expected_articles

def test_get_popular_authors(repository):
	expected_authors = 	[
		('Ursula La Multa', 507594L),
		('Rudolf von Treppenwitz', 423457L),
		('Anonymous Contributor', 170098L),
		('Markoff Chaney', 84557L)
	]

	authors = repository.get_popular_authors()
	assert type(authors) is list
	assert authors == expected_authors

def test_get_request_percent_errors_per_day(repository):
	expected_error_rates = 	[
		 ('July 17, 2016', 2.26),
	]

	error_rates = repository.get_request_percent_errors_per_day()
	assert type(error_rates) is list
	assert error_rates == expected_error_rates
