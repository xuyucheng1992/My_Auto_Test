# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/6/23 16:58
# @Author : XuYu


from common.com_manage import ComManage
from common.com_request import ComRequests


class GetToken:
    @classmethod
    def get_c_token(self):
        login_params = ComManage().manage_test_params("login.yaml")
        login_params = login_params[0][0]
        resp = ComRequests().send_requests(login_params)
        print(resp.json())
        token =resp.json()["responsebody"]["token"]
        mid = resp.json()["responsebody"]["mId"]
        return mid + "_" + token

    @classmethod
    def get_p_token(self):
        login_params = ComManage().manage_test_params("p_login.yaml")
        login_params = login_params[0][0]
        resp = ComRequests().send_requests(login_params)
        print(resp.json())
        return resp.json()["access_token"]


if __name__ == "__main__":
    print(GetToken.get_p_token())
