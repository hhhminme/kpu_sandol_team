import json
import lambda_prototype_module as Module
import base64

def lambda_handler(event, context):
    return_string = None
    try:
        request_body = event['body']
        request_body = json.loads(base64.b64decode(request_body))
        param = request_body['action']['params']
        key = list(param.keys())  # 입력으로 들어오는 값을 여기서 처리함
        # 여러개 들어오는 경우 필수 파라미터 명이 key[0]에 들어감
        if key[0] == 'weather': #날씨 관련
            return_string = Module.CrawlingFunction.weather(Module.CrawlingFunction, param[key[0]])

        elif key[0] == 'feedback_upload':
            return_string = Module.s3IOEvent.upload_feedback(Module.CrawlingFunction, params=str(param[key[0]]))
        elif key[0] == 'read_feedback':
            return_string = Module.s3IOEvent.read_feedback(Module.CrawlingFunction, params=str(param[key[0]]))
        elif key[0] == 'perm_chk':
            return_string = request_body['userRequest']['user']['id']
        elif key[0] == 'upload_date':
            return_string = [str(json.loads(param[key[0]])["date"]),param[key[1]], param[key[2]], param[key[3]], str(request_body['userRequest']['user']['properties']['botUserKey'])]
            return_string = str(return_string)
            #return_string = Module.s3IOEvent.upload_meal(Module.s3IOEvent, str(json.loads(param[key[0]])["date"]),param[key[1]], param[key[2]], param[key[3]], str(request_body['userRequest']['user']['properties']['botUserKey']))
        else:
            return_string = "산돌이가 작업을 마무리하지 못했어요ㅠㅠ\n 피드백을 통해 어떤 기능에서 오류가 발생했는지 알려주시면 빠른 시일 내에 작동 하도록 할게요" + str(param)

        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": str(return_string)
                        }
                    }
                ]
            }
        }

    except Exception as e:
        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": str(e)
                        }
                    }
                ]
            }
        }

    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

lambda_handler("a","b")