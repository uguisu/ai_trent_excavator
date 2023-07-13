# coding=utf-8
# author xin.he
from skATE.data_mysql.i_data_fetcher import IDataFetcher


class SegmentLatencyFetcher(IDataFetcher):
    """
    SegmentLatencyFetcher
    """

    def __init__(self,
                 database_connection,
                 trace_name: str,
                 trace_id: str,
                 limitation: int = 2000):
        """
        init

        :param database_connection: database connection object
        :param trace_name: trace name
        :param trace_id: trace id
        :param limitation: limitation
        """

        self._trace_name = trace_name
        self._trace_id = trace_id
        self._limitation = limitation

        super().__init__(database_connection)

    def declare_sql(self) -> str:
        """
        declare SQL statement
        """

        return f'''
        SELECT
            segm.latency
        FROM
            service_traffic srv_tra
        LEFT JOIN instance_traffic ins_tra
            ON srv_tra.service_id = ins_tra.service_id
        LEFT JOIN segment segm
            ON ins_tra.id = segm.service_instance_id
        WHERE
            srv_tra.name = '{self._trace_name}'
            AND srv_tra.id = '{self._trace_id}'
        ORDER BY
            segm.start_time DESC,
            segm.time_bucket DESC
        LIMIT {self._limitation}
        '''

    @staticmethod
    def metadata() -> dict:
        """
        get metadata
        """
        return {
            'trace_name': '',
            'trace_id': '',
            'limitation': 2000,
        }
