# Qazaqnovel.kz · Instagram

Контент Instagram-аккаунта Qazaqnovel.kz: стратегия, дизайн-система,
месячные планы, посты (тексты и готовые PNG) и Claude skill, который их
делает. Код сайта — в отдельном репозитории `dauletra/qazaqnovel`.

## Как пользоваться

Открой сессию Claude Code на этом репозитории и попроси, например:

- «Сделай план на ноябрь»
- «Сделай пост Авторлар мектебі про клиффхэнгер»
- «Сделай Үзінді из этого отрывка» (+ текст, обложка, согласие автора)

Claude пишет текст по-казахски, рисует слайды и кладёт всё в папку поста.
Ты вычитываешь текст, скачиваешь PNG и `caption.txt`, публикуешь.

## Структура

```
docs/plan.md             стратегия: миссия, аудитория, рубрики, ритм, решения
docs/design-system.md    цвета, шрифты, логотип, сетка, компоненты
plan/ГГГГ-ММ.md          план на месяц (шаблон — plan/_template.md)
posts/ГГГГ-ММ/ДД-рубрика-тема/
    post.yaml            текст слайдов, подпись, хэштеги, статус
    01.png, 02.png …     готовые слайды 1080×1350 (сторис — 1080×1920)
    caption.txt          подпись к посту для копирования
    cover.jpg …          исходные картинки (обложка, фото, скриншот)
brand/                   аватар и обложки Highlights — загрузить в Instagram
.claude/skills/instagram-post/   skill: шаблоны, шрифты, логотип, рендер
```

## Рендер вручную

```bash
bash .claude/skills/instagram-post/scripts/render.sh posts/2026-10/13-avtorlar-alghashqy-abzac/post.yaml --sheet
```

Нужны Python 3.11+ и Chromium (Playwright ставит его сам при первом запуске).

## Лицензии

Шрифты Montserrat и Open Sans — SIL Open Font License 1.1. Иконки — Flowbite
Icons, MIT. Логотип — собственность Qazaqnovel.kz.
