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
-- Table structure for table `biddingsystem_message`
--

DROP TABLE IF EXISTS `biddingsystem_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `biddingsystem_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `recipient_id` int NOT NULL,
  `sender_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `biddingsystem_message_recipient_id_0bedc159_fk_auth_user_id` (`recipient_id`),
  KEY `biddingsystem_message_sender_id_eb33bcfd_fk_auth_user_id` (`sender_id`),
  CONSTRAINT `biddingsystem_message_recipient_id_0bedc159_fk_auth_user_id` FOREIGN KEY (`recipient_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `biddingsystem_message_sender_id_eb33bcfd_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biddingsystem_message`
--

LOCK TABLES `biddingsystem_message` WRITE;
/*!40000 ALTER TABLE `biddingsystem_message` DISABLE KEYS */;
INSERT INTO `biddingsystem_message` VALUES (1,'hi this is saad texting gosal','2023-12-19 20:47:34.592513',4,1),(2,'hi there, saad','2023-12-19 20:49:53.283554',1,4),(3,'it is so nice to greet you','2023-12-19 20:50:10.487577',1,4),(4,'hi hissan, how are you? I have got some nice products to sell, thought you might be interested in having a look','2023-12-19 20:51:22.274672',2,4),(5,'im just checking out your listings','2023-12-20 12:48:32.416963',4,1),(6,'hi hissan, how are you','2023-12-20 13:59:20.400174',2,1),(7,'acha saad, do you want anything else from my collection','2023-12-21 00:22:10.450921',1,4),(8,'Hi saad','2023-12-21 06:15:14.837404',1,4),(9,'Hi saad','2023-12-21 06:15:17.527846',1,4),(10,'Kesa hai KARANCHI','2023-12-21 06:15:39.174338',1,4),(11,'Haris Here','2023-12-21 06:15:54.225829',1,4),(12,'hello','2023-12-21 07:16:20.439072',4,1),(13,'hello','2023-12-21 08:34:06.397325',1,4);
/*!40000 ALTER TABLE `biddingsystem_message` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-21 14:06:56
