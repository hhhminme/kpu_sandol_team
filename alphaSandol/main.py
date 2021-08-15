if __name__ == '__main__':
    # main 파일을 엔트리포인트로 사용할 경우, path에 폴더 경로를 추가해 절대 경로로 임포트가 가능하게 함
    from sys import path
    import os
    path.append(os.path.dirname(__file__))

import json
import base64
import lambda_module as Module

def lambda_handler(event, context):
    try:
        return_string = ''
        request_body = event['body']
        request_body = json.loads(base64.b64decode(request_body))
        param = request_body['action']['params']
        key = list(param.keys())
        func_name = key[0]
        key_values = list(param.values())
        ACCESS_ID = str(request_body['userRequest']['user']['id'])  # 접근 권한을 가진 ID 확인용

        if func_name == 'weather':
            return_string = Module.Weather.weather()
        else:
            raise Exception

    except Exception as e:
        return_string = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"산돌이 기능 업데이트중입니다! 일부 기능이 사용이 제한됩니다\{e}"
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "messageText": "도움말",
                        "action": "message",
                        "label": "도움말"
                    }
                ]
            }
        }

    return {
        'statusCode': 200,
        'body': json.dumps(return_string),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }