CREATE DATABASE  IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `mydb`;
-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `model`
--

DROP TABLE IF EXISTS `model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `train_date` datetime DEFAULT NULL,
  `acc` decimal(10,0) NOT NULL,
  `model_type` varchar(45) NOT NULL,
  `dataset_description` varchar(500) DEFAULT NULL,
  `model_path` varchar(500) DEFAULT NULL,
  `disease` varchar(100) NOT NULL,
  `test_data_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
INSERT INTO `model` VALUES (12,'2019-02-03 22:59:18',1,'nnet','leukemia2019-02-03_225905-model_info.json','leukemia2019-02-03_225905','leukemia',NULL),(14,'2019-02-04 12:56:13',0,'nnet','colon(pos-neg)2019-02-04_125611-model_info.json','colon(pos-neg)2019-02-04_125611','colon(pos-neg)',NULL);
/*!40000 ALTER TABLE `model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `patient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'1'),(2,'708011155'),(3,'521201123'),(4,'101039776'),(5,'701221337'),(6,'992664768'),(7,'935096390'),(8,'225905333'),(9,'604002062'),(10,'594155721'),(11,'697416987'),(12,'166771281'),(13,'839647455'),(14,'650747165'),(15,'428201751'),(16,'223262877'),(17,'672396872'),(18,'503299900'),(19,'937643392'),(20,'701180488'),(21,'223510528'),(22,'742628245'),(23,'915711373'),(24,'379532541'),(25,'964365454'),(26,'277589714'),(27,'681523763'),(28,'234465251'),(29,'200367990'),(30,'223953323'),(31,'897409802'),(32,'370107660'),(33,'707755827'),(34,'795672011'),(35,'248559057'),(36,'822394919'),(37,'401222569'),(38,'400887019'),(39,'367492723'),(40,'845535524'),(41,'811192449'),(42,'991446457'),(43,'317455182'),(44,'669442433'),(45,'518606190'),(46,'347257673'),(47,'595373333'),(48,'996125333'),(49,'356344538'),(50,'732970381'),(51,'226251520'),(52,'266378096'),(53,'530352148'),(54,'752162291'),(55,'547282931'),(56,'383120915'),(57,'775986688'),(58,'566131795'),(59,'317308900'),(60,'322758732'),(61,'213245881'),(62,'509177780'),(63,'136754330'),(64,'796797012');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prediction`
--

DROP TABLE IF EXISTS `prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `prediction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  `expression_file_path` varchar(45) NOT NULL,
  `result` varchar(45) NOT NULL,
  `model_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`model_id`,`patient_id`,`user_id`),
  KEY `fk_prediction_model_idx` (`model_id`),
  KEY `fk_prediction_patient1_idx` (`patient_id`),
  KEY `fk_prediction_user1_idx` (`user_id`),
  CONSTRAINT `fk_prediction_model` FOREIGN KEY (`model_id`) REFERENCES `model` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_prediction_patient1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_prediction_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prediction`
--

LOCK TABLES `prediction` WRITE;
/*!40000 ALTER TABLE `prediction` DISABLE KEYS */;
INSERT INTO `prediction` VALUES (3,'2019-02-04 02:13:18','2019-02-04_021313leukemia.tsv','1.0',12,2,3),(4,'2019-02-04 02:13:18','2019-02-04_021313leukemia.tsv','1.0',12,3,3),(5,'2019-02-03 02:13:18','2019-02-04_021313leukemia.tsv','1.0',12,4,3),(6,'2019-02-04 02:13:18','2019-02-04_021313leukemia.tsv','1.0',12,5,3),(7,'2019-02-04 02:13:18','2019-02-04_021313leukemia.tsv','1.0',12,6,3),(8,'2019-02-04 02:13:18','2019-02-04_021313leukemia.tsv','1.0',12,7,3),(9,'2019-02-03 02:13:19','2019-02-04_021313leukemia.tsv','1.0',12,8,3),(10,'2019-02-04 02:13:19','2019-02-04_021313leukemia.tsv','1.0',12,9,3),(11,'2019-02-04 02:13:19','2019-02-04_021313leukemia.tsv','1.0',12,10,3),(12,'2019-02-04 02:13:19','2019-02-04_021313leukemia.tsv','1.0',12,11,3),(13,'2019-02-01 02:13:19','2019-02-04_021313leukemia.tsv','1.0',12,12,3),(14,'2019-02-04 02:13:20','2019-02-04_021313leukemia.tsv','1.0',12,13,3),(15,'2019-02-04 02:13:20','2019-02-04_021313leukemia.tsv','1.0',12,14,3),(16,'2019-02-04 02:13:20','2019-02-04_021313leukemia.tsv','1.0',12,15,3),(17,'2019-02-04 02:13:20','2019-02-04_021313leukemia.tsv','1.0',12,16,3),(18,'2019-02-04 02:13:20','2019-02-04_021313leukemia.tsv','1.0',12,17,3),(19,'2019-02-04 02:13:21','2019-02-04_021313leukemia.tsv','1.0',12,18,3),(20,'2019-02-04 02:13:21','2019-02-04_021313leukemia.tsv','1.0',12,19,3),(21,'2019-02-04 02:13:21','2019-02-04_021313leukemia.tsv','1.0',12,20,3),(22,'2019-02-04 02:13:21','2019-02-04_021313leukemia.tsv','1.0',12,21,3),(23,'2019-02-04 02:13:21','2019-02-04_021313leukemia.tsv','1.0',12,22,3),(24,'2019-02-03 02:13:22','2019-02-04_021313leukemia.tsv','1.0',12,23,3),(25,'2019-02-04 02:13:22','2019-02-04_021313leukemia.tsv','1.0',12,24,3),(26,'2019-02-04 02:13:22','2019-02-04_021313leukemia.tsv','1.0',12,25,3),(27,'2019-02-04 02:13:22','2019-02-04_021313leukemia.tsv','1.0',12,26,3),(28,'2019-02-02 02:13:23','2019-02-04_021313leukemia.tsv','1.0',12,27,3),(29,'2019-02-04 02:13:23','2019-02-04_021313leukemia.tsv','0.0',12,28,3),(30,'2019-02-04 02:13:23','2019-02-04_021313leukemia.tsv','1.0',12,29,3),(31,'2019-02-04 02:13:23','2019-02-04_021313leukemia.tsv','1.0',12,30,3),(32,'2019-02-04 02:13:24','2019-02-04_021313leukemia.tsv','1.0',12,31,3),(33,'2019-02-04 02:13:24','2019-02-04_021313leukemia.tsv','1.0',12,32,3),(34,'2019-02-04 02:13:24','2019-02-04_021313leukemia.tsv','1.0',12,33,3),(35,'2019-02-04 02:13:24','2019-02-04_021313leukemia.tsv','1.0',12,34,3),(36,'2019-02-04 02:13:25','2019-02-04_021313leukemia.tsv','1.0',12,35,3),(95,'2019-02-04 12:46:36','2019-02-04_124634leukemia.tsv','1.0',12,2,22),(96,'2019-02-04 12:46:36','2019-02-04_124634leukemia.tsv','1.0',12,3,22),(97,'2019-02-04 12:46:36','2019-02-04_124634leukemia.tsv','1.0',12,4,22),(98,'2019-02-04 12:46:36','2019-02-04_124634leukemia.tsv','1.0',12,5,22),(99,'2019-02-04 12:46:36','2019-02-04_124634leukemia.tsv','1.0',12,6,22),(100,'2019-02-04 12:46:36','2019-02-04_124634leukemia.tsv','1.0',12,7,22),(101,'2019-02-04 12:46:36','2019-02-04_124634leukemia.tsv','1.0',12,8,22),(102,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,9,22),(103,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,10,22),(104,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,11,22),(105,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,12,22),(106,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,13,22),(107,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,14,22),(108,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,15,22),(109,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,16,22),(110,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,17,22),(111,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,18,22),(112,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,19,22),(113,'2019-02-04 12:46:37','2019-02-04_124634leukemia.tsv','1.0',12,20,22),(114,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,21,22),(115,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,22,22),(116,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,23,22),(117,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,24,22),(118,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,25,22),(119,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,26,22),(120,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,27,22),(121,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','0.0',12,28,22),(122,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,29,22),(123,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,30,22),(124,'2019-02-04 12:46:38','2019-02-04_124634leukemia.tsv','1.0',12,31,22),(125,'2019-02-04 12:46:39','2019-02-04_124634leukemia.tsv','1.0',12,32,22),(126,'2019-02-04 12:46:39','2019-02-04_124634leukemia.tsv','1.0',12,33,22),(127,'2019-02-04 12:46:39','2019-02-04_124634leukemia.tsv','1.0',12,34,22),(128,'2019-02-04 12:46:39','2019-02-04_124634leukemia.tsv','1.0',12,35,22);
/*!40000 ALTER TABLE `prediction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rol` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (3,'marco','65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5','marcomunozperez@uma.es','Admin'),(20,'Dr. Test Pill','65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5','doctor@hospital.com','Doctor'),(22,'Maria Cabello','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','maria@gmail.com','Doctor');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-04 21:15:04
