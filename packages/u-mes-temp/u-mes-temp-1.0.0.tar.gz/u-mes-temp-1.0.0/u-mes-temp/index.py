# encoding: utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
File: sms_client.py.py
Author: zhousongchuan(zhousongchuan@zybank.com.cn)
Date: 2021/11/5 上午9:18
"""
import socket
import datetime
import time
import sys


from config import current_env, DevConfig, TestConfig, ProConfig


seq_no = ""

class SmsClient(object):
    """
    短信客户端
    """

    def __init__(self):
        super(SmsClient, self).__init__()
        if current_env == "dev":
            self.host = DevConfig.SMS_HOST
            self.port = DevConfig.SMS_PORT
        elif current_env == "test":
            self.host = TestConfig.SMS_HOST
            self.port = TestConfig.SMS_PORT
        elif current_env == "pro":
            self.host = ProConfig.SMS_HOST
            self.port = ProConfig.SMS_PORT
        else:
            raise Exception("current_env {} not supported".format(current_env))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.logger = init_log("sms_client")

    def generate_content(self, address, ip, detail, level, metric, value, trans_branch="000", temp_code="4428",
                         system_name="omc", send_channel=0, tran_code="0200C200",
                         service_code="", seq_no=None, user_id="0001", customer_id="omc", branch_id="omc",
                         source_type="omc", tran_date=datetime.datetime.today().strftime("%Y%m%d"),
                         tran_timestamp=int(time.time()), server_id=None, source_branch_no="", dest_branch_no="",
                         tran_mode="", ws_id="omc", ebank_head_protocol="c200", ebank_head_src_branch="0"):
        """
        构造发送报文
        <?xml version="1.0" encoding="UTF-8">
        <Message>
          <Sys_Head>
            <TRAN_CODE>{tran_code}</TRAN_CODE>
            <SERVICE_CODE>{service_code}</SERVICE_CODE>
            <SEQ_NO>{seq_no}</SEQ_NO>
            <USER_ID>{user_id}</USER_ID>
            <CUSTOMER_ID>{customer_id}</CUSTOMER_ID>
            <BRANCH_ID>{branch_id}</BRANCH_ID>
            <SOURCE_TYPE>{source_type}</SOURCE_TYPE>
            <CONSUMER_ID></CONSUMER_ID>
            <TRAN_DATE>{tran_date}</TRAN_DATE>
            <TRAN_TIMESTAMP>{tran_timestamp}</TRAN_TIMESTAMP>
            <SERVER_ID>{server_id}</SERVER_ID>
            <SOURCE_BRANCH_NO>{source_branch_no}</SOURCE_BRANCH_NO>
            <DEST_BRANCH_NO>{dest_branch_no}</DEST_BRANCH_NO>
            <TRAN_MODE>{tran_mode}</TRAN_MODE>
            <WS_ID>{ws_id}</WS_ID>
          </Sys_Head>
          <Body>
            <Ebank_Head>
              <PROTOCOL>{ebank_head_protocol}</PROTOCOL>
              <SRCBRANCH>{ebank_head_src_branch}</SRCBRANCH>
            </Ebank_Head>
            <TRANSBRANCH>{trans_branch}</TRANSBRANCH>
            <ADDRESS>{address}</ADDRESS>
            <SENDCHANNEL>{send_channel}</SENDCHANNEL>
            <SYSTEMNAME>{system_name}</SYSTEMNAME>
            <IP>{ip}</IP>
            <DETAIL>{detail}</DETAIL>
            <LEVEL>{level}</LEVEL>
            <METRIC>{metric}</METRIC>
            <VALUE>{value}</VALUE>
            <DATE>{date}</DATE>
            <TEMPCODE>{temp_code}</TEMPCODE>
          </Body>
        </Message>
        :params
        :param address: 手机号
        :param trans_branch:
        :param send_channel: 0 短信 1原心
        :param system_name:
        :param ip:
        :param detail:
        :param level:
        :param metric:
        :param value:
        :param date:
        :param temp_code:
        :params sys_head: 内容,关键字参数
        :param tran_code: 交易码, STRING(8)
        :param service_code: 服务领域, STRING24
        :param seq_no: 全局流水号，编码规则： 3位字符串+6位字符串YYMMDD+9位整型数字+2位交易序号00
        :param user_id: 服务请求者身份
        :param customer_id: 客户号
        :param branch_id: 发送方机构id
        :param source_type: 渠道类型
        :param ws_id: 终端标识
        :param consumer_id: 请求系统编号，
        :param tran_date: 交易日期，
        :param tran_timestamp: 交易时间
        :param server_id: 服务器标识
        :param source_branch_no: 源节点编号
        :param dest_branch_no: 目标节点编号
        :param tran_mode: 交易模式
        :param ebank_head_protocol:
        :param ebank_head_src_branch:
        :return:
        """

        body = """
        <?xml version="1.0" encoding="UTF-8"?>
        <Message>
          <Sys_Head>
            <TRAN_CODE>{tran_code}</TRAN_CODE>
            <SERVICE_CODE>{service_code}</SERVICE_CODE> 
            <SEQ_NO>{seq_no}</SEQ_NO>
            <USER_ID>{user_id}</USER_ID>
            <CUSTOMER_ID>{customer_id}</CUSTOMER_ID>
            <BRANCH_ID>{branch_id}</BRANCH_ID>
            <SOURCE_TYPE>{source_type}</SOURCE_TYPE>
            <CONSUMER_ID></CONSUMER_ID>
            <TRAN_DATE>{tran_date}</TRAN_DATE>
            <TRAN_TIMESTAMP>{tran_timestamp}</TRAN_TIMESTAMP>
            <SERVER_ID>{server_id}</SERVER_ID>
            <SOURCE_BRANCH_NO>{source_branch_no}</SOURCE_BRANCH_NO>
            <DEST_BRANCH_NO>{dest_branch_no}</DEST_BRANCH_NO>
            <TRAN_MODE>{tran_mode}</TRAN_MODE>
            <WS_ID>{ws_id}</WS_ID>
          </Sys_Head>
          <Body>
            <Ebank_Head>
              <PROTOCOL>{ebank_head_protocol}</PROTOCOL>
              <SRCBRANCH>{ebank_head_src_branch}</SRCBRANCH>
            </Ebank_Head>
            <TRANSBRANCH>{trans_branch}</TRANSBRANCH>
            <ADDRESS>{address}</ADDRESS>
            <SENDCHANNEL>{send_channel}</SENDCHANNEL>
            <SYSTEMNAME>{system_name}</SYSTEMNAME>
            <IP>{ip}</IP>
            <DETAIL>{detail}</DETAIL>
            <LEVEL>{level}</LEVEL>
            <METRIC>{metric}</METRIC>
            <VALUE>{value}</VALUE>
            <DATE>{date}</DATE>
            <TEMPCODE>{temp_code}</TEMPCODE>
          </Body>
        </Message>
        """.format(address=address, ip=ip, detail=detail, level=level, metric=metric, value=value,
                   trans_branch=trans_branch, temp_code=temp_code, system_name=system_name,
                   send_channel=send_channel, tran_code=tran_code, service_code=service_code,
                   seq_no=seq_no, user_id=user_id, customer_id=customer_id, branch_id=branch_id,
                   source_type=source_type, tran_date=tran_date, tran_timestamp=tran_timestamp,
                   server_id=server_id, source_branch_no=source_branch_no, dest_branch_no=dest_branch_no,
                   tran_mode=tran_mode, ws_id=ws_id, ebank_head_protocol=ebank_head_protocol,
                   ebank_head_src_branch=ebank_head_src_branch, date=datetime.date.today().strftime("%Y-%m-%d"))
        return body

    def send(self, address, ip, detail, level, metric, value):
        """
        socket 初始化短连接，并发送socket报文
        :param address: 手机电话
        :param ip: 报警对象
        :param detail: 报警描述
        :param level: 报警级别
        :param metric: 报警指标
        :param value: 报警值
        :return:
        """
        self.sock.connect((self.host, self.port))
        content = self.generate_content(address, ip, detail, level, metric, value)
        # payload 获取负载
        payload = "%06d" % (len(content)) + content
        if sys.version_info.major >= 3:
            ret = self.sock.send(payload.encode("utf8"))
            result = self.sock.recv(1024)
            self.logger.info("payload={},send_ret={}, result={}".format(payload, ret, result.decode("utf8")))
        else:
            ret = self.sock.send(payload)
            result = self.sock.recv(1024)
            self.logger.info("payload={},result={}".format(payload, ret, result))
        return result
