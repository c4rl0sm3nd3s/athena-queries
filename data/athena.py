import config
from pandas.core.frame import DataFrame
from data.query_athena import QueryAthena

class Athena:

    def __init__(self):
        pass


    def get_query_executed(self) -> DataFrame:


        query = "SELECT * "
        query += 'FROM "%s"."%s" ' % (config.athena_db, config.athena_table)
        #add conditions WHERE GROUP ORDER etc

        query_athena = QueryAthena(query)

        res = query_athena.run_query()

        return res