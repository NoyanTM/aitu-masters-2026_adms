# TODO
1. General:
    - unique, required attributes in NOT NULL, nullable FK, optionals
    - meaningful indexes (e.g., booking time per equipment)
    - mormal forms with redundancy eliminaton (3NF, BCNF, etc.)
    - FK ON DELETE / ON UPDATE or cascade deletion (https://docs.sqlalchemy.org/en/20/orm/cascades.html)
    - created_at / decision_ts / time columns TIMESTAMPTZ NOT NULL DEFAULT now()
    - cange generic TEXT to specific size limit depending on domain
    - utc+0 for timezone
    - customizable types with annotated (e.g., BigInteger) https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
1. Entity for `university` and entities within this organization such as department, faculty, etc.
    - Relationship to `laboratory`. On surface, two or more universities do not have same laboratories. Some universities can be without any laboratory at all or exceptional cases when someone shares one laboratory?
    - Relationship to `room`. How to structure relations in such way that we can attach rooms to both `university` and `laboratory`.
    - Relationship to `account`. For example, `university` can have multiple  accounts (students or staff that works or studies at) attached to specific university at once. Can such account attached to multiple universities (e.g., no dual education program and strict regulation to be at one place only)? What about constraint that account of user / person must be registered to university of laboratory (or it is like open laboratory or university for external actors)?
1. Relationship of `project` between `partner` and `resource` should be optional. Also, there should be unique constraint for `partner` and `resource` within same `project` to not have duplicates (e.g. list of same partners within same project).

pdflatex --output-directory=build report.tex
biber ./build/report
pdflatex --output-directory=build report.tex
pdflatex --output-directory=build report.tex

------------------------------------------------------------------------------

Автоматическая генерация и заполнение отчетов с выгрузкой в word, pdf, etc.

preconfigure deply resources in compose, postgres configuration (e.g., max connections, etc.), container for migrations and script, https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs

Аккаунты для студентов и работников университета (и гостей по необходимости - сотрудники смежных организаций / подрядчиков / collaborations)
Общедоступный профиль с описанием (как в социальных сетях): ФИО, email (университетский), описание, фото с ID card (URI/URL link in database, raw file/object is stored in S3 storage (or even IPFS storage?)) и ID если присутствует
Social credit system and biometric identification (with СКУД системой)
Калькулятор и валидатор GPA
Automatically generate complex passwords like in DU

Splash screen in mobile application (react native + expo)
Icons and font (fontawesome)
Animations (for tab bar, pop ups, etc.)
Adaptive design (mobile first?)
Pages: Title/main page, banner с новостной информацией, контент (Основная информация по курсам, каталог курсов и т.д.), footer (нижняя информация - ссылки, наши партнеры и т.д.), registration page, courses page (для курсов платных), resources page (бесплатные ресурсы, новости и т.д.), admin dashboard/panel
Stripe or alternative for оплата товара и тестовый режим (mocks)

Сдача экзаменов и тестирования:
Open source alternative for gptzero and turnitin для поиска плагиаризма и определения формата написания текста (уникальные паттерны, различия ai и human-based, и т.д.). Однако это обходится за счет перефразирования
Поиск и аннулирование ответов скопированные от других (как шейринг флагов в CTF или нарушение правил), для этого необходимо генерировать уникальный флаг/вопрос/вариант ответа специально под определенного студента (для группы/выборки или одного индивида чтобы проверять наличие списывание

Technological stack:
Backend in python (flask, sqlalchemy with multiple engines, alembic migrations)
Frontend (boostrap)
Wireframes in figma and adobe xd
Nginx (webserver), certbot (ssl/tls certificates), dns server, fortivpn

helpdesk and moderation, deadlines, образовательные программы рк, electives major and minor, feedback и передача информация на регулярной основе (то есть не так чтоб за день ДО происходит оповещение а есть составленный календарь и уведомления на регулярной основе), Office Hours, questionnaire, voting system, groups (CS-2103), scheduling system, quizzes, recommendation algorithms (подсказывать какие курсы и темы выбирать в зависимости от оценок и персональных материалов/работ студентов)

keys in csv can be any other (capital or lower case) - need to automatically converted or validated before upload to show that user upload incorrect file format instead of sending raw error without results

/health endpoint {“status”: “ok”} (detailed status of API - работает, все системы работают, некоторые лишь, и т.д. с подробным указанием как status in cloudflare?)

Автоматизация создания отчетности и календарных планов как в DU (вместо сдачи постоянной макулатуры) и загрузка дипломной в той же платформе вместе с презентацией (и чтобы коллегия предварительно ознакомилась с дипломной (это не как предзащиты) а больше как официальная процедура в несколько этапов перед финальной защитой, иначе задают тупые вопросы совершенно не связанные с темой). А также отчетность по производственной практике и т.д.

api key to github - gitleaks
