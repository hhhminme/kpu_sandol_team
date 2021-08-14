import json
import lambda_module as Module
import base64

def go_function(function_name:list) ->dict:
    pass
def lambda_handler(event, context):
    try:
        request_body = event['body']
        request_body = json.loads(base64.b64decode(request_body))
        param = request_body['action']['params']
        key = list(param.keys())  # 입력으로 들어오는 값을 여기서 처리함
        # 여러개 들어오는 경우 필수 파라미터 명이 key[0]에 들어감
        if key[0] not in Constant.KEY_SET.keys():
            raise Exception('입력 파라미터가 잘못되었습니다.')

        return_string = Constant.KEY_SET[key[0]].

    except Exception as e:
        return_string = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "[Main Function Error]"+str(e)
                        }
                    }
                ],
                "quickReplies" : [
                    {
                        "messageText" : "도움말",
                        "action" : "message",
                        "label" : "도움말"
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
