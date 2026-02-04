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

how to represent unlimited time period postgres or null time or unspeciefied date https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html#no-default-infinity-dates-handling

configure triggers in alembic migration https://github.com/sqlalchemy/sqlalchemy/discussions/6806

configure timestamp https://www.reddit.com/r/flask/comments/1im57ij/sqlalchemy_is_driving_me_nuts/, https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime

using Base.metadata.create_all to tests sqlalchemy

sqlalchemy to pydantic or dataclass to_dict methods (to_something convention)

sql naming convention

sqlalchemy remove caching of queries

typehinting in IDE when creating instance of object in sqlalchemy
https://www.reddit.com/r/learnpython/comments/1pn0mbi/is_there_a_way_to_get_instance_creation_hints/
https://www.reddit.com/r/SQLAlchemy/comments/14dll1n/proper_type_hinting_or_proper_type_conversion/

auto increment issues
https://stackoverflow.com/questions/5342440/reset-auto-increment-counter-in-postgres
https://til.codeinthehole.com/posts/that-postgres-sequences-arent-restored-after-a-rollback/

configure sessionmaker
https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session
https://stackoverflow.com/questions/72434935/is-sqlalchemy-sessionmaker-thread-safe

https://stackoverflow.com/questions/378331/physical-vs-logical-hard-vs-soft-delete-of-database-record

https://stackoverflow.com/questions/7786207/whats-the-difference-between-a-fixture-and-a-factory-in-my-unit-tests

https://github.com/thoughtbot/factory_bot
https://stackoverflow.com/questions/23349772/why-is-factory-boy-superior-to-using-the-orm-directly-in-tests

https://softwareengineering.stackexchange.com/questions/280324/is-it-better-to-make-database-calls-or-external-api-calls-first-in-the-context-o

https://github.com/francoisnt/seedlayer/tree/main

1. Entity for `university` and entities within this organization such as department, faculty, etc.
    - Relationship to `laboratory`. On surface, two or more universities do not have same laboratories. Some universities can be without any laboratory at all or exceptional cases when someone shares one laboratory?
    - Relationship to `room`. How to structure relations in such way that we can attach rooms to both `university` and `laboratory`.
    - Relationship to `account`. For example, `university` can have multiple  accounts (students or staff that works or studies at) attached to specific university at once. Can such account attached to multiple universities (e.g., no dual education program and strict regulation to be at one place only)? What about constraint that account of user / person must be registered to university of laboratory (or it is like open laboratory or university for external actors)?
1. Relationship of `project` between `partner` and `resource` should be optional. Also, there should be unique constraint for `partner` and `resource` within same `project` to not have duplicates (e.g. list of same partners within same project).
1. `project`:
    - budget, duration (from, to), supervisor, funding source, ИРН, and other multiple fields/tables
    - content cards in {"en": {}, "ru": {}, "kk": {}} (about_fields as list, tags, info, banner, slogan)
    - consortium or some form of collaboration between multiple organization (laboratory many-to-many project), but for now, we assume that two or many laboratories do not have same research projects (laboratory one-to-many project), so laboratory_id is mandatory field, because project must be attached to one of them
1. `project_resource`:
    - mark publications as optional in m2m, because they appear only after some time
1. `project_participant`:
    - optional many to many
    - role within project (руководитель, исполнитель, и т.д.)
    - history of activity of the participant
    - rename to i.e., team member, contributer, etc.?
    - constraint to check if person within same laboratory of the project, but external consultant can also be part of project
1. `room`:
    - Geometric shape and coordinates in postgis
    - Currenly,  two or more laboratories do not share same space (laboratory one-to-many room). But it should be many-to-many to clearly represent cases with external rental spaces. 
    - Also, need to research about possibility of digital laboratories without any physical space within law and regulations of Kazakhstan.
1. `resource`:
    - how to mention or attach participants and authors in reasonable way
    - class ResourceType as enum?
    - автоматическая генерация и заполнение отчетов с выгрузкой в word, pdf, etc.
1. `presentation`:
    - quality or resolution and other additional fields (VideoPresentation, AudioPresentation, more detailed types)
    - compatiblity with standard transcription software for subtitles
1. `software_repository`:
    - self-referencing to related / similar repositories or precomputed/cached query for percent of similarity
1. `dataset`:
    - calculated fields for columns_amount and rows_amount
1. `account`:
    - decompose to multiple full_name to (first_name, middle_name, etc.)
    - tag, username, and other fields
    - role within system (moderator, administrator) must be seperated from role within organization
