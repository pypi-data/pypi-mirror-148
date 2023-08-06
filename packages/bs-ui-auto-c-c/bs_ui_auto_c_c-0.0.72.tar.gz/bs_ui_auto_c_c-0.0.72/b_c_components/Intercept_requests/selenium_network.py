
import math
import json
import time
from urllib import parse

class WebdriverLogFacade(object):

    last_timestamp = 0

    def __init__(self, webdriver):
        self._webdriver = webdriver

    def get_log(self):
        last_timestamp = self.last_timestamp
        entries = self._webdriver.get_log("performance")
        filtered = []

        for entry in entries:
            # check the logged timestamp against the
            # stored timestamp
            if entry["timestamp"] > self.last_timestamp:
                filtered.append(entry)

                # save the last timestamp only if newer
                # in this set of logs
                if entry["timestamp"] > last_timestamp:
                    last_timestamp = entry["timestamp"]

        # store the very last timestamp
        self.last_timestamp = last_timestamp

        return filtered

def info(driver):
    """
    已弃用，不允许新的方法引用，如引用，需引用get_network_data
    :param driver:
    :return:
    """
    # 睡眠的作用是等待网页加载完毕，因为还有异步加载的网页，有时候会少拿到请求
    return get_network_data(driver)


def get_network_data(driver):
    """
    调用selenium,开启selenium的日志收集功能，收集所有日志，并从中挑出network部分，分析格式化数据，传出
    :param driver:
    :return:
    """
    # 睡眠的作用是等待网页加载完毕，因为还有异步加载的网页，有时候会少拿到请求
    response_data, requests_post_data = None, None
    time.sleep(4)
    network_data = []
    # log_facade = WebdriverLogFacade(driver)
    # logs = log_facade.get_log()
    # more logs will be generated
    page_object = driver.log_obj.get_log()
    # newest log returned only
    # page_object = driver.get_log('performance')
    for log in page_object:
        x = json.loads(log['message'])['message']
        if x["method"] == "Network.requestWillBeSent":
            if x["params"]["request"]["method"] == 'OPTIONS':
                continue
            try:
                response_data = driver.execute_cdp_cmd(
                    'Network.getResponseBody', {
                        'requestId': x["params"]['requestId']})
                if x["params"]["request"]["method"] == "POST":
                    requests_post_data = driver.execute_cdp_cmd(
                        'Network.getRequestPostData', {
                            'requestId': x["params"]['requestId']})

            except Exception:
                pass

            network_data.append(
                    {
                        'type': x["params"]["type"],
                        'request': {
                            'requestId': x["params"]['requestId'],
                            'url': x["params"]["request"]["url"],
                            'method': x["params"]["request"]["method"],
                            'headers': x["params"]['request']['headers'],
                            'request_post_data': parse.unquote(requests_post_data.get('postData')) if requests_post_data is not None else None
                        },
                        'response_data': response_data if response_data is not None else None
                    }
            )
    for log in page_object:
        x = json.loads(log['message'])['message']
        if x["method"] == "Network.responseReceived":
            for data in network_data:
                if x['params']['requestId'] == data['request']['requestId']:
                    data.update(responseReceived=x['params']['response'])
    driver.global_cases_instance['network_data'] += network_data
    return network_data


def get_interface_date(driver, url_path, get_type):
    """
    获取指定接口返回数据
    url_path:接口地址
    get_type: 获取内容:request|response|all
    :param: driver
    """
    get_network_data(driver)
    return_list = []
    for data in driver.global_cases_instance.get('network_data'):
        if url_path in data.get('request').get('url'):
            if get_type == 'request':
                return_list.append({'request': data.get('request')})
            if get_type == 'response':
                return_list.append({'response_data': data.get('response_data')})
            if get_type == 'all':
                return_list.append({'request': data.get('request'), 'response_data': data.get('response')})

    return return_list


def get_interface_body(driver, interface_path, interface_type='Fetch'):
    """
    获取对应请求的body
    """
    get_network_data(driver)
    network_data = driver.global_cases_instance.get('network_data')
    network_data.reverse()
    data = None
    for data_1 in network_data:
        if interface_path in data_1.get('request').get('url') and data_1.get('type') == interface_type:
            data = data_1.get('response_data').get('body')
            break
    return data


def get_case_all_network_data(driver):
    """
    获取当前case运行期间产生的所有请求
    """
    get_network_data(driver)
    return driver.global_cases_instance.get('network_data')
