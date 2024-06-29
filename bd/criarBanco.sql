-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-04-16 00:11:59.84
USE filmes_teste;
-- tables
-- Table: Episodio
CREATE TABLE Episodio (
    titulo_id int  NOT NULL,
    temporada_id int  NOT NULL,
    episodio_id int  NOT NULL auto_increment,
    episodio_nome varchar(40)  NOT NULL,
    episodio_desc varchar(100)  NOT NULL,
    episodio_num int NOT NULL,
    episodio_duracao int  NOT NULL,
    CONSTRAINT Episodio_pk PRIMARY KEY (episodio_id,titulo_id,temporada_id)
);

-- Table: Filme
CREATE TABLE Filme (
    titulo_id int  NOT NULL,
    filme_duracao int  NOT NULL,
    CONSTRAINT Filme_pk PRIMARY KEY (titulo_id)
);

-- Table: Funcao
CREATE TABLE Funcao (
    funcao_id int  NOT NULL auto_increment,
    funcao_nome varchar(40)  NOT NULL,
    CONSTRAINT Funcao_pk PRIMARY KEY (funcao_id)
);

-- Table: Genero
CREATE TABLE Genero (
    genero_id int  NOT NULL auto_increment,
    genero_nome varchar(40)  NOT NULL,
    CONSTRAINT Genero_pk PRIMARY KEY (genero_id)
);

-- Table: Pessoa
CREATE TABLE Pessoa (
    pessoa_id int  NOT NULL auto_increment,
    pessoa_nome varchar(40)  NOT NULL,
    pessoa_desc varchar(100)  NOT NULL,
    CONSTRAINT Pessoa_pk PRIMARY KEY (pessoa_id)
);

-- Table: Serie
CREATE TABLE Serie (
    titulo_id int  NOT NULL,
    serie_temporadas int NOT NULL,
    serie_duracao_epi int NOT NULL,
    CONSTRAINT Serie_pk PRIMARY KEY (titulo_id)
);

-- Table: Temporada
CREATE TABLE Temporada (
    titulo_id int  NOT NULL,
    temporada_id int  NOT NULL auto_increment,
    temporada_nome varchar(40)  NOT NULL,
    temporada_desc varchar(100)  NOT NULL,
    CONSTRAINT Temporada_pk PRIMARY KEY (temporada_id,titulo_id)
);

-- Table: Titulo
CREATE TABLE Titulo (
    titulo_id int  NOT NULL auto_increment,
    titulo_nome varchar(40)  NOT NULL,
    titulo_data_lancamento int NOT NULL,
    titulo_idade int  NOT NULL,
    titulo_sinopse varchar(200)  NOT NULL,
    CONSTRAINT Titulo_pk PRIMARY KEY (titulo_id)
);

-- Table: Titulo_Genero
CREATE TABLE Titulo_Genero (
    titulo_id int  NOT NULL,
    genero_id int  NOT NULL,
    CONSTRAINT Titulo_Genero_pk PRIMARY KEY (titulo_id,genero_id)
);

-- Table: Titulo_Pessoa
CREATE TABLE Titulo_Pessoa (
    titulo_id int  NOT NULL,
    pessoa_id int  NOT NULL,
    funcao_id int  NOT NULL,
    CONSTRAINT Titulo_Pessoa_pk PRIMARY KEY (titulo_id,pessoa_id)
);

-- Table: Usuario
CREATE TABLE Usuario (
    usuario_id int  NOT NULL auto_increment,
    usuario_email varchar(100)  NOT NULL,
    usuario_username varchar(40)  NOT NULL,
    usuario_senha varchar(40)  NOT NULL,
    usuario_recebe_news boolean  NOT NULL,
    CONSTRAINT Usuario_pk PRIMARY KEY (usuario_id)
);

CREATE  UNIQUE INDEX Usuario_idx_1 ON Usuario (usuario_username);

CREATE INDEX Usuario_idx_2 ON Usuario (usuario_email);

-- foreign keys
-- Reference: Episodio_Temporada (table: Episodio)
ALTER TABLE Episodio ADD CONSTRAINT Episodio_Temporada FOREIGN KEY Episodio_Temporada (temporada_id,titulo_id)
    REFERENCES Temporada (temporada_id,titulo_id);

-- Reference: Filme_Titulo (table: Filme)
ALTER TABLE Filme ADD CONSTRAINT Filme_Titulo FOREIGN KEY Filme_Titulo (titulo_id)
    REFERENCES Titulo (titulo_id);

-- Reference: Serie_Titulo (table: Serie)
ALTER TABLE Serie ADD CONSTRAINT Serie_Titulo FOREIGN KEY Serie_Titulo (titulo_id)
    REFERENCES Titulo (titulo_id);

-- Reference: Temporada_Serie (table: Temporada)
ALTER TABLE Temporada ADD CONSTRAINT Temporada_Serie FOREIGN KEY Temporada_Serie (titulo_id)
    REFERENCES Serie (titulo_id);

-- Reference: Titulo_Genero_Genero (table: Titulo_Genero)
ALTER TABLE Titulo_Genero ADD CONSTRAINT Titulo_Genero_Genero FOREIGN KEY Titulo_Genero_Genero (genero_id)
    REFERENCES Genero (genero_id);

-- Reference: Titulo_Genero_Titulo (table: Titulo_Genero)
ALTER TABLE Titulo_Genero ADD CONSTRAINT Titulo_Genero_Titulo FOREIGN KEY Titulo_Genero_Titulo (titulo_id)
    REFERENCES Titulo (titulo_id);

-- Reference: Titulo_Pessoa_Funcao (table: Titulo_Pessoa)
ALTER TABLE Titulo_Pessoa ADD CONSTRAINT Titulo_Pessoa_Funcao FOREIGN KEY Titulo_Pessoa_Funcao (funcao_id)
    REFERENCES Funcao (funcao_id);

-- Reference: Titulo_Pessoa_Pessoa (table: Titulo_Pessoa)
ALTER TABLE Titulo_Pessoa ADD CONSTRAINT Titulo_Pessoa_Pessoa FOREIGN KEY Titulo_Pessoa_Pessoa (pessoa_id)
    REFERENCES Pessoa (pessoa_id);

-- Reference: Titulo_Pessoa_Titulo (table: Titulo_Pessoa)
ALTER TABLE Titulo_Pessoa ADD CONSTRAINT Titulo_Pessoa_Titulo FOREIGN KEY Titulo_Pessoa_Titulo (titulo_id)
    REFERENCES Titulo (titulo_id);

-- End of file.

