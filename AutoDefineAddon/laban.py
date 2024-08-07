import requests
from http import cookiejar
from bs4 import BeautifulSoup

class WordNotFound(Exception):
    """Exception raised when a word is not found in the dictionary (404 status code)."""
    pass

class BlockAll(cookiejar.CookiePolicy):
    """Policy to block cookies."""
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

class Word:
    """Retrieve word info from the Laban dictionary website."""
    BASE_URL = 'https://dict.laban.vn/find?type=1&query='
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/118.0.0.0 Safari/537.36'
    }

    def __init__(self, word, headers=HEADERS):
        self.word = word
        self.soup_data = None
        self.HEADERS = headers

    def get_url(self):
        """Get the URL of the word definition."""
        return self.BASE_URL + self.word

    def fetch_word_data(self):
        """Fetch the HTML soup of the word."""
        session = requests.Session()
        session.cookies.set_policy(BlockAll())
        
        response = session.get(self.get_url(), headers=self.HEADERS)
        if response.status_code == 404:
            raise WordNotFound(f"Word '{self.word}' not found in the dictionary.")
        self.soup_data = BeautifulSoup(response.content, 'html.parser')

    def parse_definitions(self):
        """Parse and return word definitions."""
        if not self.soup_data:
            return []

        content_divs = self.soup_data.select('.slide_content:not(.hidden) #content_selectable')
        definitions = []

        for content_div in content_divs:
            wordform_divs = content_div.find_all('div', {'class': 'bg-grey bold font-large m-top20'})
            for wordform_div in wordform_divs:
                wordform = wordform_div.get_text(strip=True)
                definition_elements = wordform_div.find_next_siblings('div', limit=20)  # Increased limit to capture more siblings
                
                word_definitions = []
                current_definition = {'description': "", 'examples': []}
                for element in definition_elements:
                    if 'green' in element.get('class', []) and 'bold' in element.get('class', []):
                        if current_definition['description']:
                            word_definitions.append(current_definition)
                        current_definition = {'description': element.get_text(strip=True), 'examples': []}
                    elif 'color-light-blue' in element.get('class', []):
                        example_text = ' '.join(element.stripped_strings)
                        translation_element = element.find_next_sibling('div', {'class': 'margin25'})
                        translation_text = translation_element.get_text(strip=True) if translation_element else ""
                        current_definition['examples'].append({'example': example_text, 'translation': translation_text})
                
                if current_definition['description']:
                    word_definitions.append(current_definition)
                
                definitions.append({
                    'wordform': wordform,
                    'definitions': word_definitions
                })
        
        return definitions

    def parse_idioms(self):
        """Parse and return idioms."""
        if not self.soup_data:
            return []
        
        content_divs = self.soup_data.select('.slide_content:not(.hidden) #content_selectable')

        idioms = []
        for content_div in content_divs:
            idiom_elements = content_div.find_all('div', {'class': 'bold dot-blue m-top15'})
            for idiom_element in idiom_elements:
                idiom_text = idiom_element.get_text(strip=True)
                current_element = idiom_element

                idiom_definitions = []
                current_definition = {'description': "", 'examples': []}

                while current_element := current_element.find_next_sibling():
                    if 'grey' in current_element.get('class', []) and 'bold' in current_element.get('class', []):
                        if current_definition['description']:
                            idiom_definitions.append(current_definition)
                        current_definition = {'description': current_element.get_text(strip=True), 'examples': []}
                    elif 'color-light-blue' in current_element.get('class', []):
                        example_text = ' '.join(current_element.stripped_strings)
                        translation_element = current_element.find_next_sibling('div', {'class': 'margin25'})
                        translation_text = translation_element.get_text(strip=True) if translation_element else ""
                        current_definition['examples'].append({'example': example_text, 'translation': translation_text})
                    else:
                        break
                
                if current_definition['description']:
                    idiom_definitions.append(current_definition)

                idioms.append({
                    'name': idiom_text,
                    'definitions': idiom_definitions
                })

        return idioms

    def get_info(self):
        """Return all info about a word."""
        self.fetch_word_data()

        return {
            'definitions': self.parse_definitions(),
            'idioms': self.parse_idioms()
        }

'''
# Usage example:
try:
    word_to_lookup = 'love'
    word_instance = Word(word_to_lookup)
    word_info = word_instance.get_info()
    print(word_info)
except WordNotFound as e:
    print(e)
'''

