-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: vizin
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `apartamento`
--

DROP TABLE IF EXISTS `apartamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartamento` (
  `id_apartamento` int NOT NULL AUTO_INCREMENT,
  `numero` int NOT NULL,
  `placa_veiculo` char(7) DEFAULT NULL,
  `bloco` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_apartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE administrador (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `tipo_admin` ENUM ('Sindico Morador', 'Sindico profissional', 'Empresa') NOT NULL,
  `CNPJ` CHAR (14) DEFAULT NULL,
  `inicio_mandato` date NOT NULL,
  `fim_mandato` DATE NOT NULL,
  `nome_admin` VARCHAR (100) NOT NULL,
  `email_admin` VARCHAR (100) NOT NULL UNIQUE,
  `senha_admin` varchar(150) NOT NULL,
  PRIMARY KEY (`id_admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `area_reserva`
--

DROP TABLE IF EXISTS `area_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `area_reserva` (
  `id_area` int NOT NULL AUTO_INCREMENT,
  `tipo_area` varchar(50) NOT NULL,
  `regras` text NOT NULL,
  `taxa_reserva` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id_area`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area_reserva`
--

LOCK TABLES `area_reserva` WRITE;
/*!40000 ALTER TABLE `area_reserva` DISABLE KEYS */;
/*!40000 ALTER TABLE `area_reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comunicado`
--

DROP TABLE IF EXISTS `comunicado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comunicado` (
  `id_comunicado` int NOT NULL AUTO_INCREMENT,
  `tipo_comunicado` enum('Manutencao','Assembleia','Falta de agua','Falta de energia','Seguranca','Evento','Obras','Aviso urgente','Financeiro','Convivencia') NOT NULL,
  `descricao` text NOT NULL,
  `id_admin` int NOT NULL,
  PRIMARY KEY (`id_comunicado`),
  KEY `id_admin` (`id_admin`),
  CONSTRAINT `comunicado_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `administrador` (`id_admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comunicado`
--

LOCK TABLES `comunicado` WRITE;
/*!40000 ALTER TABLE `comunicado` DISABLE KEYS */;
/*!40000 ALTER TABLE `comunicado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encomenda`
--

DROP TABLE IF EXISTS `encomenda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `encomenda` (
  `id_encomenda` int NOT NULL AUTO_INCREMENT,
  `id_apartamento` int NOT NULL,
  `chegada` datetime NOT NULL,
  `status_encomenda` enum('Pendente','Retirada') NOT NULL,
  PRIMARY KEY (`id_encomenda`),
  KEY `id_apartamento` (`id_apartamento`),
  CONSTRAINT `encomenda_ibfk_1` FOREIGN KEY (`id_apartamento`) REFERENCES `apartamento` (`id_apartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encomenda`
--

LOCK TABLES `encomenda` WRITE;
/*!40000 ALTER TABLE `encomenda` DISABLE KEYS */;
/*!40000 ALTER TABLE `encomenda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `escala`
--

DROP TABLE IF EXISTS `escala`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `escala` (
  `data_escala` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fim` time NOT NULL,
  `id_escala` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_escala`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `escala`
--

LOCK TABLES `escala` WRITE;
/*!40000 ALTER TABLE `escala` DISABLE KEYS */;
/*!40000 ALTER TABLE `escala` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionario`
--

DROP TABLE IF EXISTS `funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionario` (
  `id_funcionario` int NOT NULL AUTO_INCREMENT,
  `id_escala` int NOT NULL,
  `nome_funcionario` VARCHAR (100) NOT NULL,
  `email_funcionario` VARCHAR (100) NOT NULL UNIQUE,
  `senha_funcionario` VARCHAR (150) NOT NULL,
  `cargo` enum('Porteiro','Zelador','Administração') NOT NULL,
  PRIMARY KEY (`id_funcionario`),
  KEY `id_escala` (`id_escala`),
  CONSTRAINT `funcionario_ibfk_1` FOREIGN KEY (`id_escala`) REFERENCES `escala` (`id_escala`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionario`
--

LOCK TABLES `funcionario` WRITE;
/*!40000 ALTER TABLE `funcionario` DISABLE KEYS */;
/*!40000 ALTER TABLE `funcionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `morador`
--

DROP TABLE IF EXISTS `morador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `morador` (
  `id_morador` int NOT NULL auto_increment,
  `tipo_morador` enum('Responsavel','Comum') NOT NULL,
  `id_apartamento` int NOT NULL,
  `nome_morador` VARCHAR (100) NOT NULL,
  `email_morador` VARCHAR (100) NOT NULL UNIQUE,
  `senha_morador` VARCHAR (150) NOT NULL,
  PRIMARY KEY (`id_morador`),
  KEY `id_apartamento` (`id_apartamento`),
  CONSTRAINT `morador_ibfk_1` FOREIGN KEY (`id_apartamento`) REFERENCES `apartamento` (`id_apartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `morador`
--

LOCK TABLES `morador` WRITE;
/*!40000 ALTER TABLE `morador` DISABLE KEYS */;
/*!40000 ALTER TABLE `morador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reclamacao`
--

DROP TABLE IF EXISTS `reclamacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reclamacao` (
  `id_reclamacao` int NOT NULL AUTO_INCREMENT,
  `id_apartamento` int NOT NULL,
  `tipo_reclamacao` enum('Barulho','Vaga irregular','Manutencao','Dano a Patrimonio','Animal solto','Problema hidraulico','Outro') NOT NULL,
  `descricao` varchar(300) NOT NULL,
  `data_reclamacao` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_reclamacao`),
  KEY `id_apartamento` (`id_apartamento`),
  CONSTRAINT `fk_reclamacao_apartamento` FOREIGN KEY (`id_apartamento`) REFERENCES `apartamento` (`id_apartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reclamacao`
--

LOCK TABLES `reclamacao` WRITE;
/*!40000 ALTER TABLE `reclamacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `reclamacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocorrencia`
--

DROP TABLE IF EXISTS `ocorrencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocorrencia` (
  `id_ocorrencia` int NOT NULL AUTO_INCREMENT,
  `tipo_ocorrencia` enum('Barulho','Vaga irregular','Manutenção','Dano a patrimônio','Animal solto','Falta de energia','Problema hidráulico','Mudança') NOT NULL,
  `status_ocorrencia` enum('Aberta','Em andamento','Resolvida','Cancelada') NOT NULL,
  `id_reclamacao` INT NOT NULL,
  `descricao_ocorrencia` VARCHAR (300) NOT NULL,
  `id_admin` INT NOT NULL,
  `data_ocorrencia` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_ocorrencia`),
  KEY `fk_ocorrencia_reclamacao` (`id_reclamacao`),
  KEY `fk_ocorrencia_administrador` (`id_admin`),
  CONSTRAINT `fk_ocorrencia_reclamacao` FOREIGN KEY (`id_reclamacao`) REFERENCES `reclamacao` (`id_reclamacao`),
  CONSTRAINT `fk_ocorrencia_administrador` FOREIGN KEY (`id_admin`) REFERENCES `administrador` (`id_admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocorrencia`
--

LOCK TABLES `ocorrencia` WRITE;
/*!40000 ALTER TABLE `ocorrencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `ocorrencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva`
--

DROP TABLE IF EXISTS `reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva` (
  `id_reserva` int NOT NULL AUTO_INCREMENT,
  `horario` time NOT NULL,
  `data_reserva` date NOT NULL,
  `motivo_reserva` varchar(100) NOT NULL,
  `id_apartamento` int NOT NULL,
  `id_area` int NOT NULL,
  PRIMARY KEY (`id_reserva`),
  KEY `id_apartamento` (`id_apartamento`),
  KEY `fk_reserva_area` (`id_area`),
  CONSTRAINT `fk_reserva_area` FOREIGN KEY (`id_area`) REFERENCES `area_reserva` (`id_area`),
  CONSTRAINT `reserva_ibfk_1` FOREIGN KEY (`id_apartamento`) REFERENCES `apartamento` (`id_apartamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visita`
--

DROP TABLE IF EXISTS `visita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visita` (
  `id_visita` INT NOT NULL AUTO_INCREMENT,
  `cpf` CHAR (11) NOT NULL,
  `id_funcionario` INT NOT NULL,
  `nome` VARCHAR (100) DEFAULT NULL,
  `entrada` DATETIME DEFAULT NULL,
  `acesso` INT,
  PRIMARY KEY (`id_visita`),
  UNIQUE KEY `acesso` (`acesso`),
  KEY `id_funcionario` (`id_funcionario`),
  CONSTRAINT `visita_ibfk_1` FOREIGN KEY (`id_funcionario`) REFERENCES `funcionario` (`id_funcionario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

