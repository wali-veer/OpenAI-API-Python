# Weather Assistant using OpenAI Function Calling

This project demonstrates a CLI-based AI assistant that answers weather-related questions using OpenAI function calling and the OpenWeatherMap API.

---

## Running the Script

```bash
(env) PS <MY_PYTHON_SCRIPT_PATH>> python.exe ./mainProgram.py
```

---

## Sample Execution

```
Bot: Hello, I am a helpful assistant. Type 'exit' to quit.
You: What is the weather like in Bangalore ?
```

### Model Tool Call Output

```python
ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_mj28SOYP4ib0TF0aSGlthfEm', function=Function(arguments='{"location":"Bangalore","unit":"celsius"}', name='get_current_weather'), type='function')])
```

### Weather Function Response

```json
{"location": "Bangalore", "temperature": "23", "unit": "celsius", "forecast": "clear sky"}
```

### Final Bot Response

```
Bot: The current weather in Bangalore is 23°C with a clear sky.
```

---

## Manual API Invocation

### 1) Geocoding API

```
http://api.openweathermap.org/geo/1.0/direct?q=Bangalore&appid=<API-KEY>
```

**Response**

```json
[
  {
    "name": "Bengaluru",
    "local_names": {
      "pa": "ਬੈਂਗਲੁਰੂ",
      "or": "ବେଙ୍ଗାଳୁରୁ",
      "oc": "Bengaluri",
      "hi": "बेंगलुरु",
      "ml": "ബെംഗളൂരു",
      "ru": "Бангалор",
      "zh": "班加罗尔",
      "el": "Μπανγκαλόρ",
      "te": "బెంగళూరు",
      "de": "Bangalore",
      "cs": "Bengalúru",
      "as": "বাংগালোৰ",
      "uk": "Бенгалуру",
      "ja": "バンガロール",
      "he": "בנגלור",
      "th": "บังคาลอร์",
      "mr": "बंगळूर",
      "my": "ဘန်ဂလိုမြို့",
      "it": "Bangalore",
      "gu": "બેંગલોર",
      "ur": "بنگلور",
      "ar": "بنغالور",
      "ta": "பெங்களூரு",
      "en": "Bengaluru",
      "fr": "Bangalore",
      "bn": "বেঙ্গালুরু",
      "ko": "벵갈루루",
      "kn": "ಬೆಂಗಳೂರು",
      "ms": "Bangalore",
      "be": "বেঙ্গালূরু"
    },
    "lat": 12.9767936,
    "lon": 77.590082,
    "country": "IN",
    "state": "Karnataka"
  }
]
```

---

### 2) Current Weather API

```
https://api.openweathermap.org/data/2.5/weather?lat=12.9767936&lon=77.590082&appid=<API-KEY>
```

**Response**

```json
{
  "coord": {
    "lon": 77.5901,
    "lat": 12.9768
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01n"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 295.56,
    "feels_like": 295.45,
    "temp_min": 294.05,
    "temp_max": 296.66,
    "pressure": 1016,
    "humidity": 61,
    "sea_level": 1016,
    "grnd_level": 918
  },
  "visibility": 6000,
  "wind": {
    "speed": 8.05,
    "deg": 90,
    "gust": 18.33
  },
  "clouds": {
    "all": 5
  },
  "dt": 1770911293,
  "sys": {
    "type": 2,
    "id": 2105374,
    "country": "IN",
    "sunrise": 1770858805,
    "sunset": 1770900871
  },
  "timezone": 19800,
  "id": 6695236,
  "name": "Kanija Bhavan",
  "cod": 200
}
```
