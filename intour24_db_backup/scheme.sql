--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

-- Started on 2017-06-01 09:34:32

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2352 (class 1262 OID 16394)
-- Dependencies: 2351
-- Name: intour24; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE intour24 IS 'Main database';


--
-- TOC entry 1 (class 3079 OID 12387)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2354 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 202 (class 1259 OID 24689)
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE category_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 201 (class 1259 OID 24681)
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE category (
    id integer DEFAULT nextval('category_id_seq'::regclass) NOT NULL,
    name character varying
);


ALTER TABLE category OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 24736)
-- Name: excursion_property_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE excursion_property_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE excursion_property_id_seq OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 24728)
-- Name: excursion_property; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE excursion_property (
    id integer DEFAULT nextval('excursion_property_id_seq'::regclass) NOT NULL,
    name character varying,
    image character varying
);


ALTER TABLE excursion_property OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 24635)
-- Name: excursions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE excursions_id_seq
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE excursions_id_seq OWNER TO postgres;

--
-- TOC entry 185 (class 1259 OID 16411)
-- Name: excursions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE excursions (
    id integer DEFAULT nextval('excursions_id_seq'::regclass) NOT NULL,
    name character varying(200),
    description text,
    capacity integer,
    is_picking boolean,
    average_rating real,
    duration text,
    category_id integer,
    picking_place_id integer,
    operator_id integer,
    link_to_site character varying,
    images character varying[],
    price_id integer
);


ALTER TABLE excursions OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24847)
-- Name: excursions_excursion_property_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE excursions_excursion_property_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE excursions_excursion_property_id_seq OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24832)
-- Name: excursions_excursion_property; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE excursions_excursion_property (
    id integer DEFAULT nextval('excursions_excursion_property_id_seq'::regclass) NOT NULL,
    excursion_id integer,
    excursion_property_id integer
);


ALTER TABLE excursions_excursion_property OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24829)
-- Name: excursions_sights_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE excursions_sights_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE excursions_sights_id_seq OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24814)
-- Name: excursions_sights; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE excursions_sights (
    id integer DEFAULT nextval('excursions_sights_id_seq'::regclass) NOT NULL,
    excursion_id integer,
    soght_id integer
);


ALTER TABLE excursions_sights OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 24776)
-- Name: group_tourist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE group_tourist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE group_tourist_id_seq OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 24761)
-- Name: group_tourist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE group_tourist (
    id integer DEFAULT nextval('group_tourist_id_seq'::regclass) NOT NULL,
    tourist_id integer,
    group_id integer
);


ALTER TABLE group_tourist OWNER TO postgres;

--
-- TOC entry 193 (class 1259 OID 24638)
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: intour24_admin
--

CREATE SEQUENCE groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE groups_id_seq OWNER TO intour24_admin;

--
-- TOC entry 190 (class 1259 OID 16611)
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE groups (
    id integer DEFAULT nextval('groups_id_seq'::regclass) NOT NULL,
    tour_date timestamp with time zone,
    reserved integer,
    excursion_id integer,
    guide_id integer,
    capacity integer
);


ALTER TABLE groups OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 24641)
-- Name: guides_id_seq; Type: SEQUENCE; Schema: public; Owner: intour24_admin
--

CREATE SEQUENCE guides_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE guides_id_seq OWNER TO intour24_admin;

--
-- TOC entry 188 (class 1259 OID 16429)
-- Name: guides; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE guides (
    id integer DEFAULT nextval('guides_id_seq'::regclass) NOT NULL,
    first_name character varying(60),
    email character varying(40),
    phone character varying(20),
    average_rating double precision,
    last_name character varying
);


ALTER TABLE guides OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 24700)
-- Name: operator_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE operator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE operator_id_seq OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 24692)
-- Name: operator; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE operator (
    id integer DEFAULT nextval('operator_id_seq'::regclass) NOT NULL,
    name character varying,
    phone character varying,
    address character varying,
    logo character varying
);


ALTER TABLE operator OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 24643)
-- Name: picking_places_id_seq; Type: SEQUENCE; Schema: public; Owner: intour24_admin
--

CREATE SEQUENCE picking_places_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE picking_places_id_seq OWNER TO intour24_admin;

--
-- TOC entry 186 (class 1259 OID 16419)
-- Name: picking_places; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE picking_places (
    id integer DEFAULT nextval('picking_places_id_seq'::regclass) NOT NULL,
    name character varying(60),
    geoposition character varying(50)
);


ALTER TABLE picking_places OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24866)
-- Name: prices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE prices (
    id integer NOT NULL,
    price_for_children integer,
    price_for_adult integer,
    price_for_enfant integer
);


ALTER TABLE prices OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 24647)
-- Name: ratings_id_seq; Type: SEQUENCE; Schema: public; Owner: intour24_admin
--

CREATE SEQUENCE ratings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ratings_id_seq OWNER TO intour24_admin;

--
-- TOC entry 191 (class 1259 OID 16641)
-- Name: ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE ratings (
    id integer DEFAULT nextval('ratings_id_seq'::regclass) NOT NULL,
    excursion_id integer,
    guide_id integer,
    excursion_rate integer,
    guide_rate integer,
    feedback text
);


ALTER TABLE ratings OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 24666)
-- Name: schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: intour24_admin
--

CREATE SEQUENCE schedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE schedule_id_seq OWNER TO intour24_admin;

--
-- TOC entry 199 (class 1259 OID 24661)
-- Name: schedule; Type: TABLE; Schema: public; Owner: intour24_admin
--

CREATE TABLE schedule (
    id integer DEFAULT nextval('schedule_id_seq'::regclass) NOT NULL,
    start_date timestamp with time zone,
    repeat_interval integer,
    repeat_weekday integer,
    repeat_week integer,
    end_date timestamp with time zone,
    excursion integer NOT NULL,
    repeat_year integer,
    repeat_month integer,
    repeat_day integer
);


ALTER TABLE schedule OWNER TO intour24_admin;

--
-- TOC entry 206 (class 1259 OID 24725)
-- Name: sight_property_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sight_property_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sight_property_id_seq OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 24717)
-- Name: sight_property; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sight_property (
    id integer DEFAULT nextval('sight_property_id_seq'::regclass) NOT NULL,
    name character varying,
    image character varying
);


ALTER TABLE sight_property OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 24754)
-- Name: sight_sight_property_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sight_sight_property_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sight_sight_property_id_seq OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 24739)
-- Name: sight_sight_property; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sight_sight_property (
    id integer DEFAULT nextval('sight_sight_property_id_seq'::regclass) NOT NULL,
    sight_id integer,
    sight_property_id integer
);


