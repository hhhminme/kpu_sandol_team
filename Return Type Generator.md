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

### Simple Text

<img src="./return_type_img/Text Type.JPG" style="zoom:50%;" />



```Python
def is_Text(self, text):
```

**필수 파라미터**

> text\<string\> : 출력할 string을 입력으로 받음



**사용 예시**

```python
import return_type_generator as Generator
gen = Generator()
result = gen.is_Text("<날씨 스킬 파트 실행>")
```

<img src="./return_type_img/Simple Text Test.JPG" style="zoom:100%;" />





### Basic Card

<img src="./return_type_img/Basic Card Type.JPG" style="zoom:50%;" />



```python
def is_Card(self,thumb_img, *is_buttons, is_title = None, is_description = None): 
```

<img src="./return_type_img/Basic Card Field.JPG" style="zoom:50%;" />



**필수 파라미터**

> thumb_img \<string\> : img의 주소를 `string` 형태로 전달



**선택 파라미터**

> *is_buttons \<dict\> : button 을 생성하는 dictionary(JSON) 형태로 전달.
>
> is_title \<string\> : 카드의 제목을 문자열 형태로 전달
>
> is_description \<string\> : 카드에 대한 설명을 문자열 형태로 전달



**사용 예시**

```python
import return_type_generator as Generator
gen = Generator()
result = gen.is_Card("https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/img/logo1.png", is_title="logo", is_description = "<코로나 스킬 파트 실행>")
```

<img src="./return_type_img/Basic Card Test.JPG" style="zoom:100%;" />





### Commerce Card

```Python
def is_commerce(self,thumbnail, description, price, currency, *is_buttons, is_discount = None, is_discountRate = None, is_discountedPrice = None, profile = None):
```

<img src="./return_type_img/Commerce Card Field.JPG" style="zoom:50%;" />

**필수 파라미터**

> description \<string\> : 판매 항목의 설명을 문자열 형태로 전달
>
> price \<int\> : 제품의 가격을 문자열 형태로 전달
>
> currency \<string\> : 제품 가격의 통화를 전달합니다 (`won`만 가능)
>
> thumbnail \<string\> : 썸네일 이미지 URL을 전달합니다.
>
> is_buttons\<string\> : 기본적으로 `구매하기` 버튼이 생성되며, 추가 버튼을 전달합니다 (최대 2개)



**선택 파라미터**

> is_discount \<int\> : 제품의 할인한 금액을 전달합니다.
>
> is_discountRate \<int\> : 제품의 가격에 대한 할인된 가격의 비율을 전달합니다.
>
> is_discountPrice\<int\> : 제품의 가격에 대한 할인가(할인된 가격)을 전달합니다.
>
> profile : 제품을 판매하는 프로필 정보를 전달합니다.

