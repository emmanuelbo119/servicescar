CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--Talleres mecanicos

CREATE TABLE IF NOT EXISTS public.taller_mecanicos (
	"uuidTallermecanico" uuid DEFAULT uuid_generate_v4() NOT NULL,
	nombre varchar(255) NOT NULL,
	direccion varchar(255) NOT NULL,
	latitud float8 NOT NULL,
	longitud float8 NOT NULL,
	"horarioAtencion" varchar(255) NOT NULL,
	servicios text NULL,
	"fechaCreacion" timestamp NULL,
	"fechaModificacion" timestamp NULL,
	CONSTRAINT taller_mecanicos_pkey PRIMARY KEY ("uuidTallermecanico")
);



INSERT INTO public.taller_mecanicos ("uuidTallermecanico",nombre,direccion,latitud,longitud,"horarioAtencion",servicios,"fechaCreacion","fechaModificacion") VALUES
	 ('299ac113-f80d-449e-ba62-5741edb51056','Taller Mecánico Los Andes','Av. Corrientes 1234, Buenos Aires',-34.603722,-58.381592,'Lunes a Viernes de 8:00 a 18:00','Cambio de aceite, Alineación y balanceo, Reparación de motores','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('89b890ef-681b-40b4-a28f-c2a2750a9ebb','Taller Automotriz El Sol','Calle Falsa 123, Córdoba',-31.420083,-64.188776,'Lunes a Viernes de 9:00 a 19:00','Cambio de neumáticos, Frenos, Electricidad del automóvil','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('fa3b9ec3-c498-4f87-a56b-8107d3334737','Taller Integral Patagonia','Ruta 40 Km 1234, San Carlos de Bariloche',-41.133472,-71.310278,'Lunes a Sábado de 8:00 a 17:00','Mecánica general, Suspensión, Diagnóstico computarizado','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('b31a6f19-9c0a-4924-a434-7574ee79d49e','Mecánica Rápida','Av. San Martín 567, Mendoza',-32.890842,-68.827171,'Lunes a Viernes de 8:00 a 18:00','Cambio de aceite, Reparación de frenos, Alineación y balanceo','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('6f2686fe-46f5-4168-811e-9ff1f52c0172','Taller Mecánico Norte','Av. Sarmiento 789, Salta',-24.782932,-65.423198,'Lunes a Viernes de 8:30 a 18:30','Cambio de batería, Reparación de embrague, Mecánica ligera','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('1e79646d-158b-4c7d-97a1-58387f5c044f','Servicio Automotor Pampa','Calle Principal 234, Santa Rosa',-36.620001,-64.290001,'Lunes a Viernes de 9:00 a 18:00','Cambio de aceite, Reparación de transmisión, Diagnóstico computarizado','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('0bdaaef0-401d-4068-8513-213b30fa0560','Taller del Este','Av. Libertador 456, San Juan',-31.5375,-68.536389,'Lunes a Viernes de 8:00 a 17:00','Alineación y balanceo, Cambio de bujías, Reparación de motores','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('9761149f-3d72-4ee6-abc5-dc944802e0e0','Taller Mecánico Costero','Calle 50 678, Mar del Plata',-38.005477,-57.54261,'Lunes a Viernes de 9:00 a 19:00','Cambio de aceite, Alineación y balanceo, Reparación de frenos','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('a726b659-ecb5-4200-9319-68f43f861ff2','Automotriz Andina','Av. Colón 890, La Rioja',-29.4135,-66.8557,'Lunes a Viernes de 8:00 a 18:00','Cambio de neumáticos, Reparación de frenos, Electricidad del automóvil','2024-05-26 00:00:00','2024-05-26 00:00:00'),
	 ('5927c22d-92a3-4ea9-8b63-928474208499','Taller Centro','Calle 10 234, Tucumán',-26.822,-65.207,'Lunes a Viernes de 8:00 a 18:00','Mecánica general, Diagnóstico computarizado, Cambio de aceite','2024-05-26 00:00:00','2024-05-26 00:00:00');


--Modelos vehiculos

CREATE TABLE IF NOT EXISTS public.modelo_vehiculos (
	uuidmodelovehiculo uuid DEFAULT gen_random_uuid() NOT NULL,
	nombre varchar(255) NOT NULL,
	descripcion text NULL,
	"fechaCreacion" timestamp NOT NULL,
	"fechaModificacion" timestamp NULL,
	marca_id uuid NULL,
	CONSTRAINT modelo_vehiculos_pkey PRIMARY KEY (uuidmodelovehiculo)
);


-- public.modelo_vehiculos foreign keys

ALTER TABLE public.modelo_vehiculos ADD CONSTRAINT modelo_vehiculos_marca_vehiculos_fk FOREIGN KEY (marca_id) REFERENCES public.marca_vehiculos(uuidmarcavehiculo);

INSERT INTO public.modelo_vehiculos (uuidmodelovehiculo,nombre,descripcion,"fechaCreacion","fechaModificacion",marca_id) VALUES
	 ('070924a1-0bc4-4301-87b7-28a948783c4d','Aveo',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','c14d5506-f559-4183-b1ac-866bd22a35e4'),
	 ('6761e03f-eee0-466c-bba9-ef5714418743','Spark',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','c14d5506-f559-4183-b1ac-866bd22a35e4'),
	 ('20273ff3-4e12-42bc-abeb-4559cc91fcad','Malibu',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','c14d5506-f559-4183-b1ac-866bd22a35e4'),
	 ('52c369f8-cf26-4d04-927e-f8e9a99d166a','Cruze',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','c14d5506-f559-4183-b1ac-866bd22a35e4'),
	 ('473213d9-332c-468f-86ef-aea3b7db56be','Trax',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','c14d5506-f559-4183-b1ac-866bd22a35e4'),
	 ('8952240c-604c-4043-afa2-c986fa433139','Equinox',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','c14d5506-f559-4183-b1ac-866bd22a35e4'),
	 ('fbdaadbe-875e-4e03-aeac-db29cc7deb83','Silverado',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','c14d5506-f559-4183-b1ac-866bd22a35e4'),
	 ('8839b756-91be-45d6-97c0-4354f4c1c611','Corolla',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','563f3d67-2f97-40f3-807e-8b86de8e3efe'),
	 ('8f876bbb-01bd-4861-be72-564dce19c202','Camry',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','563f3d67-2f97-40f3-807e-8b86de8e3efe'),
	 ('80a60faa-9cc7-49c0-b94a-d8e5e133ea27','Prius',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','563f3d67-2f97-40f3-807e-8b86de8e3efe');
INSERT INTO public.modelo_vehiculos (uuidmodelovehiculo,nombre,descripcion,"fechaCreacion","fechaModificacion",marca_id) VALUES
	 ('7594fed1-1ed1-495b-a3de-ab8bca905bdd','Hilux',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','563f3d67-2f97-40f3-807e-8b86de8e3efe'),
	 ('10bdf786-66b1-48e1-9c6a-762d37bdcfac','RAV4',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','563f3d67-2f97-40f3-807e-8b86de8e3efe'),
	 ('26f7d684-c403-4165-83e1-81b6721a932e','Land Cruiser',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','563f3d67-2f97-40f3-807e-8b86de8e3efe'),
	 ('2e262b61-586e-4762-af9c-cc4522491ef5','Yaris',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','563f3d67-2f97-40f3-807e-8b86de8e3efe'),
	 ('3be4efa5-2c0f-4622-a1dc-357397b910af','Golf',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3bdf2d0e-c5b5-428b-98c6-6e64cc872c09'),
	 ('835b6190-ef01-414d-aa1e-f8080ee83d22','Polo',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3bdf2d0e-c5b5-428b-98c6-6e64cc872c09'),
	 ('1abcedf3-405e-43b3-88d3-fce30c4ea514','Passat',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3bdf2d0e-c5b5-428b-98c6-6e64cc872c09'),
	 ('48e3e6e9-5125-440b-8008-8f08f3109373','Tiguan',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3bdf2d0e-c5b5-428b-98c6-6e64cc872c09'),
	 ('1235886b-e901-42cb-b3dd-0c17163d987e','Jetta',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3bdf2d0e-c5b5-428b-98c6-6e64cc872c09'),
	 ('67ec087c-635e-449f-9d6e-7d281c4c1bb4','Beetle',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3bdf2d0e-c5b5-428b-98c6-6e64cc872c09');
INSERT INTO public.modelo_vehiculos (uuidmodelovehiculo,nombre,descripcion,"fechaCreacion","fechaModificacion",marca_id) VALUES
	 ('b3fd984c-4ceb-4f55-a8db-77341d9f979c','Touareg',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3bdf2d0e-c5b5-428b-98c6-6e64cc872c09'),
	 ('0d7fb9d6-0f85-42c2-b6ae-f504b417c372','Clio',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','b41c181b-81ac-4aaf-b425-9190867294df'),
	 ('3d6e66fb-fce8-4106-9a46-5116b7e177ef','Megane',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','b41c181b-81ac-4aaf-b425-9190867294df'),
	 ('b13b6cb5-69fd-4c3e-8be4-2bf5ddb646a6','Captur',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','b41c181b-81ac-4aaf-b425-9190867294df'),
	 ('56524cbd-5716-48ba-a94d-c581f22b195c','Koleos',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','b41c181b-81ac-4aaf-b425-9190867294df'),
	 ('3b221457-a88e-4d56-80e8-8221d55abfc3','Duster',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','b41c181b-81ac-4aaf-b425-9190867294df'),
	 ('ccff2136-28af-464c-bf49-bdbb1b495dc6','Sandero',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','b41c181b-81ac-4aaf-b425-9190867294df'),
	 ('b74a7081-04db-49bb-8632-c876483b37b9','Twingo',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','b41c181b-81ac-4aaf-b425-9190867294df'),
	 ('faeb9d75-fc32-4074-88bc-6f1afd8e2dde','208',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','bdf03fc7-90c8-4d8c-91c0-0d126575d4d9'),
	 ('2e9f51e3-9f1b-4377-9e31-fbc2c5d5d2ee','308',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','bdf03fc7-90c8-4d8c-91c0-0d126575d4d9');
INSERT INTO public.modelo_vehiculos (uuidmodelovehiculo,nombre,descripcion,"fechaCreacion","fechaModificacion",marca_id) VALUES
	 ('6ba49ad6-2979-43f3-9b0f-2509010e0f21','3008',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','bdf03fc7-90c8-4d8c-91c0-0d126575d4d9'),
	 ('98da3fa5-1a9c-4d0e-9488-db8a786aa817','5008',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','bdf03fc7-90c8-4d8c-91c0-0d126575d4d9'),
	 ('0f63bf21-0218-41af-8b46-2f9c66e9210f','2008',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','bdf03fc7-90c8-4d8c-91c0-0d126575d4d9'),
	 ('c0fe247c-0551-4e51-8902-39a9202ae35f','508',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','bdf03fc7-90c8-4d8c-91c0-0d126575d4d9'),
	 ('d74246fa-3be9-4938-9d0e-11d6fbb731e5','Partner',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','bdf03fc7-90c8-4d8c-91c0-0d126575d4d9'),
	 ('20de3dfd-85f0-481e-b848-d9ed4628574b','500',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','2171bf92-ddc4-4352-accc-a06c64c809c0'),
	 ('36d86109-22a0-4221-8971-3bd6d9517657','Panda',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','2171bf92-ddc4-4352-accc-a06c64c809c0'),
	 ('25e0d146-605a-461e-8b31-f64a5b0a7bab','Tipo',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','2171bf92-ddc4-4352-accc-a06c64c809c0'),
	 ('8d0b3e06-8231-4a56-92d5-d67936dfb162','Punto',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','2171bf92-ddc4-4352-accc-a06c64c809c0'),
	 ('69a1fd0f-8a5d-455a-93fc-1a572f45960c','Doblo',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','2171bf92-ddc4-4352-accc-a06c64c809c0');
INSERT INTO public.modelo_vehiculos (uuidmodelovehiculo,nombre,descripcion,"fechaCreacion","fechaModificacion",marca_id) VALUES
	 ('a22688dc-131b-440b-868a-8c89f1410cd8','124 Spider',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','2171bf92-ddc4-4352-accc-a06c64c809c0'),
	 ('db81e1ad-1f62-419c-b3db-20803d7a5b23','Argo',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','2171bf92-ddc4-4352-accc-a06c64c809c0'),
	 ('ded52a68-33e4-488c-967f-1109f4d842fd','C3',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','a64e75e8-4a72-4c92-96c3-e520aa400653'),
	 ('d78a0c40-bc1f-4c33-847f-55a7847f24c8','C4',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','a64e75e8-4a72-4c92-96c3-e520aa400653'),
	 ('44770e16-9f44-4c2c-8523-bc773fd013d4','C5 Aircross',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','a64e75e8-4a72-4c92-96c3-e520aa400653'),
	 ('8926cc81-8d49-472c-a0da-7de1db71bb81','Berlingo',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','a64e75e8-4a72-4c92-96c3-e520aa400653'),
	 ('c768e7c7-8e9e-4f24-9b48-dd369c7392bb','C1',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','a64e75e8-4a72-4c92-96c3-e520aa400653'),
	 ('4e8796fa-1a5f-4eff-917c-fd8fd8615cf8','C-Elysée',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','a64e75e8-4a72-4c92-96c3-e520aa400653'),
	 ('03c57cad-6171-4d41-a8c6-884e14b50234','Jumper',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','a64e75e8-4a72-4c92-96c3-e520aa400653'),
	 ('98f88f4a-43f0-4562-bb96-529ab8870aba','Micra',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3e807e0c-5a39-47f6-9d03-347f1b7bdbb9');
INSERT INTO public.modelo_vehiculos (uuidmodelovehiculo,nombre,descripcion,"fechaCreacion","fechaModificacion",marca_id) VALUES
	 ('cb3cd68e-3847-4ef0-9a66-27404f21f9a0','Altima',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3e807e0c-5a39-47f6-9d03-347f1b7bdbb9'),
	 ('9fddce25-6449-409f-a5f7-42da56cb5fcc','Maxima',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3e807e0c-5a39-47f6-9d03-347f1b7bdbb9'),
	 ('78b3916f-00e0-460e-891f-4b1baacfeac5','Qashqai',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3e807e0c-5a39-47f6-9d03-347f1b7bdbb9'),
	 ('5cee9e20-4eb4-43f5-a1da-3e574efd8609','X-Trail',NULL,'2024-05-26 00:00:00','2024-05-26 00:00:00','3e807e0c-5a39-47f6-9d03-347f1b7bdbb9');




--Marcas vehiculos

CREATE TABLE IF NOT EXISTS public.marca_vehiculos (
	uuidmarcavehiculo uuid DEFAULT uuid_generate_v4() NOT NULL,
	nombre varchar(255) NOT NULL,
	descripcion text NULL,
	fechacreacion timestamp NOT NULL,
	fechamodificacion timestamp NULL,
	CONSTRAINT marca_vehiculos_pkey PRIMARY KEY (uuidmarcavehiculo)
);


INSERT INTO public.marca_vehiculos (uuidmarcavehiculo,nombre,descripcion,fechacreacion,fechamodificacion) VALUES
	 ('7984f267-7c07-456d-a09d-ff0b9d86ce21','Ford','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('c14d5506-f559-4183-b1ac-866bd22a35e4','Chevrolet','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('563f3d67-2f97-40f3-807e-8b86de8e3efe','Toyota','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('3bdf2d0e-c5b5-428b-98c6-6e64cc872c09','Volkswagen','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('b41c181b-81ac-4aaf-b425-9190867294df','Renault','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('bdf03fc7-90c8-4d8c-91c0-0d126575d4d9','Peugeot','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('2171bf92-ddc4-4352-accc-a06c64c809c0','Fiat','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('a64e75e8-4a72-4c92-96c3-e520aa400653','Citroën','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('3e807e0c-5a39-47f6-9d03-347f1b7bdbb9','Nissan','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('69ec8d22-72ab-4b8c-bb0d-7905a1995d73','Honda','','2024-05-23 00:00:00','2024-05-23 00:00:00');
INSERT INTO public.marca_vehiculos (uuidmarcavehiculo,nombre,descripcion,fechacreacion,fechamodificacion) VALUES
	 ('8b6ac0ba-0d63-455d-987e-e69ac5da065d','Hyundai','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('3715d7d3-2267-4e8b-a908-b1c8196d02b4','Kia','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('4a5d7ca9-ef3c-4a89-92f3-82f1b15e3a1d','Jeep','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('c4bd9b3c-5b64-413a-a584-a44a544577f1','Subaru','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('d9ca3966-c27b-4953-928c-4903f012c9d8','BMW','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('7a8e7a30-4dc5-4439-a847-1af0f033c939','Mercedes-Benz','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('85c2adb4-3e3f-463e-91b4-9ba03400e767','Audi','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('d8921b46-6e04-4293-ac98-b7edcb5e66f2','Mitsubishi','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('29c6b7a2-699e-4aca-a8a6-42de6c309a1c','Suzuki','','2024-05-23 00:00:00','2024-05-23 00:00:00'),
	 ('7fa3131a-6936-43b0-a6d6-023d331557c2','Chery','','2024-05-23 00:00:00','2024-05-23 00:00:00');
INSERT INTO public.marca_vehiculos (uuidmarcavehiculo,nombre,descripcion,fechacreacion,fechamodificacion) VALUES
	 ('e4eda5fd-a7ed-468b-aa8b-bdceeff3b7fb','Toyota',NULL,'2024-05-24 03:03:34.10853','2024-05-24 03:03:34.108532'),
	 ('d882afc3-caf2-4c1b-8bab-83d68fd0cc90','Renault',NULL,'2024-05-24 03:04:38.017642','2024-05-24 03:04:38.017644');