ALTER TABLE sight_sight_property OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 24645)
-- Name: sights_id_seq; Type: SEQUENCE; Schema: public; Owner: intour24_admin
--

CREATE SEQUENCE sights_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sights_id_seq OWNER TO intour24_admin;

--
-- TOC entry 187 (class 1259 OID 16424)
-- Name: sights; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sights (
    id integer DEFAULT nextval('sights_id_seq'::regclass) NOT NULL,
    name character varying(60),
    geoposition character varying(50),
    images character varying(70)[],
    description text,
    cover character varying
);


ALTER TABLE sights OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 24649)
-- Name: tourists_id_seq; Type: SEQUENCE; Schema: public; Owner: intour24_admin
--

CREATE SEQUENCE tourists_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tourists_id_seq OWNER TO intour24_admin;

--
-- TOC entry 189 (class 1259 OID 16434)
-- Name: tourists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE tourists (
    id integer DEFAULT nextval('tourists_id_seq'::regclass) NOT NULL,
    first_name character varying(60),
    email character varying(40),
    phone character varying(20),
    last_name character varying
);


ALTER TABLE tourists OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 24795)
-- Name: transport_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE transport_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transport_id_seq OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 24782)
-- Name: transport; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE transport (
    id integer DEFAULT nextval('transport_id_seq'::regclass) NOT NULL,
    capacity integer,
    number character varying,
    group_id integer
);


ALTER TABLE transport OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 24811)
-- Name: transport_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE transport_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transport_type_id_seq OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 24798)
-- Name: transport_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE transport_type (
    id integer DEFAULT nextval('transport_type_id_seq'::regclass) NOT NULL,
    name character varying,
    transport_id integer
);


ALTER TABLE transport_type OWNER TO postgres;

--
-- TOC entry 2326 (class 0 OID 24681)
-- Dependencies: 201
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY category (id, name) FROM stdin;
\.


--
-- TOC entry 2355 (class 0 OID 0)
-- Dependencies: 202
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('category_id_seq', 1, false);


--
-- TOC entry 2332 (class 0 OID 24728)
-- Dependencies: 207
-- Data for Name: excursion_property; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY excursion_property (id, name, image) FROM stdin;
\.


--
-- TOC entry 2356 (class 0 OID 0)
-- Dependencies: 208
-- Name: excursion_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('excursion_property_id_seq', 1, false);


