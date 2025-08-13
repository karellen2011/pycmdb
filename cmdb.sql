--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: get_uuid(); Type: FUNCTION; Schema: public; Owner: cmdb
--

CREATE FUNCTION public.get_uuid() RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
    uuid varchar(32);
BEGIN
    SELECT REPLACE(CAST(uuid_generate_v4() AS varchar(36)), '-', '') INTO uuid;
    RETURN uuid;
END;
$$;


ALTER FUNCTION public.get_uuid() OWNER TO cmdb;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _sys_dictionary; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public._sys_dictionary (
    uuid character varying(32) DEFAULT public.get_uuid(),
    sys_table character varying(256),
    sys_table_column character varying(256),
    dict_value character varying(256),
    sys_order integer,
    color character varying(8) DEFAULT ''::character varying
);


ALTER TABLE public._sys_dictionary OWNER TO cmdb;

--
-- Name: _sys_display_value; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public._sys_display_value (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    display_value character varying(256),
    sys_table character varying(256),
    sys_table_column character varying(256),
    sys_order integer,
    include boolean,
    hide boolean DEFAULT false
);


ALTER TABLE public._sys_display_value OWNER TO cmdb;

--
-- Name: _sys_function; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public._sys_function (
    uuid character varying(32) DEFAULT public.get_uuid(),
    sys_table character varying(256),
    sys_table_column character varying(256),
    function_name character varying(256)
);


ALTER TABLE public._sys_function OWNER TO cmdb;

--
-- Name: _sys_reference; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public._sys_reference (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    source character varying(256),
    target character varying(256)
);


ALTER TABLE public._sys_reference OWNER TO cmdb;

--
-- Name: company; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.company (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    developer boolean DEFAULT false,
    publisher boolean DEFAULT false,
    manufacturer boolean DEFAULT false,
    vendor boolean DEFAULT false,
    url character varying(64) DEFAULT ''::character varying,
    country character varying(32) DEFAULT 'cb3a85c24b6d40f8bf46e5611c8da42f'::character varying
);


ALTER TABLE public.company OWNER TO cmdb;

--
-- Name: country; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.country (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    official_state_name character varying(256) DEFAULT ''::character varying,
    sovereignty character varying(32) DEFAULT ''::character varying,
    iso_3166_1_alpha_2 character varying(2) DEFAULT ''::character varying,
    iso_3166_1_alpha_3 character varying(3) DEFAULT ''::character varying,
    iso_3166_1_numeric character varying(3) DEFAULT ''::character varying,
    tld character varying(16) DEFAULT ''::character varying,
    capital character varying(64) DEFAULT ''::character varying,
    population integer DEFAULT 0,
    land_area integer DEFAULT 0,
    population_density integer DEFAULT 0,
    country_latitude numeric(9,6) DEFAULT 0.000000,
    country_longitude numeric(9,6) DEFAULT 0.000000,
    capital_latitude numeric(7,4) DEFAULT 0.0000,
    capital_longitude numeric(7,4) DEFAULT 0.0000
);


ALTER TABLE public.country OWNER TO cmdb;

--
-- Name: harddisk; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.harddisk (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    serial_nmuber character varying(64) DEFAULT ''::character varying,
    size numeric(8,2) DEFAULT 0.000,
    hardware_asset character varying(32) DEFAULT '96e441f8c78c49739e25ad10cf1f80ff'::character varying
);


ALTER TABLE public.harddisk OWNER TO cmdb;

--
-- Name: hardware; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.hardware (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    cpu_type character varying(32) DEFAULT 'e2354cad85f34870b57a90a1f572dd84'::character varying,
    company character varying(32) DEFAULT 'a65c511a51054dac91641b3944f7bb5b'::character varying,
    product_lifecycle character varying(32) DEFAULT '0be2235637f14e4f8a8b506d6b5df007'::character varying
);


ALTER TABLE public.hardware OWNER TO cmdb;

--
-- Name: hardware_asset; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.hardware_asset (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    software character varying(32) DEFAULT 'f57d575fe9f64446b80cdecf296442e4'::character varying,
    company character varying(32) DEFAULT 'a65c511a51054dac91641b3944f7bb5b'::character varying,
    hardware character varying(32) DEFAULT 'e4033e0c002643c1addf746f67880c09'::character varying,
    hw_lifecycle character varying(32) DEFAULT '15054e5d5bdc4ed7b1d252618e9414a2'::character varying,
    qrcode character varying(1),
    ram numeric(6,3) DEFAULT 0.000,
    cpu_speed numeric(6,3) DEFAULT 0.000,
    order_date date DEFAULT '1970-01-01'::date
);


ALTER TABLE public.hardware_asset OWNER TO cmdb;

--
-- Name: knowledge; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.knowledge (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    article text DEFAULT 'Please enter some knowledge...'::text,
    approved boolean DEFAULT false
);


ALTER TABLE public.knowledge OWNER TO cmdb;

--
-- Name: location; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.location (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    country character varying(32) DEFAULT 'e1e5d806b1e9433ab69b1d6e79f95370'::character varying,
    street character varying(256) DEFAULT ''::character varying,
    zip_code integer,
    city character varying(256) DEFAULT ''::character varying,
    asdf character varying(256) DEFAULT 'qwer'::character varying
);


ALTER TABLE public.location OWNER TO cmdb;

--
-- Name: network_interfaces; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.network_interfaces (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    mac_address character varying(17) DEFAULT '00:00:00:00:00:00'::character varying,
    ip_address character varying(15) DEFAULT '0.0.0.0'::character varying,
    netmask character varying(15) DEFAULT '255.255.255.0'::character varying,
    ip_type character varying(32) DEFAULT 'a886340306b543a883df8f9a3bdf9100'::character varying,
    hardware_asset character varying(32) DEFAULT '96e441f8c78c49739e25ad10cf1f80ff'::character varying,
    connector character varying(32) DEFAULT '2d42948af8064b1d884d149024d1f591'::character varying
);


ALTER TABLE public.network_interfaces OWNER TO cmdb;

--
-- Name: processes; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.processes (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    supplier character varying(256) DEFAULT ''::character varying,
    input character varying(256) DEFAULT ''::character varying,
    output character varying(256) DEFAULT ''::character varying,
    customer character varying(256) DEFAULT ''::character varying,
    knowledge character varying(32) DEFAULT '10f2cfaab5cb4967adb602b9c0f8e53e'::character varying
);


ALTER TABLE public.processes OWNER TO cmdb;

