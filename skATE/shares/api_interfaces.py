# coding=utf-8
# author xin.he

class BaseRsp:
    """
    BaseRsp
    """
    def __init__(self, body, is_success, msg):
        # verify
        assert isinstance(is_success, bool)
        assert (msg is None) or (isinstance(msg, str))

        self._body = body
        self._is_success = is_success
        self._msg = msg

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def is_success(self):
        return self._is_success

    @is_success.setter
    def is_success(self, is_success):
        assert isinstance(is_success, bool)
        self._is_success = is_success

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        assert (msg is None) or (isinstance(msg, str))
        self._msg = msg

    def to_dict(self):
        return {
            "body": self._body,
            "isSuccess": self._is_success,
            "msg": self._msg
        }