{
  "definitions": [
    {
      "wordform": "Danh từ",
      "definitions": [
        {
          "description": "tình yêu, tình thương",
          "examples": [
            {
              "example": "a mother's love for her children",
              "translation": "tình thương của mẹ đối với con cái"
            },
            {
              "example": "love of [ one's ] country",
              "translation": "tình yêu đất nước"
            },
            {
              "example": "she has a great love for animals",
              "translation": "chị ta rất thương loài vật"
            },
            {
              "example": "their love has cooled",
              "translation": "tình yêu của họ đã nguôi lạnh"
            }
          ]
        },
        {
          "description": "người yêu; người đáng yêu, vật đáng yêu",
          "examples": [
            {
              "example": "take care , my love",
              "translation": "cẩn thận đấy, em yêu"
            },
            {
              "example": "what a love her daughter is !",
              "translation": "con gái bà ta thật đáng yêu làm sao!"
            },
            {
              "example": "isn't this hat perfect love?",
              "translation": "cái mũ này có đáng yêu không?"
            }
          ]
        },
        {
          "description": "(tôn giáo) lòng nhân từ của Chúa (đối với nhân loại)",
          "examples": []
        },
        {
          "description": "lòng say mê",
          "examples": [
            {
              "example": "a love of music",
              "translation": "lòng say mê âm nhạc"
            }
          ]
        }
      ]
    },
    {
      "wordform": "Động từ",
      "definitions": [
        {
          "description": "yêu, yêu thương, yêu mến",
          "examples": [
            { "example": "love one another", "translation": "yêu thương nhau" },
            { "example": "love one's parents", "translation": "yêu cha mẹ" },
            { "example": "love one's country", "translation": "yêu đất nước" },
            { "example": "love one's wife", "translation": "yêu vợ" }
          ]
        },
        {
          "description": "thích, ưa thích",
          "examples": [
            { "example": "love music", "translation": "thích âm nhạc" },
            {
              "example": "he loves to be praised",
              "translation": "nó thích được khen"
            },
            {
              "example": "he loves his pipe",
              "translation": "ông ta thích cái tẩu của ông lắm"
            },
            {
              "example": "we'd love you to come to dinner",
              "translation": "chúng tôi mong anh đến dùng cơm tối với chúng tôi"
            }
          ]
        }
      ]
    }
  ],
  "idioms": [
    {
      "name": "be in love [with somebody]",
      "definitions": [{ "description": "yêu ai", "examples": [] }]
    },
    {
      "name": "be in love with something",
      "definitions": [{ "description": "thích, mê (cái gì)", "examples": [] }]
    },
    { "name": "cupboardlove", "definitions": [] },
    {
      "name": "fall in love [with somebody]",
      "definitions": [{ "description": "phải lòng ai", "examples": [] }]
    },
    {
      "name": "[just] for love (for the love of something)",
      "definitions": [
        {
          "description": "vì thích mà làm, không cần thưởng công",
          "examples": [
            {
              "example": "they're all volunteers , doing it just for the love of the thing",
              "translation": "họ hết thảy là người tình nguyện, thích mà làm không phải thưởng công"
            }
          ]
        }
      ]
    },
    {
      "name": "for the love of God",
      "definitions": [
        {
          "description": "(dùng tỏ sự ngạc nhiên hay thúc giục ai làm gì) lạy Chúa",
          "examples": []
        }
      ]
    },
    {
      "name": "give (send) somebody one's love",
      "definitions": [
        {
          "description": "gửi lời chào (tới ai)",
          "examples": [
            {
              "example": "please give your sister my love",
              "translation": "xin cho gửi lời chào chị anh nhé"
            }
          ]
        }
      ]
    },
    { "name": "a labour of love", "definitions": [] },
    {
      "name": "the love of somebody's life",
      "definitions": [
        { "description": "người yêu nhất trên đời", "examples": [] },
        {
          "description": "niềm say mê, lòng yêu thích",
          "examples": [
            {
              "example": "sailing is the love of his life",
              "translation": "bơi xuồng là món yêu thích của anh"
            }
          ]
        }
      ]
    },
    {
      "name": "make love [to somebody]",
      "definitions": [
        { "description": "làm tình, ăn nằm(với ai)", "examples": [] }
      ]
    },
    {
      "name": "not for love or money",
      "definitions": [
        {
          "description": "bằng bất cứ cách nào cũng được",
          "examples": [
            {
              "example": "we couldn't find a hotel room for love and money",
              "translation": "chúng tôi không sao tìm được một phòng khách sạn"
            }
          ]
        }
      ]
    },
    {
      "name": "there's little (no) love lost between A and B",
      "definitions": [{ "description": "A và B không ưa nhau", "examples": [] }]
    },
    {
      "name": "love me, love my dog",
      "definitions": [
        { "description": "yêu ai yêu cả tông chi họ hàng", "examples": [] }
      ]
    }
  ]
}