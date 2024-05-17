-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: event
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `budgets`
--

DROP TABLE IF EXISTS `budgets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `budgets` (
  `budget_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int DEFAULT NULL,
  `total_budget` decimal(10,2) DEFAULT NULL,
  `expenses` decimal(10,2) DEFAULT NULL,
  `task_id` int DEFAULT NULL,
  PRIMARY KEY (`budget_id`),
  KEY `event_id` (`event_id`),
  KEY `tid` (`task_id`),
  CONSTRAINT `budgets_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `tid` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budgets`
--

LOCK TABLES `budgets` WRITE;
/*!40000 ALTER TABLE `budgets` DISABLE KEYS */;
INSERT INTO `budgets` VALUES (6,21,10000.00,NULL,15),(7,22,5.00,NULL,16),(8,23,12.00,NULL,17);
/*!40000 ALTER TABLE `budgets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_messages`
--

DROP TABLE IF EXISTS `chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_messages` (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int DEFAULT NULL,
  `receiver_id` int DEFAULT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `file_path` varchar(255) DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  `title` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`chat_id`),
  KEY `e_id` (`event_id`),
  CONSTRAINT `e_id` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_messages`
--

LOCK TABLES `chat_messages` WRITE;
/*!40000 ALTER TABLE `chat_messages` DISABLE KEYS */;
INSERT INTO `chat_messages` VALUES (1,1,2,'hi','2024-05-09 13:15:26','8Sw1.jpg',21,'catering'),(2,2,1,'hello','2024-05-09 13:20:32','5Df8.jpg',21,'catering'),(3,2,1,'ok','2024-05-09 13:23:30','9Wy5.jpg',21,'catering'),(4,2,1,'ji','2024-05-09 13:24:13','9Ys0.jpg',21,'catering'),(5,2,1,'ji','2024-05-09 13:24:37','9Hx8.jpg',21,'catering'),(6,1,2,'ok','2024-05-09 13:30:20','2Ld7.jpg',21,'catering'),(7,1,2,'done','2024-05-09 13:32:56','1Ih1.jpg',21,'catering');
/*!40000 ALTER TABLE `chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `communications`
--

DROP TABLE IF EXISTS `communications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `communications` (
  `communication_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int DEFAULT NULL,
  `message_subject` varchar(255) DEFAULT NULL,
  `message_body` text,
  `sent_to` int DEFAULT NULL,
  `sent_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  `user_type` enum('sender','reviver') DEFAULT NULL,
  `title` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`communication_id`),
  KEY `event_id` (`event_id`),
  KEY `userid` (`user_id`),
  KEY `vid` (`sent_to`),
  CONSTRAINT `communications_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `vid` FOREIGN KEY (`sent_to`) REFERENCES `vendors` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communications`
--

LOCK TABLES `communications` WRITE;
/*!40000 ALTER TABLE `communications` DISABLE KEYS */;
INSERT INTO `communications` VALUES (28,21,'dd','hi',2,'2024-03-31 16:51:02',1,'sender','decoration'),(29,21,'heloo','hello',2,'2024-03-31 16:57:40',1,'sender','decoration'),(30,21,'hi','hello',2,'2024-04-01 09:36:21',1,'sender','catering'),(31,21,'hi','ram',2,'2024-04-01 09:36:34',1,'sender','catering'),(32,22,'budget','pls reduce the budget to 5000',2,'2024-04-01 12:48:12',1,'sender','entertainment'),(33,23,'food items','a,b,c',2,'2024-04-25 10:24:20',1,'sender','catering'),(34,21,'budget','3400 is our finally budget',2,'2024-05-09 10:53:01',1,'sender','catering'),(35,21,'budget','3400 is our finally budget',2,'2024-05-09 10:53:08',1,'sender','catering');
/*!40000 ALTER TABLE `communications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customization`
--

DROP TABLE IF EXISTS `customization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customization` (
  `customization_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  `event_details_customization` text,
  `branding_customization` text,
  `communication_templates_customization` text,
  `title` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`customization_id`),
  KEY `user_id` (`user_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `customization_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `customization_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customization`
--

LOCK TABLES `customization` WRITE;
/*!40000 ALTER TABLE `customization` DISABLE KEYS */;
INSERT INTO `customization` VALUES (4,NULL,21,'df','dfgh','dfghjk','catering'),(5,NULL,21,'','','','catering'),(6,NULL,21,'fgh','vbn','bnm','catering'),(7,NULL,21,'','','','catering'),(8,NULL,21,'as','as','as','catering'),(10,1,24,'anusha','bye','sdfghj','invitations'),(11,1,22,'i need ice cream falvor choclet','ammul','ad','entertainment'),(12,NULL,23,'sdfghjk','xcvbnm,','dfghjkl','catering'),(13,1,23,'sdfghjk','asdfghj','sdfghjk','catering');
/*!40000 ALTER TABLE `customization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `description` text,
  `calendar_integration` enum('yes','no') DEFAULT NULL,
  `services` set('catering','entertainment','venue','decoration','props','invitations') DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (21,1,'Conference','2024-03-26','00:00:23','gannavaram','asdfghj',NULL,'catering,decoration'),(22,1,'Wedding','2024-03-26','00:00:12','Vijayawada','fghjk',NULL,'entertainment,props'),(23,1,'Wedding','2024-03-27','00:00:23','Vijayawada','anusha',NULL,'catering'),(24,1,'birthday party','2024-03-26','00:00:23','Vijayawada','',NULL,'invitations'),(25,1,'birthday party','2024-03-29','10:50:00','gannavaram','ghj',NULL,'decoration,props');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guests`
--

DROP TABLE IF EXISTS `guests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guests` (
  `guest_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `invitation_sent` enum('yes','no') DEFAULT NULL,
  `rsvp_status` enum('yes','no') DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`guest_id`),
  KEY `event_id` (`event_id`),
  KEY `u_id` (`user_id`),
  CONSTRAINT `guests_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `u_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guests`
--

LOCK TABLES `guests` WRITE;
/*!40000 ALTER TABLE `guests` DISABLE KEYS */;
INSERT INTO `guests` VALUES (7,21,'anusha','anusha@codegnan.com','yes','yes',NULL);
/*!40000 ALTER TABLE `guests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `task_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `description` text,
  `deadline` date DEFAULT NULL,
  `assigned_to` int DEFAULT NULL,
  `completion_status` enum('To_start','Inprogress','completed','not yet taken') DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `accept` enum('yes','no') DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  UNIQUE KEY `title` (`title`,`event_id`,`assigned_to`),
  KEY `event_id` (`event_id`),
  KEY `assigned_to` (`assigned_to`),
  KEY `uid` (`user_id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`assigned_to`) REFERENCES `vendors` (`vendor_id`),
  CONSTRAINT `uid` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (15,21,'catering','sdfgh','2024-04-02',2,'completed',1,'yes'),(16,22,'entertainment','xxfghjk','2024-04-02',2,'Inprogress',1,'yes'),(17,23,'catering','sdfgh','2024-04-02',2,'Inprogress',1,'yes');
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` bigint NOT NULL,
  `address` text NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Durga','1230','durgasd1230@gmail.com',8125543632,'8-30-23');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor_services`
--

DROP TABLE IF EXISTS `vendor_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor_services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vendor_id` int DEFAULT NULL,
  `service` enum('catering','entertainment','venue','decoration','props','invitations','photos','beauty') DEFAULT NULL,
  `provided_services` varchar(255) DEFAULT NULL,
  `minimum_capacity` varchar(255) DEFAULT NULL,
  `min_budget` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_id` (`vendor_id`),
  CONSTRAINT `vendor_services_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor_services`
--

LOCK TABLES `vendor_services` WRITE;
/*!40000 ALTER TABLE `vendor_services` DISABLE KEYS */;
INSERT INTO `vendor_services` VALUES (7,2,'invitations','4Ca0.jpg','100',2000),(9,2,'catering','4Lw6.jpg','500',20000),(11,2,'entertainment','3Lz6.jpg','12',12),(12,2,'venue','2Bn0.jpg','200',200000),(13,2,'beauty','2Oz6.jpg','10',70000);
/*!40000 ALTER TABLE `vendor_services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors`
--

DROP TABLE IF EXISTS `vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors` (
  `vendor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `mobile` bigint NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `services` set('catering','entertainment','venue','decoration','props','invitations','photos','beauty') DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors`
--

LOCK TABLES `vendors` WRITE;
/*!40000 ALTER TABLE `vendors` DISABLE KEYS */;
INSERT INTO `vendors` VALUES (2,'Sai Durga',8125543632,'durgasd1230@gmail.com','8-30-23','2000','catering,entertainment,decoration',NULL),(3,'anusha',5678,'durgasd1230@gmail.com','8-30-23','123','decoration,props',NULL),(4,'AnuEvents',6304061929,'badithaanusha206@gmail.com','P.B.Siddhartha Nagar codegnan 23/23','123','catering,entertainment,venue,decoration,props,invitations,beauty','wel2.jpg');
/*!40000 ALTER TABLE `vendors` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-15  9:21:39
