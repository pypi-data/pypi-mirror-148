import re
from typing import Optional
from PyQt6.QtCore import pyqtSignal
import logging
# 测试模块

class SshConnection:
    # 三种模式，内部使用
    COMMON = 1
    RFSW = 2
    AASHELL = 3

    def __init__(self, hostname: str, username: str, password: str, port: int,
                 logger: Optional[logging.Logger], sg: Optional[pyqtSignal] = None,
                 send_interval: float = 0.5, read_interval: float = 0.5):
        """
        :param hostname: ip地址
        :param username: 用户名
        :param password: 密码
        :param port: 端口号
        :param logger: log模块
        :param sg: 用于Qt信号发射，默认禁用
        :param send_interval: 命令发送间隔，默认为0.5s
        :param read_interval: 命令读取间隔，默认为0.5s
        """
        self.logger = logger
        self.send_interval = send_interval
        self.read_interval = read_interval
        self.sg = sg
        self._typ = SshConnection.COMMON
        self.cmd_list = []

    def common_cmd(self, command: str):
        """
        普通命令
        :param command:
        :return:
        """
        self.log('{' + command + '}')

    def rfsw_cmd(self, command: str):
        """
        rfsw命令
        :param command:
        :return:
        """
        self.log('[' + command + ']')

    def aashell_cmd(self, command: str):
        """
        aashell命令
        :param command:
        :return:
        """
        self.log('(' + command + ')')

    def log(self, message: str) -> None:
        """
        存储日志，两种方式，logger或者pyqtSignal
        :param message:
        :return:
        """
        if self.logger is not None:
            self.logger.info(message)
        if self.sg is not None:
            self.sg[str].emit(message)

    def load_cmd_file(self, file_path: str):
        """
        通过文本方式执行命令
        :param file_path:
        :return:
        """
        with open(file_path) as file:
            self.cmd_list = file.readlines()

    def send_by_file(self, param_dict: Optional[dict] = None,
                     start_mark: Optional[str] = None, stop_mark: Optional[str] = None,
                     common_prefix: str = "`", rfsw_prefix: str = "", aashell_prefix: str = "``") -> str:
        """
        可以指定执行起始标记符与截止标记符之间的命令行，默认为rfsw_cli模式
        关于标记符：
        start_mark如果为None或者找不到，则默认为文件开头
        stop_mark如果为None，则默认为下一个<xxx>，如果找不到，则默认为文件尾部
        :param param_dict: 传入字典进行format赋值
        :param start_mark: 起始标记符，默认<xxx>形式
        :param stop_mark: 截止标记符，默认<xxx>形式
        :param common_prefix: 通用命令符前缀为`
        :param rfsw_prefix: 通用命令符前缀为
        :param aashell_prefix: aashell命令符前缀为``
        :return: 最后一行命令的返回结果
        """
        res = ""
        start_row = 0
        stop_row = len(self.cmd_list)
        for index, cmd in enumerate(self.cmd_list):
            if cmd.strip() == start_mark:
                start_row = index + 1
                break
        for index, cmd in enumerate(self.cmd_list):
            if index >= start_row and (cmd.strip() == stop_mark or (stop_mark is None and re.match("<.*>", cmd))):
                stop_row = index
                break

        for cmd in self.cmd_list[start_row: stop_row]:
            if cmd == '\n' or re.match("<.*>", cmd):
                pass
            else:
                if cmd.startswith(common_prefix):
                    self.common_cmd(
                        cmd.lstrip(common_prefix).rstrip() if param_dict is None else cmd.rstrip().format(**param_dict))
                elif cmd.startswith(rfsw_prefix):
                    self.rfsw_cmd(
                        cmd.lstrip(rfsw_prefix).rstrip() if param_dict is None else cmd.rstrip().format(**param_dict))
                elif cmd.startswith(aashell_prefix):
                    self.aashell_cmd(
                        cmd.lstrip(aashell_prefix).rstrip() if param_dict is None else cmd.rstrip().format(
                            **param_dict))
        return res
