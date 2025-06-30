-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: covers
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cover`
--

DROP TABLE IF EXISTS `cover`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cover` (
  `id` int(11) NOT NULL,
  `modelo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `modelo_id` (`modelo_id`),
  CONSTRAINT `cover_ibfk_1` FOREIGN KEY (`id`) REFERENCES `producto` (`id`),
  CONSTRAINT `cover_ibfk_2` FOREIGN KEY (`modelo_id`) REFERENCES `modelo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cover` 
--

LOCK TABLES `cover` WRITE;
/*!40000 ALTER TABLE `cover` DISABLE KEYS */;
INSERT INTO `cover` VALUES (1,1),(3,1),(5,1),(7,1),(9,1),(2,2),(4,2),(6,2),(8,2),(10,2);
/*!40000 ALTER TABLE `cover` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cover_ocasion`
--

DROP TABLE IF EXISTS `cover_ocasion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cover_ocasion` (
  `id_cover` int(11) NOT NULL,
  `id_ocasion` int(11) NOT NULL,
  PRIMARY KEY (`id_cover`,`id_ocasion`),
  KEY `id_ocasion` (`id_ocasion`),
  CONSTRAINT `cover_ocasion_ibfk_1` FOREIGN KEY (`id_cover`) REFERENCES `cover` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cover_ocasion_ibfk_2` FOREIGN KEY (`id_ocasion`) REFERENCES `ocasion` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cover_ocasion`
--

LOCK TABLES `cover_ocasion` WRITE;
/*!40000 ALTER TABLE `cover_ocasion` DISABLE KEYS */;
INSERT INTO `cover_ocasion` VALUES (1,1),(1,2),(2,3),(2,4),(3,5),(3,6),(4,1),(4,7),(5,8),(5,9),(6,10),(6,11),(7,1),(7,5),(8,2),(8,6),(9,3),(9,7),(10,4),(10,8);
/*!40000 ALTER TABLE `cover_ocasion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modelo`
--

DROP TABLE IF EXISTS `modelo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modelo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modelo`
--

LOCK TABLES `modelo` WRITE;
/*!40000 ALTER TABLE `modelo` DISABLE KEYS */;
INSERT INTO `modelo` VALUES (1,'Iphone 13 Pro'),(2,'Iphone 12 Pro');
/*!40000 ALTER TABLE `modelo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocasion`
--

DROP TABLE IF EXISTS `ocasion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ocasion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocasion`
--

LOCK TABLES `ocasion` WRITE;
/*!40000 ALTER TABLE `ocasion` DISABLE KEYS */;
INSERT INTO `ocasion` VALUES (1,'Casual'),(2,'Formal'),(3,'Informal'),(4,'Gym'),(5,'Skate'),(6,'Hip-Hop'),(7,'Vintage'),(8,'Street'),(9,'Fiesta'),(10,'Trabajo'),(11,'Diario');
/*!40000 ALTER TABLE `ocasion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `precio` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Cover Flame Red','cover','covers/iphone1.png',8,12.00),(2,'Cover Urban Black','cover','covers/iphone1.png',3,10.00),(3,'Cover Skull Art','cover','covers/iphone1.png',6,9.00),(4,'Cover Neon Green','cover','img/iphone1.png',10,14.00),(5,'Cover Lightning Blue','cover','img/iphone1.png',0,11.00),(6,'Cover Retro Wave','cover','img/iphone1.png',7,13.00),(7,'Cover Grunge Fade','cover','img/iphone1.png',5,7.00),(8,'Cover Stealth','cover','img/iphone1.png',12,15.00),(9,'Cover Cyberpunk','cover','img/iphone1.png',4,10.00),(10,'Cover Purple Vibe','cover','img/iphone1.png',6,8.00),(11,'Sticker Skeleton','sticker','img/skeleton.png',10,1.00),(12,'Sticker Graffiti','sticker','img/skeleton.png',15,2.00),(13,'Sticker Street Skull','sticker','img/skeleton.png',8,1.00),(14,'Sticker Boom Box','sticker','img/skeleton.png',20,2.00),(15,'Sticker Vintage Mic','sticker','img/skeleton.png',5,1.00),(16,'Sticker Tape Vibes','sticker','img/skeleton.png',9,2.00),(17,'Sticker Old School','sticker','img/skeleton.png',6,1.00),(18,'Sticker Hip-Hop Hands','sticker','img/skeleton.png',12,2.00),(19,'Sticker 90s Spray','sticker','img/skeleton.png',7,2.00),(20,'Sticker DJ Mix','sticker','img/skeleton.png',11,1.00);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sticker`
--

DROP TABLE IF EXISTS `sticker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sticker` (
  `id` int(11) NOT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `sticker_ibfk_1` FOREIGN KEY (`id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sticker`
--

LOCK TABLES `sticker` WRITE;
/*!40000 ALTER TABLE `sticker` DISABLE KEYS */;
/*!40000 ALTER TABLE `sticker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ventas` (
  `id_venta` int(11) NOT NULL AUTO_INCREMENT,
  `id_cover` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `precio_unitario` decimal(10,2) NOT NULL,
  `fecha_venta` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_venta`),
  KEY `id_cover` (`id_cover`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_cover`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `vista_covers_por_modelo`
--

DROP TABLE IF EXISTS `vista_covers_por_modelo`;
/*!50001 DROP VIEW IF EXISTS `vista_covers_por_modelo`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vista_covers_por_modelo` AS SELECT
 1 AS `id_producto`,
  1 AS `nombre_producto`,
  1 AS `imagen`,
  1 AS `stock`,
  1 AS `precio`,
  1 AS `tipo`,
  1 AS `id_modelo`,
  1 AS `nombre_modelo` */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vista_covers_por_modelo`
--

/*!50001 DROP VIEW IF EXISTS `vista_covers_por_modelo`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_covers_por_modelo` AS select `p`.`id` AS `id_producto`,`p`.`nombre` AS `nombre_producto`,`p`.`imagen` AS `imagen`,`p`.`stock` AS `stock`,`p`.`precio` AS `precio`,`p`.`tipo` AS `tipo`,`m`.`id` AS `id_modelo`,`m`.`nombre` AS `nombre_modelo` from ((`producto` `p` join `cover` `c` on(`p`.`id` = `c`.`id`)) join `modelo` `m` on(`c`.`modelo_id` = `m`.`id`)) where `p`.`tipo` = 'cover' */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-12 11:52:55
