# Рубрики и виды слайдов

Ключ `rubric` в `post.yaml` задаёт название на плашке. Виды слайдов
(`layout`) можно сочетать свободно, но у каждой рубрики есть порядок по
умолчанию. Лимиты знаков — ориентир; точную проверку делает рендер.

Номер слайда «2/5» и стрелка «листай» ставятся сами.

## Рубрики

| `rubric` | Плашка | Порядок слайдов | Пример |
|---|---|---|---|
| `zhazu-mektebi` | Жазу мектебі | `cover` → `step` × 3–6 → `cta` | `examples/zhazu-mektebi.yaml` |
| `uzindi` | Үзінді | `excerpt_cover` → `excerpt_page` × 1–4 → `continue` | `examples/uzindi.yaml` |
| `aptanyn-kitaby` | Аптаның кітабы | `book` (один слайд) | `examples/aptanyn-kitaby.yaml` |
| `avtor` | Автор | `author_cover` → `text` × 3–5 → `cta` | `examples/avtor.yaml` |
| `dayeksoz` | Дәйексөз | `quote` (один слайд) | `examples/dayeksoz.yaml` |
| `zhanalyq` | Жаңалық | `feature` → `text` × 1–3 → `cta` | `examples/zhanalyq.yaml` |
| `baiqau` | Байқау | `contest` (1 или несколько) | `examples/baiqau.yaml` |
| `sen-ne-deisin` | Сен не дейсің? | `story_question`, `story_post` | `examples/stories.yaml` |

Обложка Reels — `reels_cover` с рубрикой ролика (`examples/reels-cover.yaml`).

## Виды слайдов

Формат 1080 × 1350, кроме отмеченных «сторис» (1080 × 1920).

| `layout` | Фон | Поля (`?` — необязательное) | Лимиты |
|---|---|---|---|
| `cover` | Бирюза | `title`, `subtitle?` | title ≤ 45 знаков, subtitle ≤ 60 |
| `step` | Қағаз | `number?` («01»), `heading`, `body`, `example?`, `example_label?` (по умолч. «Мысал») | heading ≤ 30, body ≤ 160, example ≤ 90 |
| `text` | Қағаз | `heading`, `body` | heading ≤ 50, body ≤ 380 |
| `cta` | Бирюза | `line?`, `button?` (по умолч. слоган и «qazaqnovel.kz») | line ≤ 60 |
| `excerpt_cover` | Қағаз | `quote` (без кавычек — ставятся сами), `work`, `author`, `meta?` («Жанр · N бөлім») | quote ≤ 120 |
| `excerpt_page` | Қағаз | `work`, `chapter?`, `text` (абзацы через пустую строку; реплика с «—» — без отступа) | text ≤ 650 |
| `continue` | Терең | `work`, `author`, `genre?`, `cover?` (картинка 2:3), `heading?`, `button?` | work ≤ 30 |
| `book` | Терең | `work`, `author`, `meta?`, `cover?` | work ≤ 30 |
| `author_cover` | Қағаз | `quote` (без кавычек), `name`, `about?`, `photo?` (квадрат) | quote ≤ 60 |
| `quote` | Бирюза; `variant: teren` — Терең | `text` (без кавычек), `author`, `source?` | text ≤ 150 |
| `feature` | Қағаз + телефон | `title`, `subtitle?`, `screenshot?` (скриншот телефона) | title ≤ 30 |
| `contest` | Лайм | `title`, `rows?` (список `{label, value}`, ≤ 3), `body?`, `button?` | title ≤ 30 |
| `story_question` | Бирюза, сторис | `question`, `label?` | question ≤ 60; ниже — место под стикер опроса |
| `story_post` | Терең, сторис | `image?` (обычно `01.png` поста), `label?`, `line?` | — |
| `reels_cover` | Бирюза, сторис | `title`, `subtitle?` | title ≤ 35 |

Текстовые поля с несколькими абзацами (`body`, `text`) — блок YAML `|-`,
абзацы через пустую строку.

## Поля поста

```yaml
rubric: zhazu-mektebi
date: 2026-10-13          # день публикации
status: draft             # draft → ready → published
slides: [...]
caption: |-               # подпись под постом, см. voice.md
  ...
hashtags: ["#qazaqnovel", "#қазақшажаз", "#жазумектебі"]
consent: "автор, 12.10, Telegram"   # для Үзінді / Автор / цитат авторов сайта
```

`date`, `status`, `consent` рендер не использует — они для плана и учёта.
