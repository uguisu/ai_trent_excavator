# coding=utf-8
# author xin.he


def get_current_date_time() -> str:
    """
    get current date time in '99991231_235959'
    """
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d%_H%M%S")
