import time
import hmac
import hashlib
import base64
import json
import aiohttp

import requests
from urllib.parse import quote_plus, urlencode


class DingTalkBot:
    url = 'https://oapi.dingtalk.com/robot/send'

    def __init__(self, token, secret):
        self.access_token = token
        self.secret = secret
        self.interval_set = {}

    @staticmethod
    def get_signature(ts, s):
        secret_enc = s.encode('utf-8')
        string_to_sign = '{}\n{}'.format(ts, s)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        return quote_plus(base64.b64encode(hmac_code).decode('utf-8'))

    def not_allow_report(self, tag, interval):
        if tag and interval:
            ts = int(time.time())
            last_report_ts = self.interval_set.get(tag)
            if last_report_ts is None:
                self.interval_set[tag] = ts
                return
            if ts - last_report_ts < interval:
                return True
            else:
                self.interval_set[tag] = ts

    async def async_send(self, data, tag=None, interval=None):
        if self.not_allow_report(tag, interval) is True:
            return
        timestamp = str(round(time.time() * 1000))
        sign = self.get_signature(timestamp, self.secret)
        params = {
            'access_token': self.access_token,
            'timestamp': timestamp,
            'sign': sign
        }
        url = f'{self.url}?{urlencode(params)}'
        async with aiohttp.ClientSession() as s:
            timeout = aiohttp.ClientTimeout(sock_read=20, sock_connect=10)
            async with s.request(
                    'POST',
                    url,
                    json=data,
                    timeout=timeout
            ) as response:
                if await self.async_check_response(response):
                    return await response.text()

    def send(self, data, tag=None, interval=None):
        if self.not_allow_report(tag, interval) is True:
            return
        timestamp = str(round(time.time() * 1000))
        sign = self.get_signature(timestamp, self.secret)
        params = {
            'access_token': self.access_token,
            'timestamp': timestamp,
            'sign': sign
        }
        url = f'{self.url}?{urlencode(params)}'
        resp = requests.post(url, json=data, timeout=(10, 20))
        if self.check_response(resp):
            return resp.text

    async def async_send_text(self, text, phone=None, tag=None, interval=None):
        text_meta = {
            "text": {"content": text},
            "msgtype": "text"
        }

        if phone:
            at = {
                "atMobiles": [
                    phone
                ]
            }
            text_meta['at'] = at

        return await self.async_send(text_meta, tag, interval)

    def send_text(self, text, phone=None, tag=None, interval=None):
        text_meta = {
            "text": {"content": text},
            "msgtype": "text"
        }

        if phone:
            at = {
                "atMobiles": [
                    phone
                ]
            }
            text_meta['at'] = at

        return self.send(text_meta, tag, interval)

    async def async_send_link(self, title, desc, message_url, pic_url=None, phone=None, tag=None, interval=None):
        link_meta = {
            "msgtype": "link",
            "link": {
                "text": desc,
                "title": title,
                "picUrl": pic_url,
                "messageUrl": message_url
            }
        }

        if phone:
            at = {
                "atMobiles": [
                    phone
                ]
            }
            link_meta['at'] = at

        return await self.async_send(link_meta, tag, interval)

    def send_link(self, title, desc, message_url, pic_url=None, phone=None, tag=None, interval=None):
        link_meta = {
            "msgtype": "link",
            "link": {
                "text": desc,
                "title": title,
                "picUrl": pic_url,
                "messageUrl": message_url
            }
        }

        if phone:
            at = {
                "atMobiles": [
                    phone
                ]
            }
            link_meta['at'] = at

        return self.send(link_meta, tag, interval)

    @staticmethod
    async def async_check_response(resp):
        if 200 <= resp.status < 300:
            return True

        text = await resp.text()
        try:
            res = await resp.json()
        except ValueError:
            raise RuntimeError(f'返回值异常 {text}')

        if str(res.get('errcode')) == '0':
            return True

        raise RuntimeError(f'发送失败 {text}')

    @staticmethod
    def check_response(resp):
        if 200 <= resp.status_code < 300:
            return True

        try:
            res = json.loads(resp.text)
        except ValueError:
            raise RuntimeError(f'返回值异常 {resp.text}')

        if str(res.get('errcode')) == '0':
            return True

        raise RuntimeError(f'发送失败 {res.text}')