--
-- TOC entry 2310 (class 0 OID 16411)
-- Dependencies: 185
-- Data for Name: excursions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY excursions (id, name, description, capacity, is_picking, average_rating, duration, category_id, picking_place_id, operator_id, link_to_site, images, price_id) FROM stdin;
7	Экскурсия в Елабугу + обед	Елабуга — второй по значимости город в Республике Татарстан, обладающий уникальным историко-культурным наследием. Великолепная и неповторимая Елабуга приглашает вас в гости! Ощутите уют и очарование старинного купеческого города! Вдохните воздух шишкинских лесов, прикоснитесь к седой старине в многочисленных музеях Елабуги.\r\nВы увидите:\r\n- «Чертово» городище и его таинственную башню — свидетели событий средневековья\r\n- Шишкинские пруды – парк над долиной реки Тоймы\r\n- площадь Тысячелетия Елабуги\r\n- Спасский собор XIX века\r\n- улицу Казанскую, где расположились пышные купеческие особняки купцов-миллионеров\r\n- епархиальное училище – памятник благотворительной деятельности Елабужских купцов\r\n- Петропавловское кладбище, где захоронена М.И. Цветаева\r\n- Александровский сад, заложенный в Елабуге в честь коронации императора Александра II\r\n- Памятник кавалерист-девице Дуровой Н.А.\r\nЭкскурсия в музеи: \r\n- Мемориальный музей И.И. Шишкина расскажет Вам о жизни великого художника и его семье;\r\n- Дом памяти М.И. Цветаевой – здесь прошли последние дни жизни великой поэтессы Серебряного века.\r\nПитание:\r\nКомплексный обед\r\nВ стоимость включено: проезд на новых автобусах, входные билеты в музеи, экскурсионное обслуживание профессиональными гидами, обед.	\N	f	\N	12 часов	\N	\N	\N	\N	\N	\N
12	Экскурсия Казань в парках с посещением усадьбы Сандецкого	Автобусно - пешеходная экскурсия «Казань в парках с посещением усадьбы Сандецкого». Как и все большие города, Казань немыслима без зелёных насаждений, обилия парков и скверов. Они богемные и демократичные. История казанских парков — двухсотлетняя. До этого, в XVII веке в России вообще не было понятия «парк». То есть, были парки, но царские, боярские. Первый общественный парк, который возник в Казани в начале XIX века — Чёрное озеро. А частные парки в Казани появились еще в XVIII веке. (например, Лядской, Николаевский садики). В этих парках гуляли наши бабушки под звуки духового оркестра, здесь назначали свидания и деловые встречи, а сегодня обновленные парки встречают горожан и гостей города прохладой от летнего зноя и необычными историями из прошлого. \r\nУсадьба Сандецкого. Бывший дом командующего войсками Казанского военного округа генерала Сандецкого, представляет собой исторический памятник архитектуры конца XIX века. Сегодня в этом изящном парадном здании расположен музей изобразительных искусств РТ. Стены особняка украшает богатейшая коллекция икон и живописных полотен Рокотова, Айвазовского, Брюллова, Крамского, Репина, Шишкина, Левитана, Кустодиева, Фешина. В начале века во дворе дома был разбит регулярный парк с беседками и фонтаном. Здание усадьбы и сохранившийся парк – одно из красивейших мест в Казани. Пожалуй, это единственное место, где собирается казанская интеллигенция на ежегодный джазовый фестиваль. Посещение парковой зоны. Фотографии на память «В усадьбе генерала Сандецкого».\r\nВы увидите:\r\n- сквер Лобачевского в окружении дворянских особняков\r\n- парк «Черное озеро» и его история\r\n- утопающий в зелени Ленинский садик\r\n- Лядской сад. В честь кого он назван? И почему здесь памятник Державину?\r\n- Сквер Толстого и сквер К. Фукса. Памятники, история….\r\nЭкскурсия в музеи:\r\nУсадьба Сандецкого. В этом изящном парадном здании расположен музей изобразительных искусств РТ.\r\n- Посещение парковой зоны. Фотографии на память «В усадьбе генерала Сандецкого».\r\nВ стоимость включено: проезд на новых автобусах, входные билеты в музей, экскурсионное обслуживание профессиональными гидами	\N	f	\N	5 часов	\N	\N	\N	\N	\N	\N
1	Экскурсия по Казани + Казанский Кремль	Данная экскурсия даст вам наиболее полное представление о Казани и ее достопримечательностях. Вы отправитесь в увлекательное путешествие по историческим местам Казани. Во время этой экскурсии Вы сможете насладиться самобытной красотой столицы Татарстана, увидеть своими глазами яркие краски ее улиц и площадей, узнать, где хранятся несметные сокровища Казанских ханов и где закипел без огня котел. Прикоснитесь к вековой истории древнего города. \r\nВы увидите: \r\n- Старо-татарскую слободу со старинными татарскими мечетями;\r\n- овеянное легендами озеро Кабан;\r\n- здание – парусник Татарского академического театра им Г. Камала;\r\n- татарскую деревню «Туган Авылым»;\r\n- сказочный дворец - театр кукол «Экият»;\r\n- Казанский Университет;\r\n- площадь Свободы – культурный и административный центр Казани;\r\n- Богородицкий монастырь и его святыня Казанская икона Божией Матери;\r\n- Казанский Кремль;\r\n- Спасскую башню – главные ворота Кремля;\r\n- мечеть Кул Шариф – главную мечеть города и республики;\r\n- корпус Юнкерского училища;\r\n- Благовещенский собор;\r\n- пушечный двор;\r\n- резиденцию президента РТ (губернаторский дворец);\r\n- символ Казани - знаменитую «падающую» башню ханши Сююмбике.\r\nВ стоимость включено: проезд на новых автобусах, входные билеты в Кремль, экскурсионное обслуживание профессиональными гидами.	\N	f	\N	4 часа	\N	\N	\N	\N	\N	\N
4	Экскурсия в Болгар (Северная Мекка) + обед	Экскурсия в Болгар (с обедом). С посещением музея Болгарской цивилизации и Белой мечети. \r\n\r\nБолгарское городище - столица одного из ранних государственных объединений Восточной Европы. Болгарский историко-архитектурный комплекс самый северный в мире памятник средневекового мусульманского зодчества, включен в список всемирного наследия ЮНЕСКО. Болгар – святое для поволжских татар место. Здесь в 922 г. был принят ислам в качестве официальной государственной религии. \r\nВы увидите: \r\n- Соборную мечеть и Большой Минарет – центр архитектурного ансамбля\r\n- Восточный мавзолей - мусульманская усыпальница\r\n- Северный мавзолей – символ болгарского городища\r\n- Ханскую усыпальницу и Малый Минарет – святые места памяти предков\r\n- Черную палату - народная память связала её название с красивой легендой о болгарской царевне Алтынчеч, которая бросилась с крыши здания, отказавшись выйти замуж за золотоордынского хана\r\n- Белую Мечеть - одно из самых значительных сооружений, пополнивших современную коллекцию архитектурного наследия Татарстана. Белая чинность строения, придает мечети сходство с индийским Тадж-Махалом. \r\nЭкскурсия в музеи: \r\n-Музей Болгарской цивилизации – экспозиция музея повествует о жизни болгарского народа – предков современных казанских татар;\r\n-Памятный знак – здесь хранится самый большой печатный Коран в мире. \r\nПитание:\r\nКомплексный обед\r\nВ стоимость включено: проезд на новых автобусах, входные билеты в музеи, экскурсионное обслуживание профессиональными гидами, обед.	\N	f	\N	11 часов	\N	\N	\N	\N	\N	\N
14	Экскурсия "Слияние рек в слиянии культур"	Экскурсия «Слияние рек в слиянии культур». По берега больших и малых рек нашего края издавна жили народы. Поездка по древнему Ногайскому тракту, окунет вас во всю прелесть природных красот и традиций исторических поселений. Два села – две этнические культуры. \r\nВы увидите:\r\n- ансамбль «Каравон» встретит вас русскими народными песнями своей родины, хлебом-солью, вовлечет в озорной хоровод. \r\n- ансамбль «Сурэкэ» удивят необычными музыкальными инструментами и задушевными напевами, берущими истоки еще со времен крещения татар Иваном Грозным.\r\nПитание: \r\nВас ждет у слияния прекрасных рек Волги, Меши и Камы удивительный обед из разных сортов свежепойманной рыбы, рецепты приготовления которой хранятся в секрете у местных кулинаров.\r\nВ стоимость включено: проезд на новых автобусах, экскурсионное обслуживание профессиональными гидами, обед	\N	f	\N	6 часов	\N	\N	\N	\N	\N	\N
5	Экскурсия в Свияжск + Храм всех религий	Свияжск – это историко-культурная жемчужина Республики Татарстан. Крепость, построенная в правление Ивана Грозного в месте слияния рек Волги и Свияги, служила военным форпостом в Поволжье и местом подготовки военных частей для похода на неприступную ханскую Казань. Со временем, утратив значение военной крепости, Свияжск – духовный центр Среднего Поволжья. Позднее судьба Свияжска сложилась так, что все переломные моменты отечественной истории, как в капле воды отразились в маленьком Свияжске. Сегодня памятники архитектуры и истории объединены в государственный музей «Остров-град Свияжск». \r\nВселенский храм, Международный культурный центр духовного единения — архитектурное сооружение, возведение которого начато в 1994 году художником, архитектором, скульптором, целителем и общественным деятелем Ильдаром Хановым. По замыслу автора и владельца комплекса, он сооружён как архитектурный символ религий, культур и цивилизаций. Службы и обряды в комплексе не проводятся. В ансамбле соседствуют православная церковь, мусульманская мечеть, иудейская синагога, буддийская пагода. \r\nВы увидите:\r\n- Церковь Живоначальной Троицы – единственная сохранившаяся постройка деревянной крепости 16 в. со времён Ивана Грозного;\r\n- Церковь во имя Сергия Радонежского покровителя острова;\r\n- Собор "Всех Скорбящих Радости" - величественный пятиглавый храм в русско - византийском стиле;\r\n- действующий Успенский монастырь с его архитектурным ансамблем 17 века и уникальными фресками;\r\n- Рождественская площадь – главная площадь Свияжска;\r\n- конный двор и Ленивый Торжок – сувениры, мастера – ремесленники;\r\n- Храм всех религий.\r\nВ стоимость включено: проезд на новых автобусах, экскурсионное обслуживание профессиональными гидами, входные билеты в Свияжск.	\N	f	\N	5 часов	\N	\N	\N	\N	\N	\N
6	Экскурсия в Раифу + Храм всех религий	Экскурсия «Овеянная легендами земля» в Раифский Богородицкий мужской монастырь с осмотром Храма Всех Религий. Расположенный в 30 км. от Казани, в заповедном лесу на берегу дивной красоты озера, Монастырь основан в 17 веке. Его архитектурный ансамбль - один из самых величественных в среднем Поволжье складывался в течение столетий. \r\nВы увидите: \r\n- Церковь во имя Святых преподобных Отцов в Синае и Раифе избиенных, от которой и произошло название монастыря;\r\n- Церковь Веры, Надежды, Любови и матери их Софии;\r\n- Собор Троицы Живоначальной (Троицкий собор);\r\n- Собор Грузинской иконы Божьей Матери, где находится святыня монастыря - чудотворный Грузинский образ пресвятой Богородицы;\r\n- Озеро Раифское, «неквакующие» лягушки, великолепный сосновый лес;\r\n- Пение монастырского квартета «Притча»;\r\n- Вода из освященного патриархом источника.\r\nВ стоимость включено: проезд на новых автобусах, обслуживание профессиональными гидами, вход на территорию монастыря.	\N	f	\N	4 часа	\N	\N	\N	\N	\N	\N
11	Экскурсия в Кремль (Казанский)	Посещение Казанского Кремля, главной достопримечательности города, памятника всемирного наследия ЮНЕСКО. \r\nВы увидите: \r\n- Спасскую башню – главные ворота Кремля;\r\n- мечеть Кул Шариф – главную мечеть города и республики;\r\n- корпус Юнкерского училища;\r\n- Благовещенский собор;\r\n- пушечный двор;\r\n- резиденцию президента РТ (губернаторский дворец);\r\n- символ Казани - знаменитую «падающую» башню ханши Сююмбике.\r\nВ стоимость включено: экскурсионное обслуживание профессиональными гидами, входные билеты в Казанский Кремль.	\N	f	\N	1 час 30 минут	\N	\N	\N	\N	\N	\N
9	Экскурсия в Йошкар-Олу + обед	Йошкар-Ола — столица Республики Марий Эл. В последнее десятилетие Йошкар-Ола преобразилась: центр фактически отстроен заново. Поэтому мы едем в Марий Эл прежде всего не за историей пыльных веков, а за тем, чтобы увидеть современную жизнь главного города этой республики. \r\n\r\nВ Йошкар-Оле вы увидите:\r\n- площадь им. Оболенского-Ноготко;\r\n- самые точные марийские часы – «часы с осликом» на здании художественной галереи\r\n- памятник основателю города Оболенскому-Ноготкову;\r\n- копию Царь-пушки;\r\n- памятник Священномученику Епископу Марийскому Леониду;\r\n- восемь минут Евангельского чуда - часы с движущимися фигурами святых апостолов;\r\n- набережную Амстердам со скульптурными композициями и памятниками известным деятелям искусств;\r\n- Благовещенскую башню с боем курантов;\r\n- вы посидите на лавочке с Йошкиным котом и прогуляетесь по «Итальянскому парку\r\nЭкскурсия в музеи: \r\n- национальный музей Марийского народа. \r\nПитание: \r\nОбед - национальная Марийская кухня. \r\nВ стоимость включено: проезд на новых автобусах, входные билеты в музеи, обслуживание профессиональными гидами, национальный обед.	\N	f	\N	11 часов	\N	\N	\N	\N	\N	\N
10	Экскурсия по Казани (обзорная)	Данная экскурсия даст вам наиболее полное представление о Казани и ее достопримечательностях. Вы отправитесь в увлекательное путешествие по историческим местам Казани. На этой экскурсии вы сможете насладиться самобытной красотой древней столицы города Казани, увидеть своими глазами яркие краски ее улиц и площадей, узнать, где хранятся несметные сокровища Казанских ханов и где закипел без огня котел. Прикоснитесь к вековой истории древнего города!\r\n\r\nВы увидите:\r\n\r\n- Старо-татарскую слободу со старинными татарскими мечетями;\r\n- овеянное легендами озеро Кабан;\r\n- здание – парусник Татарского академического театра им Г. Камала;\r\n- татарскую деревню «Туган Авылым»;\r\n- сказочный дворец - театр кукол «Экият»;\r\n- Казанский Университет;\r\n- площадь Свободы – культурный и административный центр Казани;\r\n- Богородицкий монастырь и его святыня Казанская икона Божией Матери.\r\nВ стоимость включено: проезд на новых автобусах, экскурсионное обслуживание профессиональными гидами.	\N	f	\N	2 часа 30 минут	\N	\N	\N	\N	\N	\N
16	Экскурсия в крепость "Старая Казань"	Экскурсия в крепость "Старая Казань". Посещение Иске-Казанского государственного историко-культурного и природного музея-заповедника. \r\nВ 45 км от современной Казани, на священном во всем Заказанье месте, располагается целый комплекс археологических и природных объектов, входящих в охранную зону заповедника. \r\nУчастие в мастер – классе по вышивке бисером «Казанская тюбетейка». Вы попробуйте себя в роли средневекового лучника, участие в соревновании по стрельбе из лука на звание «Лучший лучник Иске Казан». Выступление татарского ансамбля "Нурлы Казан", состоящего из бабушек, исполнение национальных песен.\r\n\r\nВы увидите:\r\n- реконструированный историко-культурный и ремесленный комплекс периода Казанского ханства\r\n- поднявшись на стены крепости, вы почувствуете себя жителем древнего города\r\n- старинные орудия, при помощи которых обороняли древний город\r\nЭкскурсия в музей: \r\nэтнографический музей - раскроет взаимосвязь между современной Казанью и Иске Казан (Старая Казань).\r\nВ стоимость включено: проезд на новых автобусах, входные билеты в музей, участие в мастер-классе по вышивке бисером, стрельба из лука, обслуживание профессиональными гидами	\N	f	\N	4 часа	\N	\N	\N	\N	\N	\N
17	Татарские пляски (ТАТАР БИЮЛЯРЕ)	Уникальная интерактивная программа «Татар биюляре» познакомит гостей Татарстана с танцевальными движениями, этикетом, музыкальными инструментами, одеянием и конечно же со знаменитой татарской плясовой музыкой.\r\nСпециально для программы «Татар биюлярэ» были сшиты женские и мужские национальные костюмы. Во время изучения всех премудростей, этикета и хитростей татарского танца, туристы переодеваются в костюмы, что позволяет максимально погрузиться в атмосферу безудержного веселья под зажигательные ритмы гармониста.\r\nЧто бы были силы у туристов для ритмичных танцев, программа начинается с национального ужина. Во время застолья артисты начнут шоу программу, а после трапезы все гости переодеваются в национальные костюмы и присоединяются к артистам. Профессиональные артисты театров Татарстана за час научат танцевать и подарят массу хороших впечатлений и ярких фотографий каждому туристу.\r\nВ стоимость включено: участие в интерактивной программе с переодеванием в национальные костюмы, ужин в национальном стиле.	\N	f	\N	1 час 30 минут	\N	\N	\N	\N	\N	\N
2	Экскурсия в Раифу + Храм Всех Религий + Свияжск	Загородная экскурсия включает осмотр по трассе Храма-памятника воинам, погибшим во время взятия Казани в 1552 г.\r\nОстров-град Свияжск на «Круглой горе», которую облюбовал Иван Грозный зимой 1550 года, и весной 1551 г. выстроил здесь город, ставший центром православия Поволжья, сохранил уникальные памятники истории и архитектуры. В окружении природного ландшафта являет собой уникальный образец единения природы и общества, сказочно чарующей красоты. Не было в России уголка, где бы на 1 кв. м. приходилось столько церквей и монастырей. Обзор Церкви Живоначальной Троицы, Церкви во имя Сергия Радонежского, Собора «Всех Скорбящих Радости» (посещение), Собора Успения Пресвятой Богородицы, Церкви во имя Николы Чудотворца, Церкви во имя святых царей Константина и Елены. После экскурсии предоставляется время на отдых, самостоятельный обед , приобретение сувениров (1 час).\r\nРаифский Богородицкий монастырь, расположенный в 30 км от Казани, в заповедном лесу, на берегу прекрасного лесного озера. Монастырь основан в 17 веке. Его архитектурный ансамбль — один из самых величественных в среднем Поволжье складывался в течении столетий. Основной святыней монастыря является чудотворный Грузинский образ Пресвятой Богородицы (XVII в). На территории монастыря расположен освещенный патриархом святой источник.\r\n«Храм всех религий». В основе – идея о том, что все религии Мира — едины. Все они ведут к свету и добру. Это – смелая идея соединить в одном архитектурном строении, казалось бы, не сочетаемое. Комплекс объединяет 16 Мировых религий (в том числе и исчезнувших). \r\nВ стоимость включено: проезд на новых автобусах, входные билеты в музеи, обслуживание профессиональными гидами.	\N	f	\N	8 часов	\N	\N	\N	\N	\N	\N
18	Гостеприимный Дом Бая	Авторская интерактивная программа «Гостеприимный дом Бая» на сегодня является уникальной в своем роде на туристическом рынке Казани.\r\nВсех гостей Казани непременно приглашаем в гости, в главный дом татарского села - дом Бая. Состоятельные хозяева дома - Эбика и Бабай раскроют множество секретов из уклада жизни, обычаев и традиций татарского народа.\r\nГости разделяются на 2 группы и располагаются за столами в мужской и женской половинах дома. За столом, за сытным обедом или ужином из национальных блюд (суп Токмач, Чак-чак, Перемяч, Треугольник, Кыстыбый, Кош теле, Коймак) дорогим гостям Эбика и Бабай расскажут о любимых блюдах татарского народа через сказания и легенды.\r\nУвлекательные рассказ в музыкальном сопровождении раскроет интересные элементы национальных праздников летнего и зимнего солнцестояния - Навруз, Нардуган, Сабантуй и других праздников.\r\nСамым сокровенным и интересным в завершении вечера станет знакомство через игру актеров с национальными традициями и обычаями татарского народа. Вас ждут знакомства с понятиями Су юлы, Аулок Ой, Никах, Бэби Туе, а также интересные застольные игры.\r\nВ стоимость включено: обед из национальных татарских блюд, участие в интерактивной программе.	\N	f	\N	1 час 30 минут	\N	\N	\N	\N	\N	\N
3	Экскурсия ночная Казань - "Огни Казани"	Ночная экскурсия «Огни Казани» А знаете ли вы, как освещались улицы Казани до того, как появилось электричество? Нет? Если после насыщенной экскурсионной программы вы еще полны сил и хотите увидеть другую Казань, и услышать про другую Казань, приглашаем вас окунуться в сказочный облик ночной столицы. Перед вами предстанет Казань, затихшая и умиротворенная, вся в огнях подсветки исторических зданий. Экскурсия проходит по самым ярким местам ночного города. \r\nВы увидите: \r\n- сказочный замок – кукольный театр;\r\n- горит на медленном огне Казан – новый городской ЗАГС;\r\n- поражает воображение самый большой в Европе медиафасад стадиона Казань-Арена;\r\n- дворец земледельцев и новая набережная;\r\n- феерическое зрелище миллиона разноцветных брызг фонтанов, украшающих площади, парки и набережные Казани (в летнее время).\r\nВ стоимость включено: проезд на новых автобусах, экскурсионное обслуживание профессиональными гидами.	\N	f	\N	2 часа	\N	\N	\N	\N	\N	\N
13	Экскурсия «Прогулка по Казани разных эпох» - "Городская панорама" +Обзорная экскурсия	Экскурсия «Прогулка по Казани разных эпох». Посещение выставочно — зрелищного комплекса «Городская Панорама». Вас ждут экспозиции, посвященные Казани, ее архитектуре, истории и этапам развития. Вы совершите путешествие по лабиринтам улиц Старо-татарской слободы, на круговой видеопанораме в 360 градусов оживут старинные фотографии из жизни Казани. Вы можете почувствовать себя пассажиром старинного трамвая начала 20 века, посмотреть на город с высоты птичьего полета. На уникальных макетах предстанет Казань 16 в., Казань эпохи императоров и современная Казань. Каждое строение выполнено по отдельному проекту с индивидуальным чертежом фасада. Все макеты домов являются точной копией своих оригиналов.\r\nПо окончании экскурсии по комплексу "Городская Панорама" Вы отправитесь на Обзорную экскурсию по Казани "Легенды и тайны Тысячелетней Казани".\r\nВы увидите:\r\n- Старо-татарскую слободу со старинными татарскими мечетями;\r\n- овеянное легендами озеро Кабан;\r\n- здание – парусник Татарского академического театра им Г. Камала;\r\n- татарскую деревню «Туган Авылым»;\r\n- сказочный дворец - театр кукол «Экият»;\r\n- Казанский Университет;\r\n- площадь Свободы – культурный и административный центр Казани;\r\n- Богородицкий монастырь и его святыня Казанская икона Божией Матери\r\nВ стоимость включено: проезд на новых автобусах, входные билеты в выставочно-зрелищный комплекс "Панорама", экскурсионное обслуживание профессиональными гидами.	\N	f	\N	3 часа 30 минут	\N	\N	\N	\N	\N	\N
15	Пешеходная экскурсия «Здесь науки, здесь искусства...»+ особняк Зинаиды Ушковой	Пешеходная экскурсия «Казанский Арбат» по историческому центру города улице Баумана. (быв. Большая Проломная). В ходе экскурсии – россыпи фонтанов, колокольня и церковь Богоявления, где крестили Федора Шаляпина, сам памятник Шаляпину, здание национального банка, драматический театр, нулевой меридиан, аллея, национальных звезд, копия роскошной кареты, на которой во время своего визита по Казани передвигалась Екатерина II. Вы познакомитесь с Су Анасы и узнаете историю Казанского кота.\r\nПосещение собора Петра и Павла, самого впечатляющего в ожерелье Казанских храмов.\r\nПешеходная экскурсия «Здесь науки, здесь искусства, просвещения очаг». С давних времён Казань слывёт оплотом образования. Достаточно вспомнить, что именно в Казани было создано одно из старейших учебных заведений России — Казанский Университет, стены которого взрастили не одну плеяду будущих писателей, математиков, астрономов, химиков, деятельность которых прославила не только наш университет, но и нашу страну.Мы осмотрим весь комплекс зданий университетского городка: главное здание, обсерваторию, анатомический театр, научную библиотеку, гуманитарный и физический корпусы, здание химического института. Здесь зарождались научные школы для всей России.\r\nЭкскурсия в особняк Зинаиды Ушковой (национальная библиотека РТ). Это один из самых красивых старинных особняков Казани начала XX века, свадебный подарок купца-промышленника Алексея Ушкова своей невесте.\r\nВы увидите:\r\n- улицу Баумана-исторический центр Казани\r\n- комплекс университетского городка – выдающийся памятник русского классицизма.\r\n- обсерватория – великие астрономы\r\n- химическая лаборатория – великие открытия\r\n- анатомический театр – великие достижения\r\n- научная библиотека – великие книги\r\n- гуманитарный и физический корпусы, здание химического института;\r\n- особняк "Зинаиды Ушковой"\r\nВ стоимость включено: проезд на новых автобусах, экскурсионное обслуживание профессиональными гидами, входные билеты в особняк "Зинаиды Ушковой".	\N	f	\N	3 часа	\N	\N	\N	\N	\N	\N
8	Экскурсия в Чебоксары +интерактив «Пусть блаженствует душа!» с дегустацией пива+обед	Экскурсия «Столица чувашского народа — Шупашкар». На правом берегу Волги расположен город Чебоксары — столица Чувашской республики. По предписанию Ивана Грозного в 15 в. на берегу Волжского залива была сооружена деревянная срубная крепость, получившая название Чебоксары. Экскурсия по Чебоксарам включает экскурсию по старому городу.\r\nВы увидите:\r\n- набережную — одну из красивейших на Волге;\r\n- Чебоксарский залив — жемчужину города;\r\n- памятник любви – Таганаит;\r\n- памятник Чапаеву;\r\n- скульптуру Матери-Покровительницы;\r\n- памятник Остапу Бендеру и Кисе Воробьянинову на бульваре Купца Ефремова.\r\nВ экскурсию включено участие в программе — «Пусть блаженствует душа!». Развлекательная этнографическая программа с показом обрядов, традиций и обычаев чувашского народа. Дегустация национального напитка — Пива. (Для детей в составе тура предусмотрена замена напитков на соки. )\r\nПитание:\r\nОбед - в кафе Чебоксар\r\nВ стоимость включено: проезд на новых автобусах, развлекательная этнографическая программа, дегустация напитков, обслуживание профессиональными гидами, обед.	\N	f	\N	11 часов	\N	\N	\N	\N	\N	\N
\.