--
-- Name: service; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.service (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.service OWNER TO cmdb;

--
-- Name: service_asset; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.service_asset (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    environment character varying(32) DEFAULT '138930daac194a3094077481a60f59e1'::character varying,
    service character varying(32) DEFAULT '0e3a8e8712884eb283a2d8a34b5ac1a1'::character varying
);


ALTER TABLE public.service_asset OWNER TO cmdb;

--
-- Name: software; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.software (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    version character varying(64) DEFAULT ''::character varying,
    sw_lifecycle character varying(32) DEFAULT '2db9e4c07c3242f58a7b842a7191ecba'::character varying,
    software_type character varying(32) DEFAULT 'a8af2f0e3a054940b7abb06a72247767'::character varying
);


ALTER TABLE public.software OWNER TO cmdb;

--
-- Name: test; Type: TABLE; Schema: public; Owner: cmdb
--

CREATE TABLE public.test (
    uuid character varying(32) DEFAULT public.get_uuid() NOT NULL,
    name character varying(256),
    active boolean DEFAULT true NOT NULL,
    count integer DEFAULT 0,
    "float" numeric(8,2) DEFAULT 0.0,
    bool boolean DEFAULT true,
    "varchar" character varying(64) DEFAULT 'default'::character varying,
    order_date date DEFAULT '2025-08-30'::date,
    description text DEFAULT 'Please enter some text...'::text,
    test_lc character varying(32) DEFAULT 'ad71d6aecdaf4b3a8c04ed1136f592f4'::character varying,
    processes character varying(32) DEFAULT '14f132584c6f4a91a08113a3af7ab6b0'::character varying
);


ALTER TABLE public.test OWNER TO cmdb;

--
-- Data for Name: _sys_dictionary; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public._sys_dictionary (uuid, sys_table, sys_table_column, dict_value, sys_order, color) FROM stdin;
227eb27d167241c4bd643416abfd4ab4	hardware_asset	hw_lifecycle	In Stock	30	FCE83A
14f13d39c51541a89b0a13b53f29472c	hardware_asset	hw_lifecycle	Pending Retirement	40	FF3838
4fe586e7048349ce99454077633905a2	hardware_asset	hw_lifecycle	Disposed	60	56F000
cbda7508f1d94cd0925ba72cb28da6ea	network_interfaces	ip_type	Static	20	
a8af2f0e3a054940b7abb06a72247767	software	software_type	-- None --	10	
e9dd9386ce8d4efca74255651ab32f00	software	software_type	User Software	10	
cb3a85c24b6d40f8bf46e5611c8da42f	company	country	-- None --	10	
b995f1b2d377462cb7176831a915f70a	company	country	South Korea	10	
037a2e983c024ce090f673a0590b943c	software	sw_lifecycle	Obsolete	10	FF3838
2db9e4c07c3242f58a7b842a7191ecba	software	sw_lifecycle	-- None --	100	
0ba059d7369c4a8783a7f23e11139773	hardware	cpu_type	x86_32	10	
8b27b64193c14febb913ad8682557639	hardware	cpu_type	arm32	10	
806573b9e40b4966a37c15407dcd0302	hardware	cpu_type	sparc	10	
62f410217a8343bdad336819aa25adb5	company	country	Japan	10	
0be2235637f14e4f8a8b506d6b5df007	hardware	product_lifecycle	-- None --	10	
7328ff123f6e402e8985bb596967828b	hardware	product_lifecycle	Obsolete	30	FF3838
ea9e5224b47945f995df7b89add84d4e	hardware_asset	hw_lifecycle	Available	20	FCE83A
e62617b8d9fb4b849b39ed5b0bd79d63	company	country	Germany	10	
fc85e867554c48cba18f977c2b058271	company	country	United States of America	10	
84fbc39baefa4df2b1e0debc1426e8df	software	sw_lifecycle	Available	10	56F000
e2354cad85f34870b57a90a1f572dd84	hardware	cpu_type	-- None --	10	
abfdadab6dcf48288c0737bcce370f50	hardware	cpu_type	x86_64	10	
cfd2bcd4df4447c5a8db323f827ba215	hardware	cpu_type	arm64	10	
a886340306b543a883df8f9a3bdf9100	network_interfaces	ip_type	-- None --	10	
a4c7242fdd4c4e2881c997cf17a763c4	hardware	cpu_type	sh4	10	
99c34331ea1944bb8ca5816d6962a862	hardware	product_lifecycle	Available	20	56F000
15054e5d5bdc4ed7b1d252618e9414a2	hardware_asset	hw_lifecycle	-- None --	5	
6386ab37d91b4d45963d646431d0b6eb	hardware_asset	hw_lifecycle	On Order	10	FCE83A
0f040eee0f0d4c9faa6abd0ff9ae956f	hardware_asset	hw_lifecycle	In Use	35	FF3838
c359893877f34d82b7f64ef151a7026b	hardware_asset	hw_lifecycle	Pending Disposal	50	56F000
3f6eea09accb4406bb88d98d11010217	network_interfaces	ip_type	Dynamic	30	
06dd2581e04f497a8fed02f791eede70	network_interfaces	ip_type	Slave	40	
205399429d1f43edb37a761cb4102317	software	software_type	Operating System	10	
6e7ed0a3a1ba462ca5f0b0b15b4a8bae	software	software_type	Server Software	10	
138930daac194a3094077481a60f59e1	service_asset	environment	-- None --	10	
f9e24cc3d5f54d2aa7635140a8f40d60	service_asset	environment	Production	10	
eb6a50d707e44681af665acca3615c25	service_asset	environment	Test	10	
34b5869c3107434ba02ca5271722f4fb	service_asset	environment	Development	10	
2d42948af8064b1d884d149024d1f591	network_interfaces	connector	-- None --	10	
addcb50381a84859ba4acc90c95fa1b0	network_interfaces	connector	Built-In	20	
7ca4127158534d97a0ba4e930cd4367c	network_interfaces	connector	USB	20	
ad71d6aecdaf4b3a8c04ed1136f592f4	test	test_lc	-- None --	10	
3f9d607dab794340b1477cae4d111384	test	test_lc	Active	10	FF3838
b83656c33ea44205bc6d94a66e034f25	test	test_lc	Inactive	10	A4ABB6
\.


--
-- Data for Name: _sys_display_value; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public._sys_display_value (uuid, display_value, sys_table, sys_table_column, sys_order, include, hide) FROM stdin;
565c3ea672dd42b99ccca5480838ff5e	UUID	network_interfaces	uuid	10	f	f
560a75aabb464b94ac84424048cfb5fb	Name	network_interfaces	name	20	f	f
bffd15300d634298a136c1e423269628	Active	network_interfaces	active	30	f	f
f1ced43bea69462db6db93d950adde4a	MAC	network_interfaces	mac_address	40	f	f
6096f43ddc5d423cb600463c6b557996	Netmask	network_interfaces	netmask	60	f	f
7a503f1452084a69ba7588537bfaabc1	Size (GB)	harddisk	size	50	f	f
82403fcc174f4a3b8a68cc3bf8d19ec0	UUID	software	uuid	10	f	f
cff67a349cf84abeb90fe856a9f36962	Name	software	name	20	f	f
74b0e323d6164e7da9519ceff0d05dd4	Active	software	active	30	f	f
3477d9a1cf384ebebc2948c1f5aaaa4e	Lifecycle	software	sw_lifecycle	40	f	f
4ede3925080640469b1a475a531f5a89	ISO 3166-1 numeric	country	iso_3166_1_numeric	80	f	f
e315866808464cd6be1bfd759c6da1e9	Population	country	population	110	f	f
bbbef811b3e1456ba302c8dacfb5b5f2	Density (P/Km²)	country	population_density	130	f	f
a002d3e31dac4a03bbda86205563b380	UUID	hardware	uuid	10	f	f
825e2367f58b439fa36b21d74e860882	Name	hardware	name	20	f	f
7a545ee16e254d77816947f6a5205172	Active	hardware	active	30	f	f
5d4f78d0773a4ebabd97b1e128d2385f	CPU	hardware	cpu_type	40	f	f
52e7b87044e147e8ae149292d7328f87	Manufacturer	hardware	company	50	f	f
3c5dade3c456400babc22bc5c3f25f82	Country	country		600	f	f
ec3d7dd43acc4439a8ea561c403b2e24	UUID	country	uuid	10	f	f
5eb9e0934ae942cebc8a33f004cf0736	Name	country	name	20	f	f
1145970a803147a4aa1a4eefa11e8c0c	Active	country	active	30	f	f
53f7c14c337048a094a7c649f1d37449	ISO 3166-1 alpha-2	country	iso_3166_1_alpha_2	60	f	f
ed8b8061093e450f9a6953dcaae95213	Process	processes	name	50	f	f
ba0eddccf64442e79455c0ae4ff2433c	UUID	processes	uuid	10	f	f
189a85a84bf54277ba8112b238e0cddf	Active	processes	active	20	f	f
eb31d231d66d412ba6c7e700122e1dc6	Supplier	processes	supplier	30	f	f
37f83ff492334b23b63937db6bb538e7	Output	processes	output	60	f	f
43592016ee4f45cb9239cffcb0edd0b7	Type	software	software_type	50	f	f
60587a27835b470cb548d7a90214969a	UUID	harddisk	uuid	10	f	f
fff569b75a6246d1a488f18f66ec08f5	Name	harddisk	name	20	f	f
8e88c36b0eed40a7ad8e4312e19e5114	Active	harddisk	active	30	f	f
21d3392d813540b08f2b9a9e101614a8	IP	network_interfaces	ip_address	50	f	f
417b441b521140e8bc81fdddd87dd0db	S/N	harddisk	serial_nmuber	40	f	f
9b463f44a9b74715a38190331291e895	Version	software	version	25	t	f
1ffed5a8c5474f2684ee0be6b1f52993	Software	software		100	f	f
25a228fe93d841758c4f69e6cc01ed52	Asset Tag	hardware_asset	qrcode	5	f	f
59477cba1be54a0786f456f5aaeda0b2	UUID	hardware_asset	uuid	10	f	f
a11b61f07b0b4042a1c83382bbd3b8c6	Name	hardware_asset	name	20	f	f
d879b1d04a044386bba79bf716fb4bb9	Active	hardware_asset	active	30	f	f
ff45430fa1814ad3a8383de8a5a0928d	Harddisk	harddisk		90	f	f
e3ad22b750a84948a71403bfd4a387d7	NIC	network_interfaces		80	f	f
c38f6df5f5894176b101d838e91139de	Hardware	hardware		60	f	f
3198991cf9174257ae70ccbad7d25017	Company	company		50	f	f
ca5feb722eec4a248c727266685a73e4	Process	processes		20	f	f
13b9dcc43372486daec95fcfe239a0a0	OS	hardware_asset	software	40	f	f
c7ea3586df7d44889686feaa96b4d212	UUID	company	uuid	10	f	f
56a759bb4fe840df8266e505b4455830	Name	company	name	20	f	f
56550fc6d8e44450818051eac6efce11	RAM (GB)	hardware_asset	ram	50	f	f
9ad5d7314c6c48f8ac1d0897f0f7bc32	Official state name	country	official_state_name	40	f	t
70fe4625d7d74e3d82ed2a3353af00f8	CPU (GHz)	hardware_asset	cpu_speed	70	f	f
7d03a3cb34394198a32a43171d999541	Capital	country	capital	100	f	f
63f8e68474c74ed8b4cf69d9e1f55bf2	Country	company	country	40	f	f
93fb9ad893c54e68ace32d98f2b499ed	Lifecycle	hardware_asset	hw_lifecycle	100	f	f
6a8c0555ef15402d9f2993ed029c4c1a	IP Type	network_interfaces	ip_type	70	f	f
b9fe09123775432f828d74baf40a6d16	Developer	company	developer	45	f	f
1392df52326d40e28a8987bc724bb683	Publisher	company	publisher	50	f	f
8d12292db4fd484ca06ca4d15c698f10	Manufacturer	company	manufacturer	60	f	f
67836bbb37e64409b4ba9fc1267864ab	Vendor	company	vendor	70	f	f
32acee033c1e4679b4f1cb89f8bd2b09	URL	company	url	80	f	f
fb7b2515b3944adbb5eb3c13e0bf70f9	Input	processes	input	40	f	f
04cd0db000264039a9619384726ecf90	Customer	processes	customer	70	f	f
551544799ec84cd5a218e1ed85915497	Hardware Asset	harddisk	hardware_asset	70	f	f
61ff497c10564b9d81cf4d9f65f42edd	Hardware Asset	network_interfaces	hardware_asset	80	f	f
40bf4e90f56a40f09ea7e90a9390eea0	Lifecycle	hardware	product_lifecycle	60	f	f
0bb70c74e84b41ed93b311bd73f8355b	ISO 3166-1 alpha-3	country	iso_3166_1_alpha_3	70	f	f
38be85a70c0d4432946b015089e57988	TLD	country	tld	90	f	f
39ddb4f09d2e4e3ea53c210e0c549e20	Land Area (Km²)	country	land_area	120	f	f
db14933e9f164fdebb487b060b8cd26b	Location	location		500	f	f
8699b095fe254a99b7831ac5910803b8	UUID	location	uuid	10	f	f
8855b451f2b1461ba0bfea8e8e81aef6	Active	location	active	30	f	f
c3efcd2fcbde41f1895e96cef9c94a43	Country	location	country	40	f	f
d777b5f77c7e4e218cf235ef40d9bd64	Street	location	street	50	f	f
9ab3cf16ffcd42d3a5b9daca2efe5a32	ZIP	location	zip_code	60	f	f
5167b118affd4255ba369a6e79607f17	City	location	city	70	f	f
2de6220ce892475c87be153348ea324b	sdfg	location	asdf	80	t	t
197a045f6d0647d8b3b09a8d448d34f5	Name	location	name	20	t	f
5af4d0bc408143a2b83d96abf3d6bdbf	Sovereignty	country	sovereignty	50	f	t
0fdc0581c42949c6add3ae19c7c1c40e	Connector	network_interfaces	connector	90	f	f
d319aea9b5d44a5b8013368eeb6bdd25	Vendor	hardware_asset	company	80	f	f
b9276f70b2c54fcfb5ad42a2576cddb4	Hardware	hardware_asset	hardware	90	f	f
a1a2b626b3404993923410b496dac45e	Order Date	hardware_asset	order_date	110	f	f
24cf72ecf2164ff3a9955864a9c59023	UUID	service_asset	uuid	10	f	f
4224313addac4949ab699da07906ee36	Name	service_asset	name	20	f	f
52982e4d8b3a44879c10035a6b656afe	Active	service_asset	active	30	f	f
ae8a1dead5b04a1cb4c808e7c3014c14	Environment	service_asset	environment	40	f	f
39e552e8e9df4c79afc578452dcc46c9	Hardware Asset	hardware_asset		70	f	f
36930a998d614451b99f215adbce2c55	Service Asset	service_asset		40	f	f
6a16e93312ba4b9d8c79c9f6311b32c7	UUID	service	uuid	10	f	f
3039799b87a24c12abd5c924a51d81aa	Name	service	name	20	f	f
5dc68646431448ec9e64aaa2d480b0e6	Active	service	active	30	f	f
6099a9b564ba491b9b47eed7b2e024ff	Service	service		30	f	f
dca5ee3c15154da9bcde5d4c1f30f451	Service	service_asset	service	50	f	f
57a430435a0b45dab78403ab46bd1563	Active	company	active	30	f	f
281dc05b174d44b7945e05620d3d2733	Country Latitude	country	country_latitude	140	f	f
d660a37d2d71414bbc906418b2c4c79e	Country Longitude	country	country_longitude	150	f	f
a61722e99aa34f3bbad24e579805af5a	Capital Latitude	country	capital_latitude	160	f	f
52107a474ddb44219e73a1333dd4c0f1	Capital Longitude	country	capital_longitude	170	f	f
b4e8aa2d07d94b2d9b85fec266eee6bc	Knowledge	knowledge		400	f	f
ff8feff6be9942e1847ac6339ef2faf0	UUID	knowledge	uuid	10	f	f
ab4cfb5513324987a25fd93f4346a0f6	Name	knowledge	name	20	f	f
fc25da8b74884f12b69898aa29d93a91	Active	knowledge	active	30	f	f
833d9b29830b44b187222098d88fa82c	Test	test		10	f	f
2107c38e644548eb886f6bd6fe235872	UUID	test	uuid	10	f	f
4ffc858929a849ef96d92d4e37197084	Name	test	name	20	f	f
a308a1eb4de740878456688512df8850	Active	test	active	30	f	f
0d771ba55b8e4cb4aefa5811c6218821	Amount	test	count	40	t	f
566220766c8f48fd9262b2e63a743f7a	Float	test	float	50	f	f
8895e466b15949e6bb1ab196e33bbcb8	Bool	test	bool	60	f	t
eac52da108e6408eb63997bd77e9303f	VarChar	test	varchar	70	f	f
c313d84b3f33496b9983945afc392362	Order Date	test	order_date	80	f	f
b0f66d39b9d145a7bc06a78f2d6d7642	Description	test	description	90	f	t
6b3d87eeeacf4ed396986d6bc6d389ee	Lifecycle	test	test_lc	25	f	f
04f6a6fd2cd846ada69c2153f34dfca9	Process	test	processes	55	f	f
4f6add824af746f5b0bdc0122870db7e	Article	knowledge	article	40	f	t
3b68cede2f7d4f6a864af8720f24bb5a	Knowledge	processes	knowledge	80	f	f
08c34fefde084ccea14736632bcb4a53	Approved	knowledge	approved	50	t	f
\.


--
-- Data for Name: _sys_function; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public._sys_function (uuid, sys_table, sys_table_column, function_name) FROM stdin;
a0bd6db91e1b4de083d81264ee55a674	hardware_asset	qrcode	qrcode
d5db789d8618478da68c0f916146ae95	hardware_asset	qrcode	qrcode
\.


--
-- Data for Name: _sys_reference; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public._sys_reference (uuid, source, target) FROM stdin;
f989cb2f8e1b4515b0b026c8bb7fabb0	hardware_asset	software
c1e607d3e9a14d9f9ed7454d878692e0	dc_asset	dc_product
9fcb0b9fbc52409eb5f62149b942e31c	hardware_asset	vendor
fde4eb3aea1a40d4b9abd4ed4054517d	hardware_asset	company
fca5492fa3f94bdfa0cf887ef7145da9	hardware	company
67b28b8c82b84ba8a8e98bc8b0eb61e7	hardware_asset	hardware
bcb1e0a0d48a41c592fe0cbc60969779	harddisk	hardware_asset
9824a18bdefa4da5b61f5269bed230c1	network_interfaces	hardware_asset
fd505941598647f6bbd0a0863dd80fb6	service_asset	service
45d3f0548a374824a48bdd3514f0d01a	location	country
3e91a8576272419995e4584e8fab5c56	test	processes
6c948b6d925c4c2fb2766f44708ae343	processes	knowledge
\.


--
-- Data for Name: company; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.company (uuid, name, active, developer, publisher, manufacturer, vendor, url, country) FROM stdin;
0692b72645ae49108b5f42b78a4fd3d3	Custom Build	t	f	f	f	f		e62617b8d9fb4b849b39ed5b0bd79d63
17f96752206f412396b01598f02d4bff	Hardkernel	t	t	t	t	t	https://www.hardkernel.com	b995f1b2d377462cb7176831a915f70a
6352de0f8761490981e72967e3ff1430	ebay	t	f	f	f	t	https://www.ebay.de	e62617b8d9fb4b849b39ed5b0bd79d63
a65c511a51054dac91641b3944f7bb5b	-- None --	f	f	f	f	f		cb3a85c24b6d40f8bf46e5611c8da42f
7761252f73af47769b0436060b0562c3	HP	t	t	t	t	t	https://www.hp.com	fc85e867554c48cba18f977c2b058271
5038c9c99f02493e8d60e98bbfe74050	SUN Microsystems	t	t	t	t	t	https://www.oracle.com	fc85e867554c48cba18f977c2b058271
979b23aaa89a40db958dd0ee37f44107	Pollin	t	f	f	f	t	https://www.pollin.de	e62617b8d9fb4b849b39ed5b0bd79d63
fa79f848e1bf44ddbe17ee0aa455bafd	SEGA	t	t	t	t	f	https://www.sega.com	62f410217a8343bdad336819aa25adb5
\.


--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.country (uuid, name, active, official_state_name, sovereignty, iso_3166_1_alpha_2, iso_3166_1_alpha_3, iso_3166_1_numeric, tld, capital, population, land_area, population_density, country_latitude, country_longitude, capital_latitude, capital_longitude) FROM stdin;
701a188605cf4d519bfbc8b91998c51d	Åland Islands 	t	Åland 	Finland 	AX	ALA	248	.ax 		0	0	0	0.000000	0.000000	0.0000	0.0000
67f06b016f2e45539af643fa3548dd54	BonaireSint EustatiusSaba	t	Bonaire, Sint Eustatius and Saba 	Netherlands 	BQ	BES	535	.bq.nl		0	0	0	0.000000	0.000000	0.0000	0.0000
cecc1bd874ce4d3aaec54177455ef6c3	Aruba 	t	the Country of Aruba 	Netherlands 	AW	ABW	533	.aw 		0	0	0	12.521110	-69.968338	12.5240	-70.0270
5171cb0095194eb685029a4c4e8b3c4c	Antigua and Barbuda 	t	Antigua and Barbuda 	UN member 	AG	ATG	028	.ag 	Saint John's	94209	440	214	17.060816	-61.796428	17.1172	-61.8457
0b1299d80347428cbb676ec101b84dd8	Barbados 	t	Barbados 	UN member 	BB	BRB	052	.bb 	Bridgetown	282623	430	657	13.193887	-59.543198	13.1000	-59.6167
3e863c504f2c4278a86121a6fc9d6fda	Jamaica 	t	Jamaica 	UN member 	JM	JAM	388	.jm 	Kingston	2837077	10830	262	18.109581	-77.297508	17.9970	-76.7936
febcfac4135a422b867c698d7e9f3c78	Antarctica 	t	Antarctica 	Antarctic Treaty 	AQ	ATA	010	.aq 		0	0	0	-75.250973	-0.071389	0.0000	0.0000
44ca80d067124b99b77751a91fdcda2c	Armenia 	t	the Republic of Armenia 	UN member 	AM	ARM	051	.am 	Yerevan	2952365	28470	104	40.069099	45.038189	40.1820	44.5146
61a937d8d6fa4afc8b72d5cd9253f3b0	Anguilla 	t	Anguilla 	United Kingdom 	AI	AIA	660	.ai 		0	0	0	18.220554	-63.068615	18.2170	-63.0578
15fe7567d9a440828f06054de2aed480	Belgium 	t	the Kingdom of Belgium 	UN member 	BE	BEL	056	.be 	Brussels	11758603	30280	388	50.503887	4.469936	50.8467	4.3499
bb72cf970393454db9bb83b838c44926	Belarus 	t	the Republic of Belarus 	UN member 	BY	BLR	112	.by 	Minsk	8997603	202910	44	53.709807	27.953389	53.9000	27.5667
0b3acdb53f734a8cbda1b10552c77cbf	Benin 	t	the Republic of Benin 	UN member 	BJ	BEN	204	.bj 	Porto Novo	14814460	112760	131	9.307690	2.315834	6.3654	2.4183
c5f377b75d5647a6a43770e8d44ce73b	Cabo Verde 	t	the Republic of Cabo Verde 	UN member 	CV	CPV	132	.cv 	Praia	527326	4030	131	16.002082	-24.013197	14.9215	-23.5087
5efdd13f86614f538220d417e38158df	Guatemala 	t	the Republic of Guatemala 	UN member 	GT	GTM	320	.gt 	Guatemala City	18687881	107160	174	15.783471	-90.230759	14.6127	-90.5307
864bc0b6341844f78b6445d46ffa24c3	Bermuda 	t	Bermuda 	United Kingdom 	BM	BMU	060	.bm 		0	0	0	32.321384	-64.757370	32.2915	-64.7780
a087e4b87745448486d0ba95f9fe20da	Brazil 	t	the Federative Republic of Brazil 	UN member 	BR	BRA	076	.br 	Brasilia	212812405	8358140	25	-14.235004	-51.925280	-15.7797	-47.9297
e3ad3559ddfb42758847f1f3c6357a3e	Burkina Faso 	t	Burkina Faso 	UN member 	BF	BFA	854	.bf 	Ouagadougou	24074580	273600	88	12.238333	-1.561593	12.3642	-1.5383
455c314658e041479451fe8b11610dd4	Burundi 	t	the Republic of Burundi 	UN member 	BI	BDI	108	.bi 	Gitega[3]	14390003	25680	560	-3.373056	29.918886	-3.3822	29.3644
d4c7ae6731c74c6ca46654a6d12d51a6	Brunei Darussalam 	t	Brunei Darussalam 	UN member 	BN	BRN	096	.bn 	Bandar Seri Begawan	466330	5270	88	4.535277	114.727669	4.9403	114.9481
c4e3a5419a52412baf5f7cb9ef9cc210	Bouvet Island 	t	Bouvet Island 	Norway 	BV	BVT	074	 		0	0	0	-54.423199	3.413194	0.0000	0.0000
8c5e20a03a4f4ec7b39f552c76ed8735	Belize 	t	Belize 	UN member 	BZ	BLZ	084	.bz 	Belmopan	422924	22810	19	17.189877	-88.497650	17.2500	-88.7667
808234a9f8ef487ea54bf07da5031123	Bhutan 	t	the Kingdom of Bhutan 	UN member 	BT	BTN	064	.bt 	Thimphu	796682	38117	21	27.514162	90.433601	27.4661	89.6419
c3a5250e38844590bfb3d19efbb5df48	Malaysia 	t	Malaysia 	UN member 	MY	MYS	458	.my 	Kuala Lumpur	35977838	328550	110	4.210484	101.975766	3.1412	101.6865
67f73e512cfb4263889ace975f9f493b	Chile 	t	the Republic of Chile 	UN member 	CL	CHL	152	.cl 	Santiago	19859921	743532	27	-35.675147	-71.542969	-33.4569	-70.6483
3c185adeb31b4c239b2bec0bf9816f72	Equatorial Guinea 	t	the Republic of Equatorial Guinea 	UN member 	GQ	GNQ	226	.gq 	Malabo	1938431	28050	69	1.650801	10.267895	3.7500	8.7833
636aa74dee534f82863c71f26ed16446	American Samoa 	t	American Samoa 	United States 	AS	ASM	016	.as 		0	0	0	-14.270972	-170.132217	-14.2781	-170.7025
7bc6f5aef0f34e52be99d9d7c9a26171	Libya 	t	the State of Libya 	UN member 	LY	LBY	434	.ly 	Tripoli	7458555	1759540	4	26.335100	17.228331	32.8752	13.1875
b149e454f8054711af32afacc63b8aa5	Gabon 	t	the Gabonese Republic 	UN member 	GA	GAB	266	.ga 	Libreville	2593130	257670	10	-0.803689	11.609444	0.3925	9.4537
4e07cbbd4cdb4946bc952a91af686cea	Indonesia 	t	the Republic of Indonesia 	UN member 	ID	IDN	360	.id 	Jakarta[9]	285721236	1811570	158	-0.789275	113.921327	-6.2118	106.8416
02d4a21a55f1415e8ef58503c9800464	Nauru 	t	the Republic of Nauru 	UN member 	NR	NRU	520	.nr 	No official capital	12025	20	601	-0.522778	166.931503	-0.5308	166.9112
8fcc563cd1384875b140cfbd13a1a76b	British Indian Ocean Territory (the) 	t	the British Indian Ocean Territory 	United Kingdom 	IO	IOT	086	.io 		0	0	0	-6.343194	71.876519	0.0000	0.0000
137ed56d73864f4d947a8d8bc970fab1	Angola 	t	the Republic of Angola 	UN member 	AO	AGO	024	.ao 	Luanda	39040039	1246700	31	-11.202692	17.873887	-8.8368	13.2343
f303fac117c8403eb0843b1b05aef1e3	Seychelles 	t	the Republic of Seychelles 	UN member 	SC	SYC	690	.sc 	Victoria	132779	460	289	-4.679574	55.491977	-4.6167	55.4500
31ee3348185640a9b4a84a83af8a2948	Mauritius 	t	the Republic of Mauritius 	UN member 	MU	MUS	480	.mu 	Port Louis	1268280	2030	625	-20.348404	57.552152	-20.1619	57.4989
860fb228cb2140bf9a1a6f9f2985fab0	Saint Kitts and Nevis 	t	the Federation of Saint Kitts and Nevis 	UN member 	KN	KNA	659	.kn 	Basseterre	46922	260	180	17.357822	-62.782998	17.2948	-62.7261
63a8aa3e16e843e88d782ceebfe39fc4	Portugal 	t	the Portuguese Republic 	UN member 	PT	PRT	620	.pt 	Lisbon	10411834	91590	114	39.399872	-8.224454	38.7169	-9.1399
2f4a4129d3a24cadbbb0b354c32a61f9	Algeria 	t	the People's Democratic Republic of Algeria 	UN member 	DZ	DZA	012	.dz 	Algiers	47435312	2381740	20	28.033886	1.659626	36.7525	3.0420
6eaff9f38e364c8f82f97998d3ab3da2	Somalia 	t	the Federal Republic of Somalia 	UN member 	SO	SOM	706	.so 	Mogadishu	19654739	627340	31	5.152149	46.199616	2.0416	45.3435
5328026725d04d3582727f4ce64cec38	Afghanistan 	t	the Islamic Republic of Afghanistan 	UN member 	AF	AFG	004	.af 	Kabul	43844111	652860	67	33.939110	67.709953	34.5289	69.1725
8b302cc7623243ad989b0692603140f0	Argentina 	t	the Argentine Republic 	UN member 	AR	ARG	032	.ar 	Buenos Aires	45851378	2736690	17	-38.416097	-63.616672	-34.6051	-58.4004
8b5a4337f6694162b81dd591bd2f2058	Dominica 	t	the Commonwealth of Dominica 	UN member 	DM	DMA	212	.dm 	Roseau	65871	750	88	15.414999	-61.370976	15.3017	-61.3881
8f4f03933073430c9d5a55252fb25805	Bosnia and Herzegovina 	t	Bosnia and Herzegovina 	UN member 	BA	BIH	070	.ba 	Sarajevo	3140095	51000	62	43.915886	17.679076	43.8486	18.3564
4b8554904bb6407f8fbb369ad11e42b3	Central African Republic (the) 	t	the Central African Republic 	UN member 	CF	CAF	140	.cf 	Bangui	5513282	622980	9	6.611111	20.939444	4.3612	18.5550
807ab187a9a540daabf52f292d929882	Bangladesh 	t	the People's Republic of Bangladesh 	UN member 	BD	BGD	050	.bd 	Dhaka	175686899	130170	1350	23.684994	90.356331	23.7104	90.4074
7c01d6f29bff4d50bb1319bf33016e68	Chad 	t	the Republic of Chad 	UN member 	TD	TCD	148	.td 	N'Djamena	21003705	1259200	17	15.454166	18.732207	12.1067	15.0444
156bf8a82de94bf1aa7d47447c64ee62	Cocos (Keeling) Islands (the) 	t	the Territory of Cocos (Keeling) Islands 	Australia 	CC	CCK	166	.cc 		0	0	0	-12.164165	96.870956	0.0000	0.0000
240a2061068548809f1fba0a42198f2a	Djibouti 	t	the Republic of Djibouti 	UN member 	DJ	DJI	262	.dj 	Djibouti	1184076	23180	51	11.825138	42.590275	11.5877	43.1447
502f15a4562c4871b2cf938a193bcb19	Cuba 	t	the Republic of Cuba 	UN member 	CU	CUB	192	.cu 	Havana	10937203	106440	103	21.521757	-77.781167	23.1195	-82.3785
427689dacbee4a66a46e7cb8be077d9b	Costa Rica 	t	the Republic of Costa Rica 	UN member 	CR	CRI	188	.cr 	San Jose	5152950	51060	101	9.748917	-83.753428	9.9278	-84.0807
3808f884128f42b4a30a95a24c0261d4	Côte d'Ivoire 	t	the Republic of Côte d'Ivoire 	UN member 	CI	CIV	384	.ci 	Yamoussoukro	32711547	318000	103	7.539989	-5.547080	5.3453	-4.0268
77c6510830134c74a5a73fbac5af792a	Curaçao 	t	the Country of Curaçao 	Netherlands 	CW	CUW	531	.cw 		0	0	0	0.000000	0.000000	12.1084	-68.9335
55d0c494f89f4aaa863a56ca17af826e	Christmas Island 	t	the Territory of Christmas Island 	Australia 	CX	CXR	162	.cx 		0	0	0	-10.447525	105.690449	0.0000	0.0000
bfa589c6e5ce4295a0db635fa35942be	Denmark 	t	the Kingdom of Denmark 	UN member 	DK	DNK	208	.dk 	Copenhagen	6002507	42430	141	56.263920	9.501785	55.6759	12.5655
f332e697e96345f6b3d14bfe3982091b	Ghana 	t	the Republic of Ghana 	UN member 	GH	GHA	288	.gh 	Accra	35064272	227540	154	7.946527	-1.023194	5.5560	-0.1969
574ae2cdd2d649ceaec508e29c2e2367	Egypt 	t	the Arab Republic of Egypt 	UN member 	EG	EGY	818	.eg 	Cairo	118365995	995450	119	26.820553	30.802498	30.0392	31.2394
24253188d2a8442e9989c6dae78f8cbb	Dominican Republic (the) 	t	the Dominican Republic 	UN member 	DO	DOM	214	.do 	Santo Domingo	11520487	48320	238	18.735693	-70.162651	18.4896	-69.9018
3ec3d13944b946d4ae6e04ffde6efddc	Eritrea 	t	the State of Eritrea 	UN member 	ER	ERI	232	.er 	Asmara	3607003	101000	36	15.179384	39.782334	15.3333	38.9333
1aa5bdef6b204d72b65f089e8faf0c91	French Guiana 	t	Guyane 	France 	GF	GUF	254	.gf 		0	0	0	3.933889	-53.125782	4.9333	-52.3333
70ea9e0fb04d40d6b68dd66902be55dc	Fiji 	t	the Republic of Fiji 	UN member 	FJ	FJI	242	.fj 	Suva	933154	18270	51	-16.578193	179.414413	-18.1416	178.4415
9dfdf5b63db54c98a623b65bc098cbb8	Estonia 	t	the Republic of Estonia 	UN member 	EE	EST	233	.ee 	Tallinn	1344232	42390	32	58.595272	25.013607	59.4370	24.7535
2f7e567ce96841bd821969502da6a05c	Finland 	t	the Republic of Finland 	UN member 	FI	FIN	246	.fi 	Helsinki	5623329	303890	19	61.924110	25.748151	60.1692	24.9402
e57e24a057c14511b6f369d16f115c66	France 	t	the French Republic 	UN member 	FR	FRA	250	.fr 	Paris	66650804	547557	122	46.227638	2.213749	48.8534	2.3488
57462ca71d894451a62919c887a413ab	French Polynesia 	t	Overseas Lands of French Polynesia 	France 	PF	PYF	258	.pf 		0	0	0	-17.679742	-149.406843	-17.5333	-149.5667
eda58797882b4fbab1ca9cea230eb138	Faroe Islands (the) 	t	the Faroe Islands 	Denmark 	FO	FRO	234	.fo 		0	0	0	61.892635	-6.911806	0.0000	0.0000
83e46118fcd040d2a8882945069a41db	Georgia 	t	Georgia 	UN member 	GE	GEO	268	.ge 	Tbilisi	3806671	69490	55	42.315407	43.356892	41.6941	44.8337
cd9b07cbb8c04d7d97410a9ecdfa34cb	Guadeloupe 	t	Guadeloupe 	France 	GP	GLP	312	.gp 		0	0	0	16.995971	-62.067641	15.9985	-61.7255
078f43607de24c8ca15406ffcb5b06a8	Germany 	t	the Federal Republic of Germany 	UN member 	DE	DEU	276	.de 	Berlin	84075075	348560	241	51.165691	10.451526	52.5244	13.4105
4c53c7f3a83b4c12a85d480d440e50fe	Gibraltar 	t	Gibraltar 	United Kingdom 	GI	GIB	292	.gi 		0	0	0	36.137741	-5.345374	36.1447	-5.3526
024cc1942fd04213986fe2250f4b3bcc	Guinea-Bissau 	t	the Republic of Guinea-Bissau 	UN member 	GW	GNB	624	.gw 	Bissau	2249515	28120	80	11.803749	-15.180413	11.8636	-15.5977
74938bdc9a9c4cc59c49225cc8deb3cf	Greece 	t	the Hellenic Republic 	UN member 	GR	GRC	300	.gr 	Athens	9938844	128900	77	39.074208	21.824312	37.9534	23.7490
c9b19371b76e44ceb854493fe435dbb0	Grenada 	t	Grenada 	UN member 	GD	GRD	308	.gd 	Saint George's	117303	340	345	12.262776	-61.604171	12.0564	-61.7485
1a77630e78ca40cf885acf52f7d4b025	Bahrain 	t	the Kingdom of Bahrain 	UN member 	BH	BHR	048	.bh 	Manama	1643332	760	2162	25.930414	50.637772	26.2154	50.5832
190bbaae4c9b401eba1442faa734fb40	Guam 	t	Guam 	United States 	GU	GUM	316	.gu 		0	0	0	13.444304	144.793731	13.4757	144.7489
0bd8fb67e347446e8fb08e645e4d30ce	Greenland 	t	Greenland 	Denmark 	GL	GRL	304	.gl 		0	0	0	71.706936	-42.604303	64.1835	-51.7216
f583373cbd5d4fedb5baa33a49cfbe80	New Caledonia 	t	New Caledonia 	France 	NC	NCL	540	.nc 		0	0	0	-20.904305	165.618042	-22.2763	166.4572
117fa41a2af2423394600bd9d6134d1d	Bahamas (the) 	t	the Commonwealth of The Bahamas 	UN member 	BS	BHS	044	.bs 	Nassau	403033	10010	40	25.034280	-77.396280	25.0582	-77.3431
bda351461af24979afd6bcce6039eab2	Cayman Islands (the) 	t	the Cayman Islands 	United Kingdom 	KY	CYM	136	.ky 		0	0	0	19.513469	-80.566956	0.0000	0.0000
f4e26d94ea3b437dbd86ee43e252ab51	Eswatini 	t	the Kingdom of Eswatini 	UN member 	SZ	SWZ	748	.sz 	Mbabane	1256174	17200	73	-26.522503	31.465866	-26.3167	31.1333
11bd110ae7a047bc82a3b6d39403bcd7	Botswana 	t	the Republic of Botswana 	UN member 	BW	BWA	072	.bw 	Gaborone	2562122	566730	5	-22.328474	24.684866	-24.6545	25.9086
784b0c55e1634c1eb2b5b0ab66f162c3	Colombia 	t	the Republic of Colombia 	UN member 	CO	COL	170	.co 	Bogota	53425635	1109500	48	4.570868	-74.297333	4.6097	-74.0818
1b04e9d6d68c4647b2110d3b83fd5613	French Southern Territories (the) 	t	the French Southern and Antarctic Lands 	France 	TF	ATF	260	.tf 		0	0	0	-49.280366	69.348557	0.0000	0.0000
6208733b902b45e7957a75b7b3876144	Cyprus 	t	the Republic of Cyprus 	UN member 	CY	CYP	196	.cy 	Nicosia	1370754	9240	148	35.126413	33.429859	35.1595	33.3669
f5ead37d4a7f4e6db07d2861349a8353	Heard Island and McDonald Islands 	t	the Territory of Heard Island and McDonald Islands 	Australia 	HM	HMD	334	.hm 		0	0	0	-53.081810	73.504158	0.0000	0.0000
2603132f81b24044ba5aa427b2d84026	Iraq 	t	the Republic of Iraq 	UN member 	IQ	IRQ	368	.iq 	Baghdad	47020774	434320	108	33.223191	43.679291	33.3406	44.4009
150c31b7621e45e6bba870e786f65930	Iceland 	t	Iceland 	UN member 	IS	ISL	352	.is 	Reykjavik	398266	100250	4	64.963051	-19.020835	64.1355	-21.8954
ff6dd13ae2d84d8d8bab013f8d14fc3f	Ireland 	t	Ireland 	UN member 	IE	IRL	372	.ie 	Dublin	5308039	68890	77	53.412910	-8.243890	53.3331	-6.2489
a9fe499c2fb14c5982f6befbdde19755	Jordan 	t	the Hashemite Kingdom of Jordan 	UN member 	JO	JOR	400	.jo 	Amman	11520684	88780	130	30.585164	36.238414	31.9552	35.9450
ff09a4b9720d4988b7a965e4d26b44d3	Kenya 	t	the Republic of Kenya 	UN member 	KE	KEN	404	.ke 	Nairobi	57532493	569140	101	-0.023559	37.906193	-1.2833	36.8167
24f2e5e93cae45059ca6030468512e78	Kuwait 	t	the State of Kuwait 	UN member 	KW	KWT	414	.kw 	Kuwait City	5026078	17820	282	29.311660	47.481766	29.3697	47.9783
654bdba7f8f348f88a7ce2c419f716cd	Japan 	t	Japan 	UN member 	JP	JPN	392	.jp 	Tokyo	123103479	364555	338	36.204824	138.252924	35.6895	139.6917
ee2b8320ced14ba7a18e563213679fbf	Israel 	t	the State of Israel 	UN member 	IL	ISR	376	.il 	Jerusalem	9517181	21640	440	31.046051	34.851612	31.7690	35.2163
ea8fd330333c47f89cad9cf038d3ed37	India 	t	the Republic of India 	UN member 	IN	IND	356	.in 	New Delhi	1463865525	2973190	492	20.593684	78.962880	28.6667	77.2167
fe5a50ca94e84a9897c8c0ca950113a6	Jersey 	t	the Bailiwick of Jersey 	British Crown 	JE	JEY	832	.je 		0	0	0	49.214439	-2.131250	0.0000	0.0000
653b9c32c19c43a188f39295e8f880ec	Hungary 	t	Hungary 	UN member 	HU	HUN	348	.hu 	Budapest	9632287	90530	106	47.162494	19.503304	47.4980	19.0399
aed25f0bf3564d3bb9bea98e32fdbab1	Latvia 	t	the Republic of Latvia 	UN member 	LV	LVA	428	.lv 	Riga	1853559	62200	30	56.879635	24.603189	56.9460	24.1059
01b353440a564ec1a2bba337854a23ee	Iran (Islamic Republic of) 	t	the Islamic Republic of Iran 	UN member 	IR	IRN	364	.ir 	Tehran	92417681	1628550	57	32.427908	53.688046	35.6944	51.4215
022d32f2ab074a9382f500cadd4d7218	Cameroon 	t	the Republic of Cameroon 	UN member 	CM	CMR	120	.cm 	Yaounde	29879337	472710	63	7.369722	12.354722	3.8667	11.5167
e729bb88028b4414aa82f53f76ca4cd2	Korea (the Democratic People's Republic of) 	t	the Democratic People's Republic of Korea 	UN member 	KP	PRK	408	.kp 	Pyongyang	26571036	120410	221	40.339852	127.510093	0.0000	0.0000
994cf9b130ba4334b9f1bd734ee5c276	Cambodia 	t	the Kingdom of Cambodia 	UN member 	KH	KHM	116	.kh 	Phnom Penh	17847982	176520	101	12.565679	104.990963	11.5625	104.9160
ebbfc2275c1e448880626588619e8fcd	Lebanon 	t	the Lebanese Republic 	UN member 	LB	LBN	422	.lb 	Beirut	5849421	10230	572	33.854721	35.862285	33.9000	35.4833
b833644bbae645c78c02957bae6a40b2	Lao People's Democratic Republic (the) 	t	the Lao People's Democratic Republic 	UN member 	LA	LAO	418	.la 		0	0	0	19.856270	102.495496	0.0000	0.0000
092d5e2a2ee54c1491908a05db0475a8	Marshall Islands (the) 	t	the Republic of the Marshall Islands 	UN member 	MH	MHL	584	.mh 	Majuro	36282	180	202	7.131474	171.184478	7.0897	171.3803
dec12a98428144ef90f3f82acc76a2ae	Luxembourg 	t	the Grand Duchy of Luxembourg 	UN member 	LU	LUX	442	.lu 	Luxembourg	680453	2590	263	49.815273	6.129583	49.6117	6.1300
c6585b56a788400282a05a72dfcea0a0	Madagascar 	t	the Republic of Madagascar 	UN member 	MG	MDG	450	.mg 	Antananarivo	32740678	581795	56	-18.766947	46.869107	-18.9137	47.5361
d1e656ad668542a8a7067adc93a1ad0f	Liberia 	t	the Republic of Liberia 	UN member 	LR	LBR	430	.lr 	Monrovia	5731206	96320	60	6.428055	-9.429499	6.3005	-10.7969
041a58bc4f004caf9eaeddbc8f9f35ba	Malawi 	t	the Republic of Malawi 	UN member 	MW	MWI	454	.mw 	Lilongwe	22216120	94280	236	-13.254308	34.301525	-13.9669	33.7873
13fc06b6ce694d299a3e80b5e01ee20e	Lesotho 	t	the Kingdom of Lesotho 	UN member 	LS	LSO	426	.ls 	Maseru	2363325	30360	78	-29.609988	28.233608	-29.3167	27.4833
1ae13734c047475d834c3e4e2e905279	Myanmar 	t	the Republic of the Union of Myanmar 	UN member 	MM	MMR	104	.mm 	Nay Pyi Taw	54850648	653290	84	21.913965	95.956223	19.7450	96.1297
900571656ede4869b9c2b34dc8166185	Mongolia 	t	Mongolia 	UN member 	MN	MNG	496	.mn 	Ulaanbaatar	3517100	1553560	2	46.862496	103.846656	47.9077	106.8832
1c341e22410549f68b5b7cffa82d7cc5	Morocco 	t	the Kingdom of Morocco 	UN member 	MA	MAR	504	.ma 	Rabat	38430770	446300	86	31.791702	-7.092620	34.0133	-6.8326
1ad1473a62a643d4a84aad5ff0c98629	Mali 	t	the Republic of Mali 	UN member 	ML	MLI	466	.ml 	Bamako	25198821	1220190	21	17.570692	-3.996166	12.6500	-8.0000
5e134176e2654b7b96714517789f6f07	Mauritania 	t	the Islamic Republic of Mauritania 	UN member 	MR	MRT	478	.mr 	Nouakchott	5315065	1030700	5	21.007890	-10.940835	18.0858	-15.9785
6b404a110a054112af38b0e4e5aefdd1	Malta 	t	the Republic of Malta 	UN member 	MT	MLT	470	.mt 	Valletta	545405	320	1704	35.937496	14.375416	35.8997	14.5147
b0f57bead7b44e0caf85e8515d328c60	Montenegro 	t	Montenegro 	UN member 	ME	MNE	499	.me 	Podgorica	632729	13450	47	42.708678	19.374390	42.4411	19.2636
3dfccf0edb804368a4dee440a46182b2	Mayotte 	t	the Department of Mayotte 	France 	YT	MYT	175	.yt 		0	0	0	-12.827500	45.166244	-12.7794	45.2272
63bf5d6cebab4739b1fc2299eec9d0bf	Monaco 	t	the Principality of Monaco 	UN member 	MC	MCO	492	.mc 	Monaco	38341	1	25732	43.750298	7.412841	43.7333	7.4167
b5566729e8724f16bec681234169178d	Namibia 	t	the Republic of Namibia 	UN member 	NA	NAM	516	.na 		0	0	0	-22.957640	18.490410	-22.5594	17.0832
14e748e33bb84f008bd94a7b75ec0322	Martinique 	t	Martinique 	France 	MQ	MTQ	474	.mq 		0	0	0	14.641528	-61.024174	14.6089	-61.0733
2b3c79930de64998aa60bd7ba7172e1c	Haiti 	t	the Republic of Haiti 	UN member 	HT	HTI	332	.ht 	Port au Prince	11906095	27560	432	18.971187	-72.285215	18.5392	-72.3350
092c6e58237d49b3b7685084628f9a67	Montserrat 	t	Montserrat 	United Kingdom 	MS	MSR	500	.ms 		0	0	0	16.742498	-62.187366	16.7918	-62.2106
971680dd91324cffaaaa84af547617cd	Korea (the Republic of) 	t	the Republic of Korea 	UN member 	KR	KOR	410	.kr 	Seoul	51667029	97230	531	35.907757	127.766922	37.5683	126.9778
b0e9f0bc05084abca6ba83fa37805c96	Holy See (the) 	t	the Holy See 	UN observer 	VA	VAT	336	.va 		0	0	0	41.902916	12.453389	0.0000	0.0000
aaa0a50a99344d16bbab4a95f8d606cd	Mexico 	t	the United Mexican States 	UN member 	MX	MEX	484	.mx 	Mexico City	131946900	1943950	68	23.634501	-102.552784	19.4273	-99.1419
099ef35db365439dba82878b046b60c6	Saint Barthélemy 	t	the Collectivity of Saint-Barthélemy 	France 	BL	BLM	652	.bl 		0	0	0	0.000000	0.000000	0.0000	0.0000
b118b3a3d7f947e79e32b10ba30c3efb	Saint Martin (French part) 	t	the Collectivity of Saint-Martin 	France 	MF	MAF	663	.mf 		0	0	0	0.000000	0.000000	0.0000	0.0000
62b4ad652e644d5d87de9fe296173655	United States Minor Outlying Islands (the) 	t	United States Pacific Island Wildlife Refuges, Navassa Island, and Wake Island 	United States 	UM	UMI	581	 		0	0	0	0.000000	0.000000	0.0000	0.0000
a550ffa6cdc3404b8fcc121eed666ee9	  Nepal 	t	the Federal Democratic Republic of Nepal 	UN member 	NP	NPL	524	.np 	Kathmandu	29618118	143350	207	28.394857	84.124008	27.7017	85.3206
dd071a653ae6481386b81c7f71ba1ee0	Nigeria 	t	the Federal Republic of Nigeria 	UN member 	NG	NGA	566	.ng 	Abuja	237527782	910770	261	9.081999	8.675277	9.0574	7.4898
e9e64c3836e64be0a98bb810cf662a41	Norfolk Island 	t	the Territory of Norfolk Island 	Australia 	NF	NFK	574	.nf 		0	0	0	-29.040835	167.954712	0.0000	0.0000
199717a39be243288ac5108721d0157b	Pakistan 	t	the Islamic Republic of Pakistan 	UN member 	PK	PAK	586	.pk 	Islamabad	255219554	770880	331	30.375321	69.345116	33.7035	73.0594
8685ab38f6bc4948a86c2077eb337ef9	Niue 	t	Niue 	New Zealand 	NU	NIU	570	.nu 		0	0	0	-19.054445	-169.867233	-19.0585	-169.9213
8c36861ce4d44404979c26ce41bed969	New Zealand 	t	New Zealand 	UN member 	NZ	NZL	554	.nz 	Wellington	5251899	263310	20	-40.900557	174.885971	-41.2866	174.7756
b1559e1a628f448d91ea884a02e8649b	Oman 	t	the Sultanate of Oman 	UN member 	OM	OMN	512	.om 	Muscat	5494691	309500	18	21.512583	55.923255	23.6139	58.5922
d9e64d0697d44605acac6b5cb336156f	Nicaragua 	t	the Republic of Nicaragua 	UN member 	NI	NIC	558	.ni 	Managua	7007502	120340	58	12.865416	-85.207229	12.1328	-86.2504
2e300aae99d3427dba2cc7f7fb0b595f	Palau 	t	the Republic of Palau 	UN member 	PW	PLW	585	.pw 	Melekeok	17663	460	38	7.514980	134.582520	7.3426	134.4789
164f6bcb817a4d6da684053daf06db58	Puerto Rico 	t	the Commonwealth of Puerto Rico 	United States 	PR	PRI	630	.pr 		0	0	0	18.220833	-66.590149	18.4663	-66.1057
0a18a1215077473bbbb198f6c8f8dc4c	Peru 	t	the Republic of Peru 	UN member 	PE	PER	604	.pe 	Lima	34576665	1280000	27	-9.189967	-75.015152	-12.0432	-77.0282
42b6abf02148423196e7f6511b835e84	Saint Lucia 	t	Saint Lucia 	UN member 	LC	LCA	662	.lc 	Castries	180149	610	295	13.909444	-60.978893	14.0060	-60.9910
6e597be5aa8d4dd193ad5c1a6f3c1084	Papua New Guinea 	t	the Independent State of Papua New Guinea 	UN member 	PG	PNG	598	.pg 	Port Moresby	10762817	452860	24	-6.314993	143.955550	-9.4431	147.1797
5cfa145853cf442fa16d6f3f039b6700	Sao Tome and Principe 	t	the Democratic Republic of São Tomé and Príncipe 	UN member 	ST	STP	678	.st 	Sao Tome	240254	960	250	0.186360	6.613081	0.3365	6.7273
53659b336ffb4fc5bc2984e76f30b7a2	Pitcairn 	t	the Pitcairn, Henderson, Ducie and Oeno Islands 	United Kingdom 	PN	PCN	612	.pn 		0	0	0	-24.703615	-127.439308	0.0000	0.0000
1669adfc51a94e1b88c62ed8b8d871cd	Réunion 	t	Réunion 	France 	RE	REU	638	.re 		0	0	0	-21.115141	55.536384	-20.8823	55.4504
743e9720064646fd83b44f195dcad491	Paraguay 	t	the Republic of Paraguay 	UN member 	PY	PRY	600	.py 	Asuncion	7013078	397300	18	-23.442503	-58.443832	-25.3007	-57.6359
8cdaddce401d4638986661b73fa7c78b	Philippines (the) 	t	the Republic of the Philippines 	UN member 	PH	PHL	608	.ph 	Manila	116786962	298170	392	12.879721	121.774017	14.6042	120.9822
f233734150454e4eb171037176cefd2e	Romania 	t	Romania 	UN member 	RO	ROU	642	.ro 	Bucharest	18908650	230170	82	45.943161	24.966760	44.4328	26.1043
9fc6d82b92a24b13b0161547dcbc250b	Saint Pierre and Miquelon 	t	the Overseas Collectivity of Saint-Pierre and Miquelon 	France 	PM	SPM	666	.pm 		0	0	0	46.941936	-56.271110	46.7738	-56.1815
06771d7536fc4ce8b5f15c054b13f1f3	Sint Maarten (Dutch part) 	t	Sint Maarten 	Netherlands 	SX	SXM	534	.sx 		0	0	0	0.000000	0.000000	18.0260	-63.0458
7ae8021f5a8e403283d08a2e9a3bfc52	Russian Federation (the) 	t	the Russian Federation 	UN member 	RU	RUS	643	.ru 	Moscow	143997393	16376870	9	61.524010	105.318756	0.0000	0.0000
31c72ff2bd6e44e89e92a9bbce71f524	Serbia 	t	the Republic of Serbia 	UN member 	RS	SRB	688	.rs 	Belgrade	6689039	87460	76	44.016521	21.005859	44.8176	20.4633
13273a60081040b18c65adf405124714	South Sudan 	t	the Republic of South Sudan 	UN member 	SS	SSD	728	.ss 	Juba	12188788	610952	20	0.000000	0.000000	4.8517	31.5825
e86464d0249d4d809c191fbb792406b3	South Africa 	t	the Republic of South Africa 	UN member 	ZA	ZAF	710	.za 	Pretoria, Bloemfontein, Cape Town	64747319	1213090	53	-30.559482	22.937506	-33.9258	18.4232
01bda0d8388f40068e1544aef9bb212d	Solomon Islands 	t	the Solomon Islands 	UN member 	SB	SLB	090	.sb 	Honiara	838645	27990	30	-9.645710	160.156194	-9.4333	159.9500
869cf54c990248c8ac6f53284a731357	SvalbardJan Mayen 	t	Svalbard and Jan Mayen 	Norway 	SJ	SJM	744	 		0	0	0	77.553604	23.670272	0.0000	0.0000
e1cc9899a5b24754b1bc4f59a69cc57d	Slovenia 	t	the Republic of Slovenia 	UN member 	SI	SVN	705	.si 	Ljubljana	2117072	20140	105	46.151241	14.995463	46.0511	14.5051
cacadfae0104400bb11e17b39c6e98d0	Singapore 	t	the Republic of Singapore 	UN member 	SG	SGP	702	.sg 	Singapore	5870750	700	8387	1.352083	103.819836	1.2897	103.8501
d6026a074df54cf0a880f43fe7a537cf	Senegal 	t	the Republic of Senegal 	UN member 	SN	SEN	686	.sn 	Dakar	18931966	192530	98	14.497401	-14.452362	14.6937	-17.4441
b5b6f1d99264484eb67cba8149738682	Sierra Leone 	t	the Republic of Sierra Leone 	UN member 	SL	SLE	694	.sl 	Freetown	8819794	72180	122	8.460555	-11.779889	8.4840	-13.2299
3e0aabb490ed471db58e5e1406180f03	Saudi Arabia 	t	the Kingdom of Saudi Arabia 	UN member 	SA	SAU	682	.sa 	Riyadh	34566328	2149690	16	23.885942	45.079162	24.6905	46.7096
f5ce06bd0d0a40fb91a7784a3af0f2c0	Samoa 	t	the Independent State of Samoa 	UN member 	WS	WSM	882	.ws 	Apia	219306	2830	77	-13.759029	-172.104629	-13.8333	-171.7667
cf8913267d6b44789f9df51363c59789	San Marino 	t	the Republic of San Marino 	UN member 	SM	SMR	674	.sm 	San Marino	33572	60	560	43.942360	12.457777	43.9333	12.4500
c6a631906b7d4d9db7a65a57f2c23edd	Tokelau 	t	Tokelau 	New Zealand 	TK	TKL	772	.tk 		0	0	0	-8.967363	-171.855881	-9.3800	-171.2500
4e3846239fe8480aa5661ed8bf89df3c	Niger (the) 	t	the Republic of the Niger 	UN member 	NE	NER	562	.ne 	Niamey	27917831	1266700	22	17.607789	8.081666	13.5137	2.1098
94bf8da6598f4414883663c1c235d619	Saint Vincent and the Grenadines 	t	Saint Vincent and the Grenadines 	UN member 	VC	VCT	670	.vc 	Kingstown	99924	390	256	12.984305	-61.287228	13.1587	-61.2248
0335bb9d55994bd8a7050a15432cc1dd	Viet Nam 	t	the Socialist Republic of Viet Nam 	UN member 	VN	VNM	704	.vn 	Hanoi	101598527	310070	328	14.058324	108.277199	21.0245	105.8412
7a4de2421f094401a4a85586510bd0f3	Czechia 	t	the Czech Republic 	UN member 	CZ	CZE	203	.cz 	Prague	10609239	77240	137	49.817492	15.472962	50.0880	14.4208
9e4e200dbd304b86ac88d706218c737e	Albania 	t	the Republic of Albania 	UN member 	AL	ALB	008	.al 	Tirana	2771508	27400	101	41.153332	20.168331	41.3275	19.8189
85254da5c4e849969d8c3c2689e1741c	Cook Islands (the) 	t	the Cook Islands 	New Zealand 	CK	COK	184	.ck 		0	0	0	-21.236736	-159.777671	0.0000	0.0000
30fcc64ddce34e33a5ded94a5df27cc4	 Switzerland 	t	the Swiss Confederation 	UN member 	CH	CHE	756	.ch 	Bern	8967407	39516	227	46.818188	8.227512	46.9481	7.4474
c791015bde6943339b887b57275f78b7	Sudan (the) 	t	the Republic of the Sudan 	UN member 	SD	SDN	729	.sd 	Khartoum	51662147	1765048	29	12.862807	30.217636	0.0000	0.0000
3be1e50efbcd41069c4957badaf32a36	Thailand 	t	the Kingdom of Thailand 	UN member 	TH	THA	764	.th 	Bangkok	71619863	510890	140	15.870032	100.992541	13.7220	100.5252
80bb770985cc4b4fb4ec9468324f06c1	Syrian Arab Republic (the) 	t	the Syrian Arab Republic 	UN member 	SY	SYR	760	.sy 	Damascus	25620427	183630	140	34.802075	38.996815	0.0000	0.0000
0e7d334cbaf04834b9cdc5389ef17569	Türkiye 	t	the Republic of Türkiye 	UN member 	TR	TUR	792	.tr 	Ankara	87685426	769630	114	38.963745	35.243322	39.9199	32.8543
3532cb45ce2e40be8f2d8f3717644c4d	Togo 	t	the Togolese Republic 	UN member 	TG	TGO	768	.tg 	Lome	9721608	54390	179	8.619543	0.824782	6.1375	1.2123
fe5d394a5b0c471cb8b69e0ea377c4bd	Tonga 	t	the Kingdom of Tonga 	UN member 	TO	TON	776	.to 	Nuku'alofa	103742	720	144	-21.178986	-175.198242	-21.1394	-175.2032
60e581c7320448359d21bfecd9366f1f	Uruguay 	t	the Oriental Republic of Uruguay 	UN member 	UY	URY	858	.uy 	Montevideo	3384688	175020	19	-32.522779	-55.765835	-34.8335	-56.1674
f57f7d55ff034a229bb308fae4901143	Tuvalu 	t	Tuvalu 	UN member 	TV	TUV	798	.tv 	Funafuti	9492	30	316	-7.109535	177.649330	-8.5189	179.1991
a384ad20da634afcae10e0c55edd6e88	Tunisia 	t	the Republic of Tunisia 	UN member 	TN	TUN	788	.tn 	Tunis	12348573	155360	79	33.886917	9.537499	36.8190	10.1658
b531d2c249814be192f346a4581f4379	Uganda 	t	the Republic of Uganda 	UN member 	UG	UGA	800	.ug 	Kampala	51384894	199810	257	1.373333	32.290275	0.3163	32.5822
aebb013ff37744a8bd6df7ac8ee66166	Venezuela (Bolivarian Republic of) 	t	the Bolivarian Republic of Venezuela 	UN member 	VE	VEN	862	.ve 	Caracas	28516896	882050	32	6.423750	-66.589730	10.4880	-66.8792
76655a806eff47f5bd309bba3eca1467	Taiwan (Province of China) 	t	the Republic of China 	Disputed 	TW	TWN	158	.tw 	Taipei	0	0	0	23.697810	120.960515	0.0000	0.0000
54208f3246cc48c698994a039d1615e5	Zambia 	t	the Republic of Zambia 	UN member 	ZM	ZMB	894	.zm 	Lusaka	21913874	743390	29	-13.133897	27.849332	-15.4134	28.2771
0e726d980d214f58a903b366449f2f5a	Yemen 	t	the Republic of Yemen 	UN member 	YE	YEM	887	.ye 	Sana'a	41773878	527970	79	15.552727	48.516388	15.3531	44.2078
155b49fbe01140a7bbb7f1f9afa4b9e2	United States of America (the) 	t	the United States of America 	UN member 	US	USA	840	.us 	Washington D.C.	347275807	9147420	38	37.090240	-95.712891	0.0000	0.0000
aeaf7327ce7b4d848fbbb7a0617780c7	Zimbabwe 	t	the Republic of Zimbabwe 	UN member 	ZW	ZWE	716	.zw	Harare	16950795	386850	44	-19.015438	29.154857	-17.8294	31.0539
e28e37c1218841b1bcd075197daf585c	Austria 	t	the Republic of Austria 	UN member 	AT	AUT	040	.at 	Vienna	9113574	82409	111	47.516231	14.550072	48.2064	16.3707
fd97ef9daaef4a268c9bd6b6cae01634	Virgin Islands (British) 	t	the Virgin Islands 	United Kingdom 	VG	VGB	092	.vg 		0	0	0	18.420695	-64.639968	0.0000	0.0000
4b057310edd04a3d9c94164bf0e8f1f7	Virgin Islands (U.S.) 	t	the Virgin Islands of the United States 	United States 	VI	VIR	850	.vi 		0	0	0	18.335765	-64.896335	0.0000	0.0000
fe436973d99d465f899a2595c8dd711a	Wallis and Futuna 	t	the Territory of the Wallis and Futuna Islands 	France 	WF	WLF	876	.wf 		0	0	0	-13.768752	-177.156097	0.0000	0.0000
539b6c4b4b66471da63f470e0ac5dbf4	Andorra 	t	the Principality of Andorra 	UN member 	AD	AND	020	.ad 	Andorra la Vella	82904	470	176	42.546245	1.601554	42.5078	1.5211
809f43f8dae840bc9e37c2d28c811b01	Australia 	t	the Commonwealth of Australia 	UN member 	AU	AUS	036	.au 	Canberra	26974026	7682300	4	-25.274398	133.775136	-35.2835	149.1281
e1e5d806b1e9433ab69b1d6e79f95370	-- None --	f								0	0	0	0.000000	0.000000	0.0000	0.0000
f529b67a6bdf467896c2d37689c50744	Ecuador 	t	the Republic of Ecuador 	UN member 	EC	ECU	218	.ec 	Quito	18289896	248360	74	-1.831239	-78.183406	-0.2299	-78.5250
3b8c92acd754486bbed088fed77e2c59	Bolivia (Plurinational State of) 	t	the Plurinational State of Bolivia 	UN member 	BO	BOL	068	.bo 	La Paz , Sucre	12581843	1083300	12	-16.290154	-63.588653	-16.5000	-68.1500
0b2567f230ce4f90ab434a6e98b69dca	Azerbaijan 	t	the Republic of Azerbaijan 	UN member 	AZ	AZE	031	.az 	Baku	10397713	82658	126	40.143105	47.576927	40.3777	49.8920
b4bdb565ed7d45aca0dfb7c8b9a97b11	Bulgaria 	t	the Republic of Bulgaria 	UN member 	BG	BGR	100	.bg 	Sofia	6714560	108560	62	42.733883	25.485830	42.6975	23.3242
86c7dedc3c1641b9a0aa74ebfc30d7c9	China 	t	the People's Republic of China 	UN member 	CN	CHN	156	.cn 	Beijing	1416096094	9388211	151	35.861660	104.195397	39.9075	116.3972
f9fa40bcdf4043ada9adcb2b012651a9	Canada 	t	Canada 	UN member 	CA	CAN	124	.ca 	Ottawa	40126723	9093510	4	56.130366	-106.346771	45.4166	-75.6980
3f823457c78d4f849ee98db81dc85214	Congo (the) 	t	the Republic of the Congo 	UN member 	CG	COG	178	.cg 	Brazzaville	6484437	341500	19	-0.228021	15.827659	-4.2658	15.2832
71714322d4b9486ab1ccd9e8036522e7	Turkmenistan 	t	Turkmenistan 	UN member 	TM	TKM	795	.tm 	Ashgabat	7618847	469930	16	38.969719	59.556278	37.9500	58.3833
58e9cf8b29cd4d98a6dd93a5abe1319a	Tajikistan 	t	the Republic of Tajikistan 	UN member 	TJ	TJK	762	.tj 	Dushanbe	10786734	139960	77	38.861034	71.276093	38.5358	68.7791
7d24c2809ee94701a153dd98d3fe3b3f	Ukraine 	t	Ukraine 	UN member 	UA	UKR	804	.ua 	Kyiv or Kiev	38980376	579320	67	48.379433	31.165580	50.4454	30.5186
09757fa099b5465a8fa93ee116931c65	Sri Lanka 	t	the Democratic Socialist Republic of Sri Lanka 	UN member 	LK	LKA	144	.lk 	Sri Jayawardenapura Kotte	23229470	62710	370	7.873054	80.771797	6.9319	79.8478
b1e3b4b8acaf4453b0dd0e4a38a31db4	Suriname 	t	the Republic of Suriname 	UN member 	SR	SUR	740	.sr 	Paramaribo	639850	156000	4	3.919305	-56.027783	5.8664	-55.1668
697a9eebf11048c48a0e2ca3093d25d6	United Arab Emirates (the) 	t	the United Arab Emirates 	UN member 	AE	ARE	784	.ae 	Abu Dhabi	11346000	83600	136	23.424076	53.847818	0.0000	0.0000
401d41b71d024982829dc1094ed96ae2	Sweden 	t	the Kingdom of Sweden 	UN member 	SE	SWE	752	.se 	Stockholm	10656633	410340	26	60.128161	18.643501	59.3326	18.0649
112b0c05598d4cd3b53ab03722e300ab	Falkland Islands (the)  	t	the Falkland Islands 	United Kingdom 	FK	FLK	238	.fk 		0	0	0	-51.796253	-59.523613	0.0000	0.0000
d8c0df7a54e94586bbacee4bd0413d30	Guernsey 	t	the Bailiwick of Guernsey 	British Crown 	GG	GGY	831	.gg 		0	0	0	49.465691	-2.585278	0.0000	0.0000
a5cc32f189db41a78cc9093d57b9ddd6	South Georgia and the South Sandwich Islands 	t	South Georgia and the South Sandwich Islands 	United Kingdom 	GS	SGS	239	.gs 		0	0	0	-54.429579	-36.587909	0.0000	0.0000
c46e04c90abf4d93accb4bf7d5cb2347	Hong Kong 	t	the Hong Kong Special Administrative Region of China 	China 	HK	HKG	344	.hk 		0	0	0	22.396428	114.109497	0.0000	0.0000
689f606ae7ab45a2bc43fde5e0024505	Gambia (the) 	t	the Republic of The Gambia 	UN member 	GM	GMB	270	.gm 	Banjul	2822093	10120	279	13.443182	-15.310139	13.4531	-16.6794
5d8c66af1d26458fb9a9e79929c6929b	Italy 	t	the Italian Republic 	UN member 	IT	ITA	380	.it 	Rome	59146260	294140	201	41.871940	12.567380	41.8947	12.4811
d0f0c058b8b8424c92ad1bc03357df6b	Kiribati 	t	the Republic of Kiribati 	UN member 	KI	KIR	296	.ki 	Tarawa Atoll	136488	810	169	-3.370417	-168.734039	1.3272	172.9813
04440d669934461f8e2b4a9adb651277	Uzbekistan 	t	the Republic of Uzbekistan 	UN member 	UZ	UZB	860	.uz 	Tashkent	37053428	425400	87	41.377491	64.585262	41.2647	69.2163
b26d2744b30a47e295a73c80c13c332c	Micronesia (Federated States of) 	t	the Federated States of Micronesia 	UN member 	FM	FSM	583	.fm 	Palikir	113683	700	162	7.425554	150.550812	6.9174	158.1588
0f6fee727a864ba58b91f92fcb00df17	Maldives 	t	the Republic of Maldives 	UN member 	MV	MDV	462	.mv 	Male	529676	300	1766	3.202778	73.220680	4.1748	73.5089
eff2de6dba674014a6231b85ea7fd966	Moldova (the Republic of) 	t	the Republic of Moldova 	UN member 	MD	MDA	498	.md 	Chisinau	2996106	32850	91	47.411631	28.369885	0.0000	0.0000
5f6e36aea68f4c7a8d7fb55c53fd39e5	Macao 	t	the Macao Special Administrative Region of China 	China 	MO	MAC	446	.mo 		0	0	0	22.198745	113.543873	0.0000	0.0000
64de217a2c7e427496e2f6c118ee5e73	Northern Mariana Islands (the) 	t	the Commonwealth of the Northern Mariana Islands 	United States 	MP	MNP	580	.mp 		0	0	0	17.330830	145.384690	0.0000	0.0000
3f123365b9bd45f384621a3023a08a35	Panama 	t	the Republic of Panama 	UN member 	PA	PAN	591	.pa 	Panama City	4571189	74340	61	8.537981	-80.782127	8.9958	-79.5196
f6c6be91e01b4ca496e0289841792d96	Norway 	t	the Kingdom of Norway 	UN member 	NO	NOR	578	.no 	Oslo	5623071	365268	15	60.472024	8.468946	59.9127	10.7461
f97c50f8e8504d52b511086455251a28	Rwanda 	t	the Republic of Rwanda 	UN member 	RW	RWA	646	.rw 	Kigali	14569341	24670	591	-1.940278	29.873888	-1.9474	30.0579
8bd2a9901c884d02aee8f0b5a9e31b9f	Poland 	t	the Republic of Poland 	UN member 	PL	POL	616	.pl 	Warsaw	38140910	306230	125	51.919438	19.145136	52.2298	21.0118
6f43526a03bd4484870f56f925db96e7	Qatar 	t	the State of Qatar 	UN member 	QA	QAT	634	.qa 	Doha	3115889	11610	268	25.354826	51.183884	25.2747	51.5245
8f1db7edf42c4308a3e6667f8e4e30ed	Western Sahara 	t	the Sahrawi Arab Democratic Republic 	Disputed 	EH	ESH	732	 		0	0	0	24.215527	-12.885834	27.1532	-13.2014
bd5e7da2c59a4e4287fbc5e54641bee1	Spain 	t	the Kingdom of Spain 	UN member 	ES	ESP	724	.es 	Madrid	47889958	498800	96	40.463667	-3.749220	40.4165	-3.7026
c4e9e5900fe246cd89b34d6420809b0c	Timor-Leste 	t	the Democratic Republic of Timor-Leste 	UN member 	TL	TLS	626	.tl 	Dili	1418517	14870	95	-8.874217	125.727539	-8.5601	125.5668
49ba2f611ce4409fb53e772c93836c76	Saint HelenaAscension IslandTristan da Cunha 	t	Saint Helena, Ascension and Tristan da Cunha 	United Kingdom 	SH	SHN	654	.sh 		0	0	0	-24.143474	-10.030696	0.0000	0.0000
220a3af091014137be662f0096742bd0	Isle of Man 	t	the Isle of Man 	British Crown 	IM	IMN	833	.im 		0	0	0	54.236107	-4.548056	54.1500	-4.4833
0decbd4ba29c4a21a921d9e1e2313c5a	Turks and Caicos Islands (the) 	t	the Turks and Caicos Islands 	United Kingdom 	TC	TCA	796	.tc 		0	0	0	21.694025	-71.797928	0.0000	0.0000
1a857d8e54184b80a0be4d5fccffcb14	Trinidad and Tobago 	t	the Republic of Trinidad and Tobago 	UN member 	TT	TTO	780	.tt 	Port of Spain	1511155	5130	295	10.691803	-61.222503	10.6662	-61.5166
6f8a429e8c02499aabd07d876fd45953	Comoros (the) 	t	the Union of the Comoros 	UN member 	KM	COM	174	.km 	Moroni	882847	1861	474	-11.875001	43.872219	-11.7022	43.2551
0069a5fdd4b949e98164f0675ef2ec2d	Congo (the Democratic Republic of the) 	t	the Democratic Republic of the Congo 	UN member 	CD	COD	180	.cd 	Kinshasa	112832473	2267050	50	-4.038333	21.758664	-4.3276	15.3136
5538ced848ed4bdb95ea637f18500a74	Kyrgyzstan 	t	the Kyrgyz Republic 	UN member 	KG	KGZ	417	.kg 	Bishkek	7295034	191800	38	41.204380	74.766098	42.8700	74.5900
b2faa3d6b53344b3bd0177ac53747ed8	Vanuatu 	t	the Republic of Vanuatu 	UN member 	VU	VUT	548	.vu 	Port Vila	335169	12190	27	-15.376706	166.959158	-17.7338	168.3219
e9ca791418614372ad1284aa57d7f93d	Kazakhstan 	t	the Republic of Kazakhstan 	UN member 	KZ	KAZ	398	.kz 	Astana	20843754	2699700	8	48.019573	66.923684	51.1801	71.4460
3b27f40788734185bac42cf69d136c59	Croatia 	t	the Republic of Croatia 	UN member 	HR	HRV	191	.hr 	Zagreb	3848160	55960	69	45.100000	15.200000	45.8144	15.9780
df3ada9b5e764c48af684dae69f90b01	El Salvador 	t	the Republic of El Salvador 	UN member 	SV	SLV	222	.sv 	San Salvador	6365503	20720	307	13.794185	-88.896530	13.6894	-89.1872
9367abb79d2f4a90b5888c0f963436f9	Guinea 	t	the Republic of Guinea 	UN member 	GN	GIN	324	.gn 	Conakry	15099727	245720	61	9.945587	-9.696645	9.5716	-13.6476
97885074d5e245f3906269720df7693e	Guyana 	t	the Co-operative Republic of Guyana 	UN member 	GY	GUY	328	.gy 	Georgetown	835986	196850	4	4.860416	-58.930180	6.8045	-58.1553
1d955c1e76b440dca7ffcdbff72f8162	Lithuania 	t	the Republic of Lithuania 	UN member 	LT	LTU	440	.lt 	Vilnius	2830144	62674	45	55.169438	23.881275	54.6892	25.2798
1e00a56aaf944bf08cf5e4b09dd108c1	Liechtenstein 	t	the Principality of Liechtenstein 	UN member 	LI	LIE	438	.li 	Vaduz	40128	160	251	47.166000	9.555373	47.1415	9.5215
26e205c547ac4b7f8dcb9351877e5fd6	Mozambique 	t	the Republic of Mozambique 	UN member 	MZ	MOZ	508	.mz 	Maputo	35631653	786380	45	-18.665695	35.529562	-25.9653	32.5892
96b16556168a4f6e9a2e705659659f52	Ethiopia 	t	the Federal Democratic Republic of Ethiopia 	UN member 	ET	ETH	231	.et 	Addis Ababa	135472051	1000000	135	9.145000	40.489673	9.0250	38.7469
67668ab006e840909f675dd6ae1f1ccb	Honduras 	t	the Republic of Honduras 	UN member 	HN	HND	340	.hn 	Tegucigalpa	11005850	111890	98	15.199999	-86.241905	14.0818	-87.2068
25c0808085724c27bfb6f8d2b1fab226	Palestine, State of 	t	the State of Palestine 	UN observer 	PS	PSE	275	.ps 	Jerusalem	5589623	6020	929	31.952162	35.233154	31.7690	35.2163
caad0df950e248cfb04b5f49b583c099	Netherlands (Kingdom of the) 	t	the Kingdom of the Netherlands 	UN member 	NL	NLD	528	.nl 	Amsterdam	18346819	33720	544	52.132633	5.291266	52.3740	4.8897
7adc9186d1ad4344b076260b30c403cc	Slovakia 	t	the Slovak Republic 	UN member 	SK	SVK	703	.sk 	Bratislava	5474881	48088	114	48.669026	19.699024	48.1482	17.1067
b8cc9b4224dd47b2b76eca48d5aa9555	North Macedonia 	t	the Republic of North Macedonia 	UN member 	MK	MKD	807	.mk 	Skopje	1813791	25220	72	41.608635	21.745275	42.0000	21.4333
bee4b021dc334b159f33f0bb05d35cec	United Kingdom of Great Britain and Northern Ireland (the) 	t	the United Kingdom of Great Britain and Northern Ireland 	UN member 	GB	GBR	826	.gb.uk	London	69551332	241930	287	55.378051	-3.435973	51.5085	-0.1257
bc143fc3a3354462afd13bc336112d4f	Tanzania, the United Republic of 	t	the United Republic of Tanzania 	UN member 	TZ	TZA	834	.tz 	Dodoma	70545865	885800	80	-6.369028	34.888822	-6.1722	35.7395
\.


--
-- Data for Name: harddisk; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.harddisk (uuid, name, active, serial_nmuber, size, hardware_asset) FROM stdin;
7a192a6e3fbf40babd8190322c4a18c1	-- None --	f		0.00	96e441f8c78c49739e25ad10cf1f80ff
3b01888a44004776bc844f6a68828577	/dev/mmcblk0	t	0xb24c42c5	16.00	691c9f6b64ee45f69017f76bab5a8578
562b8fff75864ba2a30cfed79406c068	C:	t		0.02	3084c653048f4fa3be14b08999564f2b
b545b8ff399a4168802e52394688b5c4	C:	t		0.13	0ac354354a7d4b188220f3fa7e2ccd78
3756b76518674661bab09239a1e540a3	C:	t	ACE4_2E00_1A70_E505_2EE4_AC00_0	238.00	465da3ce847547dead403fa94b2caca0
c5d4dc08e90047eaa598b13de16f61f1	/dev/mmcblk0	t	0x1be5fa10	16.00	9b433770644c4f52bbecd4eb09dc5153
3973610d70aa412c833feb0d2bd1a838	/dev/nvme0n1	t	INTENSO_SSD_AA000000000001004_1	232.00	9b433770644c4f52bbecd4eb09dc5153
120e76d5f1d5401e91f1c7525358fc1d	/dev/sda	t	CT500MX500SSD1_1906E1E8E9F3	458.00	d9f66e4917144ef380ce9f357b3b7558
487b5b08f05340f8bece42f74d470f2a	/dev/mmcblk1	t	0xbfe4dc2b	16.00	d9f66e4917144ef380ce9f357b3b7558
b90ef492e56e481a8a424542f9ab91a7	unknown0	t		16.00	908295a7a92f48cb9c1489a56b6113aa
84cd13d97fab488c95644840284ae6f2	unknown1	t		4096.00	908295a7a92f48cb9c1489a56b6113aa
61364dd8b9534eefbfafcbfd3adc4989	/dev/sda	t	JMicron_0_DB0123457786-0:0	16384.00	691c9f6b64ee45f69017f76bab5a8578
7d8a696b23414456b51caa63931abf3f	/dev/sdb	t	JMicron_1_DB0123457786-0:1	16384.00	691c9f6b64ee45f69017f76bab5a8578
\.


--
-- Data for Name: hardware; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.hardware (uuid, name, active, cpu_type, company, product_lifecycle) FROM stdin;
e4033e0c002643c1addf746f67880c09	-- None --	f	e2354cad85f34870b57a90a1f572dd84	a65c511a51054dac91641b3944f7bb5b	0be2235637f14e4f8a8b506d6b5df007
9b3af2c29f104893a0b041f944fcdadd	386	t	0ba059d7369c4a8783a7f23e11139773	0692b72645ae49108b5f42b78a4fd3d3	7328ff123f6e402e8985bb596967828b
adfc6355866d4e378d262c44993414fa	486	t	0ba059d7369c4a8783a7f23e11139773	0692b72645ae49108b5f42b78a4fd3d3	7328ff123f6e402e8985bb596967828b
80aea40a14f746f28636f67f586acb3a	Cobalt RaQ 4	t	0ba059d7369c4a8783a7f23e11139773	5038c9c99f02493e8d60e98bbfe74050	7328ff123f6e402e8985bb596967828b
aa8da40d10e644c08961150c17a3af48	Dreamcast	t	a4c7242fdd4c4e2881c997cf17a763c4	fa79f848e1bf44ddbe17ee0aa455bafd	7328ff123f6e402e8985bb596967828b
fc3b7735d4e24a2fa9255d1b791e1726	HP 255 G8	t	abfdadab6dcf48288c0737bcce370f50	7761252f73af47769b0436060b0562c3	99c34331ea1944bb8ca5816d6962a862
2cf9217661964a5fab6efad972d588f2	Odroid C4	t	cfd2bcd4df4447c5a8db323f827ba215	17f96752206f412396b01598f02d4bff	99c34331ea1944bb8ca5816d6962a862
9d256126d24f402fafb82cf100aca80e	Odroid M1	t	cfd2bcd4df4447c5a8db323f827ba215	17f96752206f412396b01598f02d4bff	99c34331ea1944bb8ca5816d6962a862
747dc1b467054a0381861904629b5cac	Odroid N2+	t	cfd2bcd4df4447c5a8db323f827ba215	17f96752206f412396b01598f02d4bff	99c34331ea1944bb8ca5816d6962a862
adefeba1ec4d4ff5b41b1c6431b187b6	Odroid XU4 (active)	t	8b27b64193c14febb913ad8682557639	17f96752206f412396b01598f02d4bff	7328ff123f6e402e8985bb596967828b
f0741dd4c3b842bbb59e48059ef037d0	Odroid XU4 (passive)	t	8b27b64193c14febb913ad8682557639	17f96752206f412396b01598f02d4bff	7328ff123f6e402e8985bb596967828b
b4a52773f6a34544931b8cab19aef656	V100	t	806573b9e40b4966a37c15407dcd0302	5038c9c99f02493e8d60e98bbfe74050	7328ff123f6e402e8985bb596967828b
\.


--
-- Data for Name: hardware_asset; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.hardware_asset (uuid, name, active, software, company, hardware, hw_lifecycle, qrcode, ram, cpu_speed, order_date) FROM stdin;
96e441f8c78c49739e25ad10cf1f80ff	-- None --	f	f57d575fe9f64446b80cdecf296442e4	a65c511a51054dac91641b3944f7bb5b	e4033e0c002643c1addf746f67880c09	15054e5d5bdc4ed7b1d252618e9414a2	\N	0.000	0.000	1970-01-01
465da3ce847547dead403fa94b2caca0	LAPTOP-A5T8OI4I	t	bd30c0075ac74e50b6c0f8473dd82352	7761252f73af47769b0436060b0562c3	fc3b7735d4e24a2fa9255d1b791e1726	0f040eee0f0d4c9faa6abd0ff9ae956f	\N	8.000	2.100	1970-01-01
d9f66e4917144ef380ce9f357b3b7558	mf01	t	5086271047454a4faeacbfc1da8f38cc	979b23aaa89a40db958dd0ee37f44107	747dc1b467054a0381861904629b5cac	0f040eee0f0d4c9faa6abd0ff9ae956f	\N	4.000	1.910	1970-01-01
691c9f6b64ee45f69017f76bab5a8578	nas01	t	d2947f3a0fad4c53bd5c4bbc07fd10af	979b23aaa89a40db958dd0ee37f44107	adefeba1ec4d4ff5b41b1c6431b187b6	0f040eee0f0d4c9faa6abd0ff9ae956f	\N	2.000	2.000	1970-01-01
908295a7a92f48cb9c1489a56b6113aa	mc02	t	b298776a954d40f0949d18276ed543bd	979b23aaa89a40db958dd0ee37f44107	2cf9217661964a5fab6efad972d588f2	0f040eee0f0d4c9faa6abd0ff9ae956f	\N	4.000	2.000	1970-01-01
6801c63c5310486fa256087d53069d88	mf02	t	f57d575fe9f64446b80cdecf296442e4	979b23aaa89a40db958dd0ee37f44107	747dc1b467054a0381861904629b5cac	6386ab37d91b4d45963d646431d0b6eb	\N	4.000	1.910	2025-08-17
0ac354354a7d4b188220f3fa7e2ccd78	386	t	21146648320d49d7b008980ce03baff3	0692b72645ae49108b5f42b78a4fd3d3	9b3af2c29f104893a0b041f944fcdadd	c359893877f34d82b7f64ef151a7026b	\N	0.005	0.016	1995-07-01
3084c653048f4fa3be14b08999564f2b	486	t	40442e085cf143ffbb0669210bea1fa6	0692b72645ae49108b5f42b78a4fd3d3	adfc6355866d4e378d262c44993414fa	c359893877f34d82b7f64ef151a7026b	\N	0.128	0.100	1997-01-01
d6da568c1c2b4fa59f0bf3198b8fd43a	sun01	t	4510ebf9933d4fa3908c812bcfb68c80	6352de0f8761490981e72967e3ff1430	b4a52773f6a34544931b8cab19aef656	227eb27d167241c4bd643416abfd4ab4	\N	2.000	0.650	2010-03-01
cbd2db34fed44c82a53336291a5a0e50	web01	t	49afea1c3a3748e6b90dcb00d3e8e78d	6352de0f8761490981e72967e3ff1430	80aea40a14f746f28636f67f586acb3a	227eb27d167241c4bd643416abfd4ab4	\N	0.512	0.450	2010-03-01
9b433770644c4f52bbecd4eb09dc5153	py02	t	b608e43fb43149a295a917a80866b284	979b23aaa89a40db958dd0ee37f44107	9d256126d24f402fafb82cf100aca80e	0f040eee0f0d4c9faa6abd0ff9ae956f	\N	8.000	1.990	2022-12-01
4f6f8e5a04ba4c66a46fe810dc1e8913	dc01	t	ddb42da316ac461fb0b964eb1a3fc083	a65c511a51054dac91641b3944f7bb5b	aa8da40d10e644c08961150c17a3af48	0f040eee0f0d4c9faa6abd0ff9ae956f	\N	0.016	0.200	1970-01-01
\.


--
-- Data for Name: knowledge; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.knowledge (uuid, name, active, article, approved) FROM stdin;
10f2cfaab5cb4967adb602b9c0f8e53e	-- None --	t	Please enter some knowledge...	f
95d0d19f69d049d0bda815c29fee92ac	IT Procurement	t	<b>Procurement</b> is the process of locating and agreeing to terms and purchasing goods, services, or other works from an external source, often with the use of a tendering or competitive bidding process.<br>\r\n<br>\r\nSource: https://en.wikipedia.org/wiki/Procurement	f
f14b1cfd50b1412cb7c680ef907a4130	IMAC	t	<ul>\r\n<li><b>I</b>nstall</li>\r\n<li><b>M</b>ove</li>\r\n<li><b>A</b>dd</li>\r\n<li><b>C</b>hange</li>\r\n</ul>	f
b13e0e9513ad4ef6bddf4461a51d1e7b	DINROS	t	<ul>\r\n<li><b>D</b>iscover</li>\r\n<li><b>I</b>nventory</li>\r\n<li><b>N</b>ormalize</li>\r\n<li><b>R</b>econcile</li>\r\n<li><b>O</b>ptimize</li>\r\n<li><b>S</b>hare</li>\r\n</ul>	f
7290d1ee24404e68b41a9a544c7b0cb3	ITAD	t	IT Asset Disposition (ITAD) is the process of securely and responsibly <b>handling IT equipment that has reached the end of its lifecycle</b>.<br>\r\n<br>\r\nSource: https://invgate.com/itsm/it-asset-management/it-asset-disposition	f
d60d718d1c05459a990e5732db559ada	Knowledge Management	t	<b>Knowledge management (KM)</b> is the set of procedures for producing, disseminating, utilizing, and overseeing an organization's knowledge and data.<br>\r\n<br>\r\nSource: <a href="https://en.wikipedia.org/wiki/Knowledge_management">https://en.wikipedia.org/wiki/Knowledge_management</a>	t
\.


--
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.location (uuid, name, active, country, street, zip_code, city, asdf) FROM stdin;
c4e3c2f17cf545f0af16962ed0c0dedc	-- None --	t	e1e5d806b1e9433ab69b1d6e79f95370		\N		qwer
5fd579e56c5a4757a0ab2dcba71e4208	Telia Company	t	9dfdf5b63db54c98a623b65bc098cbb8	Pärnu mnt. 158	11317	Tallinn	qwer
0dc6cdf8f85d44b68d9dd6a1addfc364	Telia Company	t	f6c6be91e01b4ca496e0289841792d96	Östre Akers vej 18A	581	Oslo	qwer
a64e68fe47fd4e6a85d5c426c2ad3edd	Netic DC5	t	bfa589c6e5ce4295a0db635fa35942be	Port of Aalborg, Ankeret	9220	Aalborg	qwer
\.


--
-- Data for Name: network_interfaces; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.network_interfaces (uuid, name, active, mac_address, ip_address, netmask, ip_type, hardware_asset, connector) FROM stdin;
b496bfc7eba341139d69d1a77950d2f8	-- None --	f	00:00:00:00:00:00	0.0.0.0	255.255.255.0	a886340306b543a883df8f9a3bdf9100	96e441f8c78c49739e25ad10cf1f80ff	2d42948af8064b1d884d149024d1f591
3b2a5e329c024e119ebc4ca84383453a	bridge0	t	9e:70:6e:a3:85:e9	192.168.2.1	255.255.255.0	cbda7508f1d94cd0925ba72cb28da6ea	d9f66e4917144ef380ce9f357b3b7558	2d42948af8064b1d884d149024d1f591
8db5def85da846ce9b0aab04c8583888	0	t	00:1e:06:36:8b:17	192.168.2.3	255.255.255.0	cbda7508f1d94cd0925ba72cb28da6ea	691c9f6b64ee45f69017f76bab5a8578	2d42948af8064b1d884d149024d1f591
c4759ceb17214894bddd8c90312a6228	br0	t	de:a7:a7:29:5b:b9	192.168.3.11	255.255.255.0	cbda7508f1d94cd0925ba72cb28da6ea	9b433770644c4f52bbecd4eb09dc5153	2d42948af8064b1d884d149024d1f591
738e477ee3704bf383dff5e2850fa55c	end0	t	00:1e:06:42:53:5d	192.168.1.3	255.255.255.0	cbda7508f1d94cd0925ba72cb28da6ea	d9f66e4917144ef380ce9f357b3b7558	addcb50381a84859ba4acc90c95fa1b0
2320ceab625d4f77962396b359c2bccb	enx001e06368b17	t	00:1e:06:36:8b:17	0.0.0.0	255.255.255.0	06dd2581e04f497a8fed02f791eede70	691c9f6b64ee45f69017f76bab5a8578	7ca4127158534d97a0ba4e930cd4367c
dd79ddef31bc486abb229ee80c7124c6	enx00e04c6802b8	t	00:e0:4c:68:02:b8	0.0.0.0	255.255.255.0	06dd2581e04f497a8fed02f791eede70	691c9f6b64ee45f69017f76bab5a8578	addcb50381a84859ba4acc90c95fa1b0
4aa405c5dc284b078549f99fb74bb27d	enx7cc2c60fdd25	t	7c:c2:c6:0f:dd:25	0.0.0.0	255.255.255.0	06dd2581e04f497a8fed02f791eede70	d9f66e4917144ef380ce9f357b3b7558	7ca4127158534d97a0ba4e930cd4367c
e2620aade4d84cbbb81bad8193ab94e8	enx7cc2c61a4e84	t	c:c2:c6:1a:4e:84	0.0.0.0	255.255.255.0	06dd2581e04f497a8fed02f791eede70	d9f66e4917144ef380ce9f357b3b7558	7ca4127158534d97a0ba4e930cd4367c
7aaaba57aafd465390a4c60045f126da	eth0	t	00:1e:06:48:05:c6	192.168.3.202	255.255.255.0	3f6eea09accb4406bb88d98d11010217	908295a7a92f48cb9c1489a56b6113aa	addcb50381a84859ba4acc90c95fa1b0
f1510de85fd846d9a6a77bbb36ca3bca	eth0	t	7e:10:d2:4e:c5:e3	0.0.0.0	255.255.255.0	06dd2581e04f497a8fed02f791eede70	9b433770644c4f52bbecd4eb09dc5153	addcb50381a84859ba4acc90c95fa1b0
470a09dc970449e6be4e6b1cb84d7891	Realtek RTL8852AE WiFi 6 802.11ax PCIe Adapter	t	F8:89:D2:70:33:81	192.168.2.200	255.255.255.0	3f6eea09accb4406bb88d98d11010217	465da3ce847547dead403fa94b2caca0	addcb50381a84859ba4acc90c95fa1b0
9a56425335b0496abb085d9247933f1f	Realtek PCIe GbE Family Controller	t	E0:70:EA:58:C2:08	0.0.0.0	255.255.255.0	3f6eea09accb4406bb88d98d11010217	465da3ce847547dead403fa94b2caca0	addcb50381a84859ba4acc90c95fa1b0
f78ce594928840d38922ac4a34edfd2b	ppp0	t	00:00:00:00:00:00	172.16.12.1	255.255.255.252	cbda7508f1d94cd0925ba72cb28da6ea	4f6f8e5a04ba4c66a46fe810dc1e8913	addcb50381a84859ba4acc90c95fa1b0
2c17866103664f899ae24ec0434ae303	wlx98ba5fdd3920	t	98:ba:5f:dd:39:20	0.0.0.0	255.255.255.0	06dd2581e04f497a8fed02f791eede70	d9f66e4917144ef380ce9f357b3b7558	7ca4127158534d97a0ba4e930cd4367c
9566a19d53114f68829c154d5a91d744	wlxd03745904518	t	d0:37:45:90:45:18	192.168.2.11	255.255.255.0	cbda7508f1d94cd0925ba72cb28da6ea	9b433770644c4f52bbecd4eb09dc5153	7ca4127158534d97a0ba4e930cd4367c
25898704aa694bef8d4eafaf022f80bf	ppp2	t	00:00:00:00:00:00	172.16.12.6	255.255.255.252	cbda7508f1d94cd0925ba72cb28da6ea	9b433770644c4f52bbecd4eb09dc5153	7ca4127158534d97a0ba4e930cd4367c
eecd78c847c44644b9b5db0e8d4dbe9a	ppp1	t	00:00:00:00:00:00	172.16.12.4	255.255.255.252	cbda7508f1d94cd0925ba72cb28da6ea	9b433770644c4f52bbecd4eb09dc5153	7ca4127158534d97a0ba4e930cd4367c
73b5821e4f99497a9e0fdb5502b30b38	ppp0	t	00:00:00:00:00:00	172.16.12.2	255.255.255.252	cbda7508f1d94cd0925ba72cb28da6ea	9b433770644c4f52bbecd4eb09dc5153	7ca4127158534d97a0ba4e930cd4367c
\.


--
-- Data for Name: processes; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.processes (uuid, name, active, supplier, input, output, customer, knowledge) FROM stdin;
14f132584c6f4a91a08113a3af7ab6b0	-- None --	f					10f2cfaab5cb4967adb602b9c0f8e53e
bb7fc1c0fbf549f99db1696cc408ed61	IMAC	t	Internal	Hardware Asset	Hardware Asset	Internal	f14b1cfd50b1412cb7c680ef907a4130
b761017c828945a489e3e66767ba3183	ITAD	t	Internal	Hardware Asset	Hardware	External	7290d1ee24404e68b41a9a544c7b0cb3
edc06026aa604401862fae2250d9cd1e	IT Procurement	t	External	Hardware	Hardware Asset	Internal	95d0d19f69d049d0bda815c29fee92ac
628ccb21aaf745a989cbaa716bc89d86	Knowledge Management	t	Internal	Knowledge	Article	Internal	d60d718d1c05459a990e5732db559ada
564f44e42d544ee4884221a73b371952	RMA	t	Internal	Hardware Asset	Hardware Asset	Internal	d60d718d1c05459a990e5732db559ada
\.


--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.service (uuid, name, active) FROM stdin;
0e3a8e8712884eb283a2d8a34b5ac1a1	-- None --	t
d9d1b15c85864ac4af53217216a560c9	CMDB	t
8f98612763bd4fd58666a492598cf6ff	Wiki	t
\.


--
-- Data for Name: service_asset; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.service_asset (uuid, name, active, environment, service) FROM stdin;
bfa1fd92520a4fcebf35ab852d4b99d0	CMDB	t	f9e24cc3d5f54d2aa7635140a8f40d60	d9d1b15c85864ac4af53217216a560c9
6f2475c45a89466f8afb34c95183adc4	CMDB	t	34b5869c3107434ba02ca5271722f4fb	d9d1b15c85864ac4af53217216a560c9
20f1468f7f404509bc69af852bcee3a9	Wiki	t	f9e24cc3d5f54d2aa7635140a8f40d60	8f98612763bd4fd58666a492598cf6ff
390b06f9974448448eb72c9dc8405220	-- None --	f	138930daac194a3094077481a60f59e1	0e3a8e8712884eb283a2d8a34b5ac1a1
\.


--
-- Data for Name: software; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.software (uuid, name, active, version, sw_lifecycle, software_type) FROM stdin;
f57d575fe9f64446b80cdecf296442e4	-- None --	f		2db9e4c07c3242f58a7b842a7191ecba	a8af2f0e3a054940b7abb06a72247767
21146648320d49d7b008980ce03baff3	FreeDOS	t	1.1	037a2e983c024ce090f673a0590b943c	205399429d1f43edb37a761cb4102317
40442e085cf143ffbb0669210bea1fa6	FreeDOS	t	1.4	84fbc39baefa4df2b1e0debc1426e8df	205399429d1f43edb37a761cb4102317
4510ebf9933d4fa3908c812bcfb68c80	Solaris	t	10	037a2e983c024ce090f673a0590b943c	205399429d1f43edb37a761cb4102317
49afea1c3a3748e6b90dcb00d3e8e78d	Slackware	t	12.0	037a2e983c024ce090f673a0590b943c	205399429d1f43edb37a761cb4102317
b298776a954d40f0949d18276ed543bd	CoreELEC	t	20.5-Nexus	84fbc39baefa4df2b1e0debc1426e8df	205399429d1f43edb37a761cb4102317
bd30c0075ac74e50b6c0f8473dd82352	Windows	t	10	84fbc39baefa4df2b1e0debc1426e8df	205399429d1f43edb37a761cb4102317
5086271047454a4faeacbfc1da8f38cc	Armbian	t	trixie/sid	84fbc39baefa4df2b1e0debc1426e8df	205399429d1f43edb37a761cb4102317
b608e43fb43149a295a917a80866b284	Armbian	t	bookworm/sid	84fbc39baefa4df2b1e0debc1426e8df	205399429d1f43edb37a761cb4102317
d2947f3a0fad4c53bd5c4bbc07fd10af	Armbian	t	9.13	037a2e983c024ce090f673a0590b943c	205399429d1f43edb37a761cb4102317
ddb42da316ac461fb0b964eb1a3fc083	MPR-21871	t	v1.01c	037a2e983c024ce090f673a0590b943c	205399429d1f43edb37a761cb4102317
3cd23421d61c426798b8f74347602c85	postgresql	t	14.15	84fbc39baefa4df2b1e0debc1426e8df	6e7ed0a3a1ba462ca5f0b0b15b4a8bae
\.


--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: cmdb
--

COPY public.test (uuid, name, active, count, "float", bool, "varchar", order_date, description, test_lc, processes) FROM stdin;
6b6ce29be1d349ddabf6f6aacfafeb2e	-- None --	f	0	0.00	t	default	2025-08-30	Please enter some text...	b83656c33ea44205bc6d94a66e034f25	14f132584c6f4a91a08113a3af7ab6b0
e82f6edb6ed84dd78b9fc6236e5b2c95	Keyboard	t	100	160.22	t	default	2025-08-30	Please enter some text...	3f9d607dab794340b1477cae4d111384	628ccb21aaf745a989cbaa716bc89d86
13c32feaa8c6434794d4df6f10fef2df	Mouse	t	50	123.46	t	mouse	2024-08-30	Please enter some text...	3f9d607dab794340b1477cae4d111384	628ccb21aaf745a989cbaa716bc89d86
\.


--
-- PostgreSQL database dump complete
--

