if __name__ == '__main__':
    # main 파일을 엔트리포인트로 사용할 경우, path에 폴더 경로를 추가해 절대 경로로 임포트가 가능하게 함
    from sys import path
    import os
    path.append(os.path.dirname(__file__))

import json
import base64

def lambda_handler(context, event):
    request_body = event['body']
    request_body = json.loads(base64.b64decode(request_body))
    param = request_body['action']['params']
    # key = list(param.keys())
    # try:
    #     function_params = key[1:]
    # except Exception as e:
    #     print(e)
    #     pass

    return_string = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    'simpleText': {
                        "text": f"{str(param)}\n\n산돌이 기능개선중입니다 금방 돌아올게요!"
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
# pprint.pprint(lambda_handler(".", TEST_EVENT))