1. `profile`:
    - define posts as external table
    - fields for age, gender, external links, ...
    - some personal information are hidden depending on role and visibility configuration like in Steam profile?
1. `equipment`:
    - generated qr code or bar code
    - inventory_code like SKU (https://en.wikipedia.org/wiki/Stock_keeping_unit)
    - decompose to inventory, supply, or assets like in professional inventory management and accounting system
    - Some categories of equipment and instances need additional approval requirements (conditions/rules to when, how, why to approve/disapprove). For example, approval by approver (staff member with specific role/position, privilege, areas of responsibility within laboratory, multi-step approval), who is responsible for changing status and management on regular basis. Maybe, laboratory participants can report and message to him about incidents with equipment. Also, approval requirements can define specific days / schedule / time (e.g., working schedule of laboratory or time restrictions).
    - Approval_requirements are embedded to specific instance of equipment(laboratory can reconfigure it for their own cases independently), or by equipment_type, or both have affection on it?
1. `booking`:
    - booking for unlimited time (null, time infinite, empty field)?
    - bidirectional connection for queries account ||--|{ booking, equipment ||--|{ booking
1. Misc:
    - Автоматизация создания отчетности и календарных планов как в DU (вместо сдачи постоянной макулатуры) и загрузка дипломной в той же платформе вместе с презентацией (и чтобы коллегия предварительно ознакомилась с дипломной (это не как предзащиты) а больше как официальная процедура в несколько этапов перед финальной защитой, иначе задают глупые вопросы совершенно не связанные с темой). А также отчетность по производственной практике и т.д.
    - Сдача экзаменов и тестирования: Open source alternative for gptzero and turnitin для поиска плагиаризма и определения формата написания текста (уникальные паттерны, различия ai и human-based, и т.д.). Однако это обходится за счет перефразирования. Поиск и аннулирование ответов скопированные от других (как шейринг флагов в CTF или нарушение правил), для этого необходимо генерировать уникальный флаг/вопрос/вариант ответа специально под определенного студента (для группы/выборки или одного индивида чтобы проверять наличие списывание).
    - helpdesk and moderation, deadlines, образовательные программы рк, electives major and minor, feedback и передача информация на регулярной основе (то есть не так чтоб за день ДО происходит оповещение а есть составленный календарь и уведомления на регулярной основе), Office Hours, questionnaire, voting system, groups (CS-2103), scheduling system, quizzes, recommendation algorithms (подсказывать какие курсы и темы выбирать в зависимости от оценок и персональных материалов/работ студентов)
    - Аккаунты для студентов и работников университета (и гостей по необходимости - сотрудники смежных организаций / подрядчиков / collaborations)
    - Общедоступный профиль с описанием (как в социальных сетях): ФИО, email (университетский), описание, фото с ID card (URI/URL link in database, raw file/object is stored in S3 storage (or even IPFS storage?)) и ID если присутствует
    - Social credit system and biometric identification (with СКУД системой), Калькулятор и валидатор GPA, Automatically generate complex passwords like in DU
    - Other features: splash screen in mobile application, icons and font, animations (for tab bar, pop ups, etc.), adaptive design like mobile first
    - Pages: Title/main page, banner с новостной информацией, контент (Основная информация по курсам, каталог курсов и т.д.), footer (нижняя информация - ссылки, наши партнеры и т.д.), registration page, courses page (для курсов платных), resources page (бесплатные ресурсы, новости и т.д.), admin dashboard/panel
    Technological stack: stripe or alternative for оплата товара и тестовый режим (mocks), Frontend (boostrap), wireframes in figma and adobe xd, dns server, fortivpn

------------------------------------------------------------------

CHECK the same equipment cannot be booked foroverlapping time intervals

 approval.booking_id → ON DELETE CASCADE
 usage_log.booking_id → ON DELETE CASCADE
 booking.requester_id → RESTRICT (recommended) or CASCADE (only if justified)

# constraint for same equipment cannot be booked for approval state is embedded to booking (not as other table)
 Partial UNIQUE: allow only one active approval per booking (if not already UNIQUE):
 CREATE UNIQUE INDEX ux_approval_booking ON approval(booking_id);
Exclude overlap: prevent overlapping bookings per equipment:
 CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE booking
 ADD CONSTRAINT booking_no_overlap
 EXCLUDE USING gist (
 equipment_id WITH =,
 tstzrange(start_ts, end_ts, '[)') WITH &&
 )
 WHERE (status IN ('requested','approved'));

add constraint that account of user must belong to laboratory 
of equipment to book one or more equipment 

add constraint that limit of possible equipments per
person to specific amount (for example, 5 at time)