--
-- TOC entry 2344 (class 0 OID 24832)
-- Dependencies: 219
-- Data for Name: excursions_excursion_property; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY excursions_excursion_property (id, excursion_id, excursion_property_id) FROM stdin;
\.


--
-- TOC entry 2357 (class 0 OID 0)
-- Dependencies: 220
-- Name: excursions_excursion_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('excursions_excursion_property_id_seq', 1, false);


--
-- TOC entry 2358 (class 0 OID 0)
-- Dependencies: 192
-- Name: excursions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('excursions_id_seq', 24, true);


--
-- TOC entry 2342 (class 0 OID 24814)
-- Dependencies: 217
-- Data for Name: excursions_sights; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY excursions_sights (id, excursion_id, soght_id) FROM stdin;
\.


--
-- TOC entry 2359 (class 0 OID 0)
-- Dependencies: 218
-- Name: excursions_sights_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('excursions_sights_id_seq', 1, false);


--
-- TOC entry 2336 (class 0 OID 24761)
-- Dependencies: 211
-- Data for Name: group_tourist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY group_tourist (id, tourist_id, group_id) FROM stdin;
\.


--
-- TOC entry 2360 (class 0 OID 0)
-- Dependencies: 212
-- Name: group_tourist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('group_tourist_id_seq', 1, false);


