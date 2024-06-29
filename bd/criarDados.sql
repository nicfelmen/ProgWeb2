INSERT INTO Titulo (titulo_nome, titulo_data_lancamento, titulo_idade, titulo_sinopse) VALUES ('O Poderoso Chefão',1972, 14, 'O patriarca idoso de uma dinastia do crime organizado transfere o controle de seu império clandestino para seu filho relutante.');
INSERT INTO Titulo (titulo_nome, titulo_data_lancamento, titulo_idade, titulo_sinopse) VALUES ('Forrest Gump', 1994, 14,'O desenrolar da história sob o olhar de Forrest.');
INSERT INTO Titulo (titulo_nome, titulo_data_lancamento, titulo_idade, titulo_sinopse) VALUES ('Breaking Bad', 2008, 16, 'Um professor de química diagnosticado com câncer de pulmão se transforma em fabricante e vendedor de metanfetamina, a fim de garantir o futuro da sua família.');
INSERT INTO Episodio (titulo_id, temporada_id, episodio_id, episodio_nome,episodio_desc, episodio_duracao) VALUES ();
INSERT INTO Filme (titulo_id,filme_duracao) VALUES (1, );
INSERT INTO Funcao (funcao_id,funcao_nome) VALUES();
INSERT INTO Genero (genero_id, genero_nome) VALUES (1,"Ação");
INSERT INTO Genero (genero_id, genero_nome) VALUES (2,"Comédia");
INSERT INTO Genero (genero_id, genero_nome) VALUES (3,"Drama");
INSERT INTO Pessoa (pessoa_id, pessoa_nome, pessoa_desc) VALUES ();
INSERT INTO Serie (titulo_id) VALUES ();
INSERT INTO Temporada (titulo_id, temporada_id, temporada_nome, temporada_desc) VALUES ();
INSERT INTO Titulo_Genero (titulo_id, genero_id) VALUES ();
INSERT INTO Titulo_Pessoa(titulo_id, pessoa_id, funcao_id) VALUES ();
INSERT INTO Usuario (usuario_id, usuario_email, usuario_username, usuario_senha, usuario_recebe_news) VALUES ();

INSERT INTO Titulo (titulo_nome, titulo_idade, titulo_sinopse) VALUES ('Forrest Gump', 1994, 'O desenrolar da história sob o olhar de Forrest.');