import json
import lambda_prototype_module as Module
def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    param = request_body['action']['params']
    key = list(param.keys())[0]  # 키가 여러개 들어올 경우는 생각해봐야 함. -> 그런 경우가 있을지부터 의문
    result_value = None
    try:
        if key == 'station':
            result_value = Module.CrawlingFunction.subway(Module.CrawlingFunction, station=str(param[key]))
        elif key == 'meal':
            result_value = Module.CrawlingFunction.random_meal(Module.CrawlingFunction)
        elif key == 'suid':
            if 'd38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895' == str(request_body['userRequest']['user']['properties']['botUserKey']):
                result_value = '권한이 있어요'
            else:
                result_value = '권한이 없어요'
        elif key == 'up_feedback':
            result_value = Module.CrawlingFunction.upload_feedback(Module.CrawlingFunction, params=str(param[key]))

        else:
            raise Exception("[Parameter Error] 잘못된 파라미터가 전달되었습니다.")

    except Exception as e:
            result_value = str(e)
    result = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(result_value)
                    }
                }
            ]
        }
    }
    return {
        'statusCode':200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }
import pprint
def lambda_handler2():
    result_value = None
    key = 'meal'
    try:
        if key == 'station':
            result_value = Module.CrawlingFunction.subway(Module.CrawlingFunction, station=str(param[key]))
        elif key == 'meal':
            result_value = Module.CrawlingFunction.random_meal(Module.CrawlingFunction)
        elif key == 'feedback':
            result_value = Module.CrawlingFunction.upload_feedback(Module.CrawlingFunction, params=str(param[key]))
        else:
            raise Exception("[Parameter Error] 잘못된 파라미터가 전달되었습니다.")

    except Exception as e:
            result_value = str(e)

    result = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(result_value)
                    }
                }
            ]
        }
    }
    return {
        'statusCode':200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

print(lambda_handler2())