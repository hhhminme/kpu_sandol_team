import json
import lambda_prototype_module as Module
import base64

def lambda_handler(event, context):
    try:
        request_body = event['body']
        request_body = json.loads(base64.b64decode(request_body))
        param = request_body['action']['params']
        #key = list(param.keys())  # 입력으로 들어오는 값을 여기서 처리함
        # 여러개 들어오는 경우 필수 파라미터 명이 key[0]에 들어감
        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": str(param)
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

a = "ewogICJpbnRlbnQiOiB7CiAgICAiaWQiOiAiYWZvcGd1bmVlZ2o2c2VuZ3dmc2V6Z3VzIiwKICAgICJuYW1lIjogIuu4lOuhnSDsnbTrpoQiCiAgfSwKICAidXNlclJlcXVlc3QiOiB7CiAgICAidGltZXpvbmUiOiAiQXNpYS9TZW91bCIsCiAgICAicGFyYW1zIjogewogICAgICAiaWdub3JlTWUiOiAidHJ1ZSIKICAgIH0sCiAgICAiYmxvY2siOiB7CiAgICAgICJpZCI6ICJhZm9wZ3VuZWVnajZzZW5nd2ZzZXpndXMiLAogICAgICAibmFtZSI6ICLruJTroZ0g7J2066aEIgogICAgfSwKICAgICJ1dHRlcmFuY2UiOiAi67Cc7ZmUIOuCtOyaqSIsCiAgICAibGFuZyI6IG51bGwsCiAgICAidXNlciI6IHsKICAgICAgImlkIjogIjUwNjE3NiIsCiAgICAgICJ0eXBlIjogImFjY291bnRJZCIsCiAgICAgICJwcm9wZXJ0aWVzIjoge30KICAgIH0KICB9LAogICJib3QiOiB7CiAgICAiaWQiOiAiNWZmNzEwMzI4YzAwOGU0ZTA4MWIyZjkyIiwKICAgICJuYW1lIjogIuu0hyDsnbTrpoQiCiAgfSwKICAiYWN0aW9uIjogewogICAgIm5hbWUiOiAib2s2cWdyZ3E2ZyIsCiAgICAiY2xpZW50RXh0cmEiOiBudWxsLAogICAgInBhcmFtcyI6IHsKICAgICAgIm1lYWwiOiAiYXNkZiIKICAgIH0sCiAgICAiaWQiOiAieGI5Z2dleHdlNm5yMnFwc2picmx0ZWlkIiwKICAgICJkZXRhaWxQYXJhbXMiOiB7CiAgICAgICJtZWFsIjogewogICAgICAgICJvcmlnaW4iOiAiYXNkZiIsCiAgICAgICAgInZhbHVlIjogImFzZGYiLAogICAgICAgICJncm91cE5hbWUiOiAiIgogICAgICB9CiAgICB9CiAgfQp9"
print()