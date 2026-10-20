# courses-platform

Платформа для подготовки к экзаменам: каталог курсов, просмотр уроков (YouTube / Rutube) и тренажёр заданий с рендерингом формул через MathJax.

## Разработка

### Фронтенд

```bash
pnpm install
pnpm dev
```

Dev-сервер по умолчанию доступен на `http://localhost:5173`. Клиент отправляет API-запросы к локальному бэкенду на `http://localhost:5000/api`.

### Сборка

```bash
pnpm build
pnpm preview
```

## Стек и особенности

- **React 18 + Vite 6** — SPA на базе React Router (`v6`).
- **Tailwind CSS** — утилитарные стили интерфейса.
- **MathJax** (`better-react-mathjax`) — поддержка LaTeX-нотации в условиях задач и пояснениях.
- **Аутентификация** — сессионные куки (`token`, `password`).
- **Бэкенд** — Python / Flask (`Hosting_server_full`), обработка сессий и валидация ответов.


