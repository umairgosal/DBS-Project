CREATE DATABASE  IF NOT EXISTS `biddingsystem` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `biddingsystem`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: biddingproject.mysql.database.azure.com    Database: biddingsystem
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2uw1117qlebt3k6eo1fq8meh2pkw93uj','.eJxVjDsOwjAQBe_iGln-wpqSnjNY610bB5AtxUmFuDtESgHtm5n3EhHXpcZ15DlOLM5Ci8PvlpAeuW2A79huXVJvyzwluSlyp0NeO-fnZXf_DiqO-q1t8GisYjYZQ8kMPhgkf2R0ToO2JQXlkg3ElAorRiDnLRQE0HRSQbw_9Z84ZQ:1rFhCF:8gALv4TCy0OmbDE0oxvuoxSNzE7t4bPWhZQZEH22Jb4','2024-01-02 21:00:11.375606'),('84fw8zt2qah0zdcsmnuhwz5xbfeou8b9','.eJxVjEsOwiAUAO_C2hAKlI9L9z0DeY8HUjWQlHZlvLsh6UK3M5N5swDHXsLR0xZWYlem2OWXIcRnqkPQA-q98djqvq3IR8JP2_nSKL1uZ_s3KNDL2AqD1imPmYhATCSdltEp1Fp6C96j1yJmC7OXZJzTUUxRmdkkgdlZwT5f1ws3UQ:1rFyrC:ssbNlEa_GgAi-KFar8CwwhOW00423TNRpxBUfbzw3tY','2024-01-03 15:51:38.767119'),('amqzcpq8weyjwsbuhwekeoi188l6vcu0','e30:1rExK7:U4ffEmzV5NsYRTeXJzEksmORxZuKG6vuqcjCsAyKmU4','2023-12-31 20:01:15.021308'),('eh85nmg571l2h0o56vwlq6p12bru5y4s','.eJxVjEsOwiAUAO_C2hAKlI9L9z0DeY8HUjWQlHZlvLsh6UK3M5N5swDHXsLR0xZWYlem2OWXIcRnqkPQA-q98djqvq3IR8JP2_nSKL1uZ_s3KNDL2AqD1imPmYhATCSdltEp1Fp6C96j1yJmC7OXZJzTUUxRmdkkgdlZwT5f1ws3UQ:1rFfnr:wAfJU5yMwFm7AqFenwUBluZsrsY9fFsuqOyKR9cwYZo','2024-01-02 19:30:55.868325'),('knbtgjq09idx8gwuvk07x5j6wp67nm6n','e30:1rExK6:G378kIMzE3BBr6oPuXcz-QJC8AvaO22ECfpnDLUUur0','2023-12-31 20:01:14.457364'),('wm2yel7994inwe66bsh0pakle974a1y7','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kGBipGkhKuzL-uzbpQrf3nHNfLMK21riNssQ5szPT7PS7JcBHaTvId2i3zrG3dZkT3xV-0MGvPZfn5XD_DiqM-q1F1o5QO6uNKkl75a1CEg6FkkA2h0ym-KBNQJgckbKSvAAlzIRBCsneH9iiN1Q:1rG6D1:nYeqlmVJjpOp85qid6VwBuYDiVCl_JiGTxdCbCPJ2XM','2024-01-03 23:42:39.193601'),('ylm83n6okg3zxx7mvjwervvfy4tj2qe7','.eJxVjEEOwiAQRe_C2hCmQAMu3XsGMsOMUjWQlHZlvLtt0oVu33v_v1XCdSlp7TKnidVZgTr9MsL8lLoLfmC9N51bXeaJ9J7ow3Z9bSyvy9H-HRTsZVtHIDLAYmgwwgONbMVZ8QEihkzkbo6zCRQ9e4NiHCDYbNGNsJHI6vMF-J44Pg:1rG7mQ:GjWOzwvCghT2rdflPiEJUKhW2Hf5ZUNHyeIQRDDDPqE','2024-01-04 01:23:18.251787');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-21 14:08:11
