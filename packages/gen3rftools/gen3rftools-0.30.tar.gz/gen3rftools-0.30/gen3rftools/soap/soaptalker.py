import socket
import threading
import time
import os

from lxml import etree


class SoapTalker:
    BUFFSIZE = 307200
    SID = 1001

    def __init__(self, local_ip: str, local_port: int, remote_ip: str, remote_port: int, timeout: int = 30):
        '''

        :param local_ip:
        :param local_port:
        :param remote_ip:
        :param remote_port:
        :param timeout:
        '''
        self.local_ip = local_ip
        self.local_port = local_port
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(timeout)
        self.udp_socket.bind((self.local_ip, self.local_port))
        self._lock = threading.Lock()
        self._rec_cache = None
        self._send_cache = None

    def rec_msg(self, rec_delay: float = 1):
        '''

        :param rec_delay:
        :return:
        '''
        with open(os.path.join(os.path.dirname(__file__), "autoreply/moduleReadyAck.xml")) as file1:
            soap_test_xml = file1.read()
        with open(os.path.join(os.path.dirname(__file__), "autoreply/moduleReadyInd.xml")) as file2:
            mra_xml = file2.read()
        while True:
            rec_data, (remote_host, remote_port) = self.udp_socket.recvfrom(self.BUFFSIZE)
            print("_____________  receiving  ________________")
            print(rec_data.decode())
            print("_____________  receiving  ________________")
            time.sleep(0.1)
            # with self.lock:
            if rec_data.decode():
                self._rec_cache = rec_data.decode()
                tree = etree.HTML(self._rec_cache)
                if tree.xpath("//discoverymessage"):
                    relatesTo = tree.xpath("//id/text()")[0]
                    nodeLabel = tree.xpath("//nodelabel/text()")[0]
                    serialNum = tree.xpath("//serialnum/text()")[0]
                    send_data = soap_test_xml.format(id=self.SID, relatesTo=relatesTo, nodeLabel=nodeLabel,
                                                     serialNum=serialNum)
                    self.udp_socket.sendto(send_data.encode(), (self.remote_ip, self.remote_port))
                    self._send_cache = send_data
                    print("**************** auto sending ********************")
                    print(send_data)
                    print("**************** auto sending ********************")
                    self.SID += 1
                elif tree.xpath("//modulereadyind"):
                    relatesTo = tree.xpath("//id/text()")[0]
                    send_data = mra_xml.format(id=self.SID, relatesTo=relatesTo)
                    self.udp_socket.sendto(send_data.encode(), (self.remote_ip, self.remote_port))
                    self._send_cache = send_data
                    print("**************** auto sending ********************")
                    print(send_data)
                    print("**************** auto sending ********************")
                    self.SID += 1
            time.sleep(rec_delay)

    def send_msg(self, send_data_list: list, init_delay: float = 1, send_delay: float = 1):
        '''

        :param send_data_list:
        :param init_delay:
        :param send_delay:
        :return:
        '''
        # 开始发送信息的条件：（1）接收是soap_test初始化，发送是moduleReadyAck，接收的id等于发送的relatesTo
        #                 （2）接收是moduleReadyInd，发送是moduleReadyInd，接收的id等于发送的relatesTo
        while True:
            time.sleep(init_delay)
            if self._rec_cache and self._send_cache:
                tree1 = etree.HTML(self._rec_cache)
                tree2 = etree.HTML(self._send_cache)
                if tree1.xpath("//modulereadyind") and (
                        tree2.xpath("//modulereadyack") or tree2.xpath("//modulereadyind")):
                    if tree1.xpath("//id/text()")[0] == tree2.xpath("//relatesto/text()")[0]:
                        break

        for num, send_data in enumerate(send_data_list):
            _id = etree.HTML(self._rec_cache).xpath("//id/text()")[0]
            self.udp_socket.sendto(send_data.encode(), (self.remote_ip, self.remote_port))
            print(f"**************** manual sending {num} ********************")
            print(send_data)
            print(f"**************** manual sending {num} ********************")
            # 发送下一条信息的条件：接收是新id并且status为OK
            while True:
                time.sleep(send_delay)
                # with self.lock:
                if self._rec_cache:
                    tree = etree.HTML(self._rec_cache)
                    if tree.xpath("//status"):
                        if tree.xpath("//parvaluechangeind/status/text()")[0] == "OK" and _id != \
                                tree.xpath("//id/text()")[0]:
                            break

    def close(self):
        self.udp_socket.close()

    def __del__(self):
        self.close()