--
-- TOC entry 2315 (class 0 OID 16611)
-- Dependencies: 190
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY groups (id, tour_date, reserved, excursion_id, guide_id, capacity) FROM stdin;
\.


--
-- TOC entry 2361 (class 0 OID 0)
-- Dependencies: 193
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: intour24_admin
--

SELECT pg_catalog.setval('groups_id_seq', 2, true);


--
-- TOC entry 2313 (class 0 OID 16429)
-- Dependencies: 188
-- Data for Name: guides; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY guides (id, first_name, email, phone, average_rating, last_name) FROM stdin;
\.


--
-- TOC entry 2362 (class 0 OID 0)
-- Dependencies: 194
-- Name: guides_id_seq; Type: SEQUENCE SET; Schema: public; Owner: intour24_admin
--

SELECT pg_catalog.setval('guides_id_seq', 2, true);


--
-- TOC entry 2328 (class 0 OID 24692)
-- Dependencies: 203
-- Data for Name: operator; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY operator (id, name, phone, address, logo) FROM stdin;
\.


--
-- TOC entry 2363 (class 0 OID 0)
-- Dependencies: 204
-- Name: operator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('operator_id_seq', 1, false);


--
-- TOC entry 2311 (class 0 OID 16419)
-- Dependencies: 186
-- Data for Name: picking_places; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY picking_places (id, name, geoposition) FROM stdin;
\.


