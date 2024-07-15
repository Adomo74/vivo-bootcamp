##API RESTful para Gerenciamento de Produtos
##📒 Descrição
Este projeto é uma API RESTful construída com FastAPI, utilizando MongoDB como banco de dados, Pydantic para validações e Pytest para testes. A API permite a criação, atualização e consulta de produtos, incluindo filtragem por faixa de preço.

##🤖 Tecnologias Utilizadas
FastAPI: Framework para construção de APIs web rápidas e eficientes.
MongoDB: Banco de dados NoSQL para armazenamento dos dados.
Motor: Driver assíncrono para MongoDB.
Pydantic: Biblioteca de validação de dados e parsing para Python.
Pytest: Ferramenta de teste para aplicações Python.
##🧐 Processo de Criação
Configuração do MongoDB: Configuramos a conexão com o MongoDB utilizando motor.motor_asyncio.
Modelos Pydantic: Definimos modelos Pydantic para validação e conversão de dados, incluindo manipulação de ObjectId do MongoDB.
Operações CRUD: Implementamos funções assíncronas para adicionar, atualizar e filtrar produtos.
Rotas FastAPI: Criamos endpoints para criação, atualização e consulta de produtos com base nos modelos Pydantic.
Testes com Pytest: Implementamos testes básicos utilizando Pytest para garantir o funcionamento da API.
