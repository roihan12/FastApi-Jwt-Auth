PGDMP     
                    |            quantus    15.4    15.4                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    73252    quantus    DATABASE     ~   CREATE DATABASE quantus WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Indonesia.1252';
    DROP DATABASE quantus;
                postgres    false            �            1259    73379    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    73384    blacklisttokens    TABLE     �   CREATE TABLE public.blacklisttokens (
    id uuid NOT NULL,
    expire timestamp without time zone NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP) NOT NULL
);
 #   DROP TABLE public.blacklisttokens;
       public         heap    postgres    false            �            1259    73402    tasks    TABLE     �   CREATE TABLE public.tasks (
    id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP) NOT NULL,
    title character varying NOT NULL,
    description text NOT NULL,
    author_id uuid NOT NULL
);
    DROP TABLE public.tasks;
       public         heap    postgres    false            �            1259    73391    users    TABLE     y  CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying NOT NULL,
    full_name character varying NOT NULL,
    password character varying NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, CURRENT_TIMESTAMP) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false                      0    73379    alembic_version 
   TABLE DATA                 public          postgres    false    214                    0    73384    blacklisttokens 
   TABLE DATA                 public          postgres    false    215   ^                 0    73402    tasks 
   TABLE DATA                 public          postgres    false    217   x                 0    73391    users 
   TABLE DATA                 public          postgres    false    216   �       u           2606    73383 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    214            w           2606    73389 $   blacklisttokens blacklisttokens_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.blacklisttokens
    ADD CONSTRAINT blacklisttokens_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.blacklisttokens DROP CONSTRAINT blacklisttokens_pkey;
       public            postgres    false    215                       2606    73409    tasks tasks_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.tasks DROP CONSTRAINT tasks_pkey;
       public            postgres    false    217            |           2606    73399    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    216            x           1259    73390    ix_blacklisttokens_id    INDEX     O   CREATE INDEX ix_blacklisttokens_id ON public.blacklisttokens USING btree (id);
 )   DROP INDEX public.ix_blacklisttokens_id;
       public            postgres    false    215            }           1259    73415    ix_tasks_id    INDEX     ;   CREATE INDEX ix_tasks_id ON public.tasks USING btree (id);
    DROP INDEX public.ix_tasks_id;
       public            postgres    false    217            y           1259    73400    ix_users_email    INDEX     H   CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);
 "   DROP INDEX public.ix_users_email;
       public            postgres    false    216            z           1259    73401    ix_users_id    INDEX     ;   CREATE INDEX ix_users_id ON public.users USING btree (id);
    DROP INDEX public.ix_users_id;
       public            postgres    false    216            �           2606    73410    tasks tasks_author_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.tasks DROP CONSTRAINT tasks_author_id_fkey;
       public          postgres    false    3196    217    216               F   x���v
Q���W((M��L�K�I�M�L�/K-*���Ss�	uV�POJ614J6HI1I2T״��� ���         
   x���             
   x���             
   x���         