--
-- TOC entry 2364 (class 0 OID 0)
-- Dependencies: 195
-- Name: picking_places_id_seq; Type: SEQUENCE SET; Schema: public; Owner: intour24_admin
--

SELECT pg_catalog.setval('picking_places_id_seq', 2, true);


--
-- TOC entry 2346 (class 0 OID 24866)
-- Dependencies: 221
-- Data for Name: prices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY prices (id, price_for_children, price_for_adult, price_for_enfant) FROM stdin;
\.


--
-- TOC entry 2316 (class 0 OID 16641)
-- Dependencies: 191
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY ratings (id, excursion_id, guide_id, excursion_rate, guide_rate, feedback) FROM stdin;
\.


--
-- TOC entry 2365 (class 0 OID 0)
-- Dependencies: 197
-- Name: ratings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: intour24_admin
--

SELECT pg_catalog.setval('ratings_id_seq', 4, true);


--
-- TOC entry 2324 (class 0 OID 24661)
-- Dependencies: 199
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: intour24_admin
--

COPY schedule (id, start_date, repeat_interval, repeat_weekday, repeat_week, end_date, excursion, repeat_year, repeat_month, repeat_day) FROM stdin;
1	2017-06-03 00:00:00+03	\N	\N	\N	\N	7	\N	\N	\N
\.


