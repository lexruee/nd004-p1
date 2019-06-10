#!/usr/bin/env python

import psycopg2


class Repository(object):
    """ The Repository class is used to retrieve data from the database. """

    def __init__(self, connection):
        self._connection = connection

    def get_popular_articles(self, limit=3):
        """ Returns the most popular articles of all time. """

        sql_stmt = 'select title, views from popular_articles limit %s;'
        with self._connection.cursor() as cursor:
            cursor.execute(sql_stmt, (limit,))
            results = cursor.fetchall()
        return results or []

    def get_popular_authors(self):
        """ Returns the most popular authors of all time. """

        sql_stmt = 'select name, views from popular_authors;'
        with self._connection.cursor() as cursor:
            cursor.execute(sql_stmt)
            results = cursor.fetchall()
        return results or []

    def get_request_percent_errors_per_day(self):
        """ Returns the request percent errors per day. """

        sql_stmt = """
            select day, percent_error from request_percent_errors_per_day
                where percent_error > %s order by percent_error desc;
        """
        lower_percent_error_limit = 1.0
        with self._connection.cursor() as cursor:
            cursor.execute(sql_stmt, (lower_percent_error_limit,))
            results = [(day, self._format_error(error))
                       for day, error in cursor.fetchall()]
        return results or []

    def _format_error(self, percent_error):
        return float("{0:.2f}".format(percent_error))


class Report(object):
    """ The Report class is used to report the results. """

    def __init__(self, repository):
        self._repository = repository

    def show(self):
        """ Shows the results to the questions of the project description. """

        self.show_popular_articles()
        self.show_newline()
        self.show_newline()
        self.show_popular_authors()
        self.show_newline()
        self.show_newline()
        self.show_request_percent_errors()

    def show_popular_articles(self):
        print('What are the most popular three articles of all time?\n')

        articles = self._repository.get_popular_articles()
        for output_string in self._create_output(articles, '', 'views'):
            print(output_string)

    def show_popular_authors(self):
        print('Who are the most popular article authors of all time?\n')

        authors = self._repository.get_popular_authors()
        for output_string in self._create_output(authors, '', 'views'):
            print(output_string)

    def show_request_percent_errors(self):
        print('On which days did more than 1% of requests lead to errors?\n')

        errors = self._repository.get_request_percent_errors_per_day()
        for output_string in self._create_output(errors, '%', 'errors'):
            print(output_string)

    def show_newline(self):
        print('')

    def _create_output(self, items, unit, name):
        return [self._format(title, count, unit, name)
                for title, count in items]

    def _format(self, title, count, count_unit, count_name):
        return '{} - {}{} {}'.format(title, count, count_unit, count_name)


def main():
    connection = psycopg2.connect(dbname='news')
    repository = Repository(connection)
    report = Report(repository)
    report.show()


if __name__ == '__main__':
    main()
