# return_type_generator.py

## OverView

* 카카오 오픈빌더의 각 타입에 들어가는 인자 값을 함수의 파라미터로 받아 자동으로 리턴 값을 생성해주는  Python 코드
* 총 6종류의 JSON 형식을 지원함
  * Simple Text : 간단한 텍스트 타입
  * Simple Image : 간단한 이미지 타입
  * Basic Card : 기본 카드형 타입
  * Commerce Card : 제품 소개등을 할 때 사용하는 카드형 타입
  * List Card : 표현하고자 하는 대상이 다수일 때 효과적으로 사용하는 카드형 타입
  * Carousel : 여러 장의 카드를 하나의 메시지에 일렬로 포함하는 타입



## Usage



### Basic Card

```python
is_Card(self,thumb_img, is_title = None, is_description = None, is_buttons = None)
```

![]()