--
-- TOC entry 2366 (class 0 OID 0)
-- Dependencies: 200
-- Name: schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: intour24_admin
--

SELECT pg_catalog.setval('schedule_id_seq', 1, true);


--
-- TOC entry 2330 (class 0 OID 24717)
-- Dependencies: 205
-- Data for Name: sight_property; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sight_property (id, name, image) FROM stdin;
\.


--
-- TOC entry 2367 (class 0 OID 0)
-- Dependencies: 206
-- Name: sight_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sight_property_id_seq', 1, false);


--
-- TOC entry 2334 (class 0 OID 24739)
-- Dependencies: 209
-- Data for Name: sight_sight_property; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sight_sight_property (id, sight_id, sight_property_id) FROM stdin;
\.


--
-- TOC entry 2368 (class 0 OID 0)
-- Dependencies: 210
-- Name: sight_sight_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sight_sight_property_id_seq', 1, false);


--
-- TOC entry 2312 (class 0 OID 16424)
-- Dependencies: 187
-- Data for Name: sights; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sights (id, name, geoposition, images, description, cover) FROM stdin;
3	Здание – парусник Татарского академического театра им Г. Кам	\N	{static/img/kamal1.jpg,static/img/kamal2.jpeg}	\N	static/img/kamal1.jpg
4	Татарская деревня «Туган Авылым»	\N	{static/img/tugan1.jpg,static/img/tugan2.jpg}	\N	static/img/tugan1.jpg
5	Театр кукол «Экият»	\N	{static/img/akiyat1.jpg,static/img/akiyat2.jpg}	\N	static/img/akiyat1.jpg
6	Казанский Кремль	\N	{static/img/kazan_kremlin1.jpg,static/img/kazan_kremlin2.jpg}	\N	static/img/kazan_kremlin1.jpg
7	мечеть Кул Шариф	\N	{static/img/qolsarif_mosque1.jpg,static/img/qolsarif_mosque2.jpg}	\N	static/img/qolsarif_mosque1.jpg
8	«падающая» башня ханши Сююмбике	\N	{static/img/soyembika_tower1.jpg,static/img/soyembika_tower2.jpg}	\N	static/img/soyembika_tower1.jpg
1	Старо-татарская слобода со старинными татарскими мечетями	\N	{static/img/starotatarskayasloboda1.jpg,static/img/starotatarskayasloboda2.jpg}	\N	static/img/starotatarskayasloboda1.jpg
2	Озеро Кабан	\N	{static/img/kaban1.jpg,static/img/kaban2.jpg}	\N	static/img/kaban1.jpg
\.


--
-- TOC entry 2369 (class 0 OID 0)
-- Dependencies: 196
-- Name: sights_id_seq; Type: SEQUENCE SET; Schema: public; Owner: intour24_admin
--

SELECT pg_catalog.setval('sights_id_seq', 8, true);


--
-- TOC entry 2314 (class 0 OID 16434)
-- Dependencies: 189
-- Data for Name: tourists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tourists (id, first_name, email, phone, last_name) FROM stdin;
\.


--
-- TOC entry 2370 (class 0 OID 0)
-- Dependencies: 198
-- Name: tourists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: intour24_admin
--

SELECT pg_catalog.setval('tourists_id_seq', 2, true);


--
-- TOC entry 2338 (class 0 OID 24782)
-- Dependencies: 213
-- Data for Name: transport; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY transport (id, capacity, number, group_id) FROM stdin;
\.


--
-- TOC entry 2371 (class 0 OID 0)
-- Dependencies: 214
-- Name: transport_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('transport_id_seq', 1, false);


--
-- TOC entry 2340 (class 0 OID 24798)
-- Dependencies: 215
-- Data for Name: transport_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY transport_type (id, name, transport_id) FROM stdin;
\.


--
-- TOC entry 2372 (class 0 OID 0)
-- Dependencies: 216
-- Name: transport_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('transport_type_id_seq', 1, false);


--
-- TOC entry 2153 (class 2606 OID 24688)
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- TOC entry 2159 (class 2606 OID 24735)
-- Name: excursion_property excursion_property_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursion_property
    ADD CONSTRAINT excursion_property_pkey PRIMARY KEY (id);


--
-- TOC entry 2171 (class 2606 OID 24836)
-- Name: excursions_excursion_property excursions_excursion_property_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions_excursion_property
    ADD CONSTRAINT excursions_excursion_property_pkey PRIMARY KEY (id);


--
-- TOC entry 2137 (class 2606 OID 24616)
-- Name: excursions excursions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions
    ADD CONSTRAINT excursions_pkey PRIMARY KEY (id);


--
-- TOC entry 2169 (class 2606 OID 24818)
-- Name: excursions_sights excursions_sights_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions_sights
    ADD CONSTRAINT excursions_sights_pkey PRIMARY KEY (id);


--
-- TOC entry 2163 (class 2606 OID 24765)
-- Name: group_tourist group_tourist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY group_tourist
    ADD CONSTRAINT group_tourist_pkey PRIMARY KEY (id);


--
-- TOC entry 2147 (class 2606 OID 16615)
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2143 (class 2606 OID 16433)
-- Name: guides guides_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY guides
    ADD CONSTRAINT guides_pkey PRIMARY KEY (id);


