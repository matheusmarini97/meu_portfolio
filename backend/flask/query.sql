CREATE TABLE `Usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `idade` int NOT NULL,
  `data_nascimento` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Usuarios_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;