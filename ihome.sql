-- MySQL dump 10.13  Distrib 5.7.17, for Win32 (AMD64)
--
-- Host: localhost    Database: ihome
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('54a4d2e55ea2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_area_info`
--

DROP TABLE IF EXISTS `ih_area_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_area_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_area_info`
--

LOCK TABLES `ih_area_info` WRITE;
/*!40000 ALTER TABLE `ih_area_info` DISABLE KEYS */;
INSERT INTO `ih_area_info` VALUES (NULL,NULL,1,'黄浦区'),(NULL,NULL,2,'徐汇区'),(NULL,NULL,3,'长宁区'),(NULL,NULL,4,'静安区'),(NULL,NULL,5,'普陀区'),(NULL,NULL,6,'虹口区'),(NULL,NULL,7,'杨浦区'),(NULL,NULL,8,'闵行区'),(NULL,NULL,9,'宝山区'),(NULL,NULL,10,'嘉定区'),(NULL,NULL,11,'浦东新区'),(NULL,NULL,12,'金山区'),(NULL,NULL,13,'松江区'),(NULL,NULL,14,'青浦区'),(NULL,NULL,15,'奉贤区'),(NULL,NULL,16,'崇明区');
/*!40000 ALTER TABLE `ih_area_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_facility_info`
--

DROP TABLE IF EXISTS `ih_facility_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_facility_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_facility_info`
--

LOCK TABLES `ih_facility_info` WRITE;
/*!40000 ALTER TABLE `ih_facility_info` DISABLE KEYS */;
INSERT INTO `ih_facility_info` VALUES (NULL,NULL,1,'无线网络'),(NULL,NULL,2,'热水淋浴'),(NULL,NULL,3,'空调'),(NULL,NULL,4,'暖气'),(NULL,NULL,5,'允许吸烟'),(NULL,NULL,6,'饮水设备'),(NULL,NULL,7,'牙具'),(NULL,NULL,8,'香皂'),(NULL,NULL,9,'拖鞋'),(NULL,NULL,10,'手纸'),(NULL,NULL,11,'毛巾'),(NULL,NULL,12,'沐浴露、洗发露'),(NULL,NULL,13,'冰箱'),(NULL,NULL,14,'洗衣机'),(NULL,NULL,15,'电梯'),(NULL,NULL,16,'允许做饭'),(NULL,NULL,17,'允许带宠物'),(NULL,NULL,18,'允许聚会'),(NULL,NULL,19,'门禁系统'),(NULL,NULL,20,'停车位'),(NULL,NULL,21,'有线网络'),(NULL,NULL,22,'电视'),(NULL,NULL,23,'浴缸');
/*!40000 ALTER TABLE `ih_facility_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_facility`
--

DROP TABLE IF EXISTS `ih_house_facility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_facility` (
  `house_id` int(11) NOT NULL,
  `facility_id` int(11) NOT NULL,
  PRIMARY KEY (`house_id`,`facility_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `ih_house_facility_ibfk_1` FOREIGN KEY (`facility_id`) REFERENCES `ih_facility_info` (`id`),
  CONSTRAINT `ih_house_facility_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_facility`
--

LOCK TABLES `ih_house_facility` WRITE;
/*!40000 ALTER TABLE `ih_house_facility` DISABLE KEYS */;
INSERT INTO `ih_house_facility` VALUES (2,1),(5,1),(1,2),(3,2),(5,2),(1,3),(5,3),(4,4),(5,4),(5,5),(5,9),(5,10),(5,11),(5,12),(5,13),(5,14),(1,15),(1,19),(1,21);
/*!40000 ALTER TABLE `ih_house_facility` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_image`
--

DROP TABLE IF EXISTS `ih_house_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_image` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL,
  `house_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  CONSTRAINT `ih_house_image_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_image`
--

LOCK TABLES `ih_house_image` WRITE;
/*!40000 ALTER TABLE `ih_house_image` DISABLE KEYS */;
INSERT INTO `ih_house_image` VALUES ('2018-01-10 16:36:30','2018-01-10 16:36:30',1,'FoZg1QLpRi4vckq_W3tBBQe1wJxn',4),('2018-01-10 16:37:03','2018-01-10 16:37:03',2,'FsHyv4WUHKUCpuIRftvwSO_FJWOG',4),('2018-01-10 16:37:58','2018-01-10 16:37:58',3,'FsxYqPJ-fJtVZZH2LEshL7o9Ivxn',4),('2018-01-10 19:33:30','2018-01-10 19:33:30',4,'FsHyv4WUHKUCpuIRftvwSO_FJWOG',5),('2018-01-10 19:37:43','2018-01-10 19:37:43',5,'FsxYqPJ-fJtVZZH2LEshL7o9Ivxn',5),('2018-01-10 19:38:01','2018-01-10 19:38:01',6,'FoZg1QLpRi4vckq_W3tBBQe1wJxn',5);
/*!40000 ALTER TABLE `ih_house_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_info`
--

DROP TABLE IF EXISTS `ih_house_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `price` int(11) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `room_count` int(11) DEFAULT NULL,
  `acreage` int(11) DEFAULT NULL,
  `unit` varchar(32) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `beds` varchar(64) DEFAULT NULL,
  `deposit` int(11) DEFAULT NULL,
  `min_days` int(11) DEFAULT NULL,
  `max_days` int(11) DEFAULT NULL,
  `order_count` int(11) DEFAULT NULL,
  `index_image_url` varchar(256) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `area_id` (`area_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ih_house_info_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `ih_area_info` (`id`),
  CONSTRAINT `ih_house_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_info`
--

LOCK TABLES `ih_house_info` WRITE;
/*!40000 ALTER TABLE `ih_house_info` DISABLE KEYS */;
INSERT INTO `ih_house_info` VALUES ('2018-01-10 12:00:03','2018-01-10 12:00:03',1,'海景房',100000,'航头镇航都路18号',1,10,'一室',2,'双人床:2x1.8x1张',200000,1,1,0,'',4,11),('2018-01-10 16:11:46','2018-01-10 16:11:46',2,'1',100,'1',1,1,'1',1,'1',100,1,1,0,'',4,1),('2018-01-10 16:25:10','2018-01-10 16:25:10',3,'1',100,'1',1,1,'1',1,'1',100,1,1,0,'',4,1),('2018-01-10 16:36:21','2018-01-10 16:36:30',4,'1',100,'1',1,1,'1',1,'1',100,1,1,0,'FoZg1QLpRi4vckq_W3tBBQe1wJxn',4,1),('2018-01-10 19:32:34','2018-01-10 19:33:30',5,'学区房',99900,'航头镇航都路18号',3,30,'两室一厅',4,'2x1.8x1张 1.5x1.8x2张',199900,1,0,0,'FsHyv4WUHKUCpuIRftvwSO_FJWOG',4,11);
/*!40000 ALTER TABLE `ih_house_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_order_info`
--

DROP TABLE IF EXISTS `ih_order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_order_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `begin_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `days` int(11) NOT NULL,
  `house_price` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `status` enum('WAIT_ACCEPT','WAIT_PAYMENT','PAID','WAIT_COMMENT','COMPLETE','CANCELED','REJECTED') DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_ih_order_info_status` (`status`),
  CONSTRAINT `ih_order_info_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`),
  CONSTRAINT `ih_order_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_order_info`
--

LOCK TABLES `ih_order_info` WRITE;
/*!40000 ALTER TABLE `ih_order_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `ih_order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_user_profile`
--

DROP TABLE IF EXISTS `ih_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_user_profile` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `mobile` varchar(11) NOT NULL,
  `real_name` varchar(32) DEFAULT NULL,
  `id_card` varchar(20) DEFAULT NULL,
  `avatar_url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_user_profile`
--

LOCK TABLES `ih_user_profile` WRITE;
/*!40000 ALTER TABLE `ih_user_profile` DISABLE KEYS */;
INSERT INTO `ih_user_profile` VALUES ('2018-01-05 17:03:05','2018-01-05 17:03:05',1,'18812345678','pbkdf2:sha256:50000$DC4xZgpk$430a754b40e02fdb8edc3786cb005f08e4c687e3a86772569facc95ddd44104e','18812345678',NULL,NULL,NULL),('2018-01-05 20:05:46','2018-01-05 20:05:46',2,'18811234567','pbkdf2:sha256:50000$WChQFnGO$583d65d6d1e5f1145ceedcd5c980079c3d299c2d21e4e7bf5a8ee3eecd99b75b','18811234567',NULL,NULL,NULL),('2018-01-05 20:12:24','2018-01-06 22:19:10',3,'zsj1','pbkdf2:sha256:50000$BztLKyDA$171f2fcdb2aefa9276bc3fa60682efc4773d8235ec34369bead5c44d950bbb96','18821345678',NULL,NULL,'FvWngEQNM09Ma4Ba08I1hn7OKcTU'),('2018-01-06 22:43:26','2018-01-07 20:12:19',4,'zsj','pbkdf2:sha256:50000$n3qp36ki$289dfaafefa15061facbee456e49647a9dd92b1873c6b2d924a0f76f2f20e27f','18822345678','zsj','123456789','FvWngEQNM09Ma4Ba08I1hn7OKcTU');
/*!40000 ALTER TABLE `ih_user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-11 20:37:51
