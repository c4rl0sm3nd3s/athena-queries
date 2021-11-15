
import data.athena as athena
from pandas.core.frame import DataFrame


def main():

    #load result from athena
    data_athena = athena.Athena()

    df_result = data_athena.get_query_executed()

    #TODO use dataframe ...