--
-- TOC entry 2155 (class 2606 OID 24699)
-- Name: operator operator_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY operator
    ADD CONSTRAINT operator_pkey PRIMARY KEY (id);


--
-- TOC entry 2139 (class 2606 OID 16423)
-- Name: picking_places picking_places_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY picking_places
    ADD CONSTRAINT picking_places_pkey PRIMARY KEY (id);


--
-- TOC entry 2141 (class 2606 OID 16428)
-- Name: sights places_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sights
    ADD CONSTRAINT places_pkey PRIMARY KEY (id);


--
-- TOC entry 2173 (class 2606 OID 24870)
-- Name: prices prices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY prices
    ADD CONSTRAINT prices_pkey PRIMARY KEY (id);


--
-- TOC entry 2149 (class 2606 OID 16648)
-- Name: ratings ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (id);


--
-- TOC entry 2151 (class 2606 OID 24670)
-- Name: schedule schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: intour24_admin
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (id);


--
-- TOC entry 2157 (class 2606 OID 24724)
-- Name: sight_property sight_property_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sight_property
    ADD CONSTRAINT sight_property_pkey PRIMARY KEY (id);


--
-- TOC entry 2161 (class 2606 OID 24743)
-- Name: sight_sight_property sight_sight_property_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sight_sight_property
    ADD CONSTRAINT sight_sight_property_pkey PRIMARY KEY (id);


--
-- TOC entry 2145 (class 2606 OID 16610)
-- Name: tourists tourist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tourists
    ADD CONSTRAINT tourist_pkey PRIMARY KEY (id);


--
-- TOC entry 2165 (class 2606 OID 24789)
-- Name: transport transport_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transport
    ADD CONSTRAINT transport_pkey PRIMARY KEY (id);


--
-- TOC entry 2167 (class 2606 OID 24805)
-- Name: transport_type transport_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transport_type
    ADD CONSTRAINT transport_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2174 (class 2606 OID 24851)
-- Name: excursions excursions_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions
    ADD CONSTRAINT excursions_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- TOC entry 2191 (class 2606 OID 24837)
-- Name: excursions_excursion_property excursions_excursion_property_excursion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions_excursion_property
    ADD CONSTRAINT excursions_excursion_property_excursion_id_fkey FOREIGN KEY (excursion_id) REFERENCES excursions(id);


--
-- TOC entry 2192 (class 2606 OID 24842)
-- Name: excursions_excursion_property excursions_excursion_property_excursion_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions_excursion_property
    ADD CONSTRAINT excursions_excursion_property_excursion_property_id_fkey FOREIGN KEY (excursion_property_id) REFERENCES excursion_property(id);


--
-- TOC entry 2176 (class 2606 OID 24861)
-- Name: excursions excursions_operator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions
    ADD CONSTRAINT excursions_operator_id_fkey FOREIGN KEY (operator_id) REFERENCES operator(id);


--
-- TOC entry 2175 (class 2606 OID 24856)
-- Name: excursions excursions_picking_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions
    ADD CONSTRAINT excursions_picking_place_id_fkey FOREIGN KEY (picking_place_id) REFERENCES picking_places(id);


--
-- TOC entry 2177 (class 2606 OID 24871)
-- Name: excursions excursions_price_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions
    ADD CONSTRAINT excursions_price_id_fkey FOREIGN KEY (price_id) REFERENCES prices(id);


--
-- TOC entry 2189 (class 2606 OID 24819)
-- Name: excursions_sights excursions_sights_excursion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions_sights
    ADD CONSTRAINT excursions_sights_excursion_id_fkey FOREIGN KEY (excursion_id) REFERENCES excursions(id);


--
-- TOC entry 2190 (class 2606 OID 24824)
-- Name: excursions_sights excursions_sights_soght_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY excursions_sights
    ADD CONSTRAINT excursions_sights_soght_id_fkey FOREIGN KEY (soght_id) REFERENCES sights(id);


--
-- TOC entry 2186 (class 2606 OID 24771)
-- Name: group_tourist group_tourist_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY group_tourist
    ADD CONSTRAINT group_tourist_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(id);


--
-- TOC entry 2185 (class 2606 OID 24766)
-- Name: group_tourist group_tourist_tourist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY group_tourist
    ADD CONSTRAINT group_tourist_tourist_id_fkey FOREIGN KEY (tourist_id) REFERENCES tourists(id);


--
-- TOC entry 2179 (class 2606 OID 24617)
-- Name: groups groups_excursion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_excursion_fkey FOREIGN KEY (excursion_id) REFERENCES excursions(id);


--
-- TOC entry 2178 (class 2606 OID 16631)
-- Name: groups groups_guide_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_guide_fkey FOREIGN KEY (guide_id) REFERENCES guides(id);


--
-- TOC entry 2181 (class 2606 OID 24622)
-- Name: ratings ratings_excursion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_excursion_fkey FOREIGN KEY (excursion_id) REFERENCES excursions(id);


--
-- TOC entry 2180 (class 2606 OID 16654)
-- Name: ratings ratings_guide_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_guide_fkey FOREIGN KEY (guide_id) REFERENCES guides(id);


--
-- TOC entry 2182 (class 2606 OID 24676)
-- Name: schedule schedule_excursion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: intour24_admin
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT schedule_excursion_fkey FOREIGN KEY (excursion) REFERENCES excursions(id);


--
-- TOC entry 2183 (class 2606 OID 24744)
-- Name: sight_sight_property sight_sight_property_sight_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sight_sight_property
    ADD CONSTRAINT sight_sight_property_sight_id_fkey FOREIGN KEY (sight_id) REFERENCES sights(id);


--
-- TOC entry 2184 (class 2606 OID 24749)
-- Name: sight_sight_property sight_sight_property_sight_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sight_sight_property
    ADD CONSTRAINT sight_sight_property_sight_property_id_fkey FOREIGN KEY (sight_property_id) REFERENCES sight_property(id);


--
-- TOC entry 2187 (class 2606 OID 24790)
-- Name: transport transport_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transport
    ADD CONSTRAINT transport_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(id);


--
-- TOC entry 2188 (class 2606 OID 24806)
-- Name: transport_type transport_type_transport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transport_type
    ADD CONSTRAINT transport_type_transport_id_fkey FOREIGN KEY (transport_id) REFERENCES transport(id);


-- Completed on 2017-06-01 09:34:33

--
-- PostgreSQL database dump complete
--

