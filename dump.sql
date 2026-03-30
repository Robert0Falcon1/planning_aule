-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: prenotazione_aule
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

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
-- Table structure for table `allievi`
--

DROP TABLE IF EXISTS `allievi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `allievi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cognome` varchar(100) NOT NULL,
  `codice_fiscale` varchar(16) DEFAULT NULL,
  `data_nascita` date DEFAULT NULL,
  `nazione_nascita` varchar(100) DEFAULT NULL,
  `provincia_nascita` varchar(5) DEFAULT NULL,
  `comune_nascita` varchar(100) DEFAULT NULL,
  `sesso` enum('M','F','A') DEFAULT NULL,
  `cittadinanza` enum('COMUNITARIA','EXTRA_COMUNITARIA') DEFAULT NULL,
  `paese` varchar(100) DEFAULT NULL COMMENT 'Derivato da cittadinanza, gestito lato backend',
  `residente_in` enum('ITALIA','ESTERO') DEFAULT NULL,
  `provincia_residenza` varchar(5) DEFAULT NULL,
  `comune_residenza` varchar(100) DEFAULT NULL,
  `indirizzo` varchar(255) DEFAULT NULL,
  `cap` varchar(10) DEFAULT NULL,
  `telefono_prefisso` varchar(10) DEFAULT NULL,
  `telefono_numero` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `data_firma_patto_attivazione` date DEFAULT NULL,
  `data_iscrizione` date DEFAULT NULL,
  `data_inizio_frequenza` date DEFAULT NULL,
  `data_ritiro` date DEFAULT NULL,
  `motivo_ritiro` varchar(500) DEFAULT NULL,
  `posizione_registro_cartaceo` int(11) DEFAULT NULL COMMENT 'Corrispondenza registro cartaceo / Sistema Piemonte',
  `ore_assenza` float NOT NULL,
  `ore_erogate` float NOT NULL,
  `uditore` tinyint(1) NOT NULL COMMENT 'Se True l''allievo è uditore non formale',
  `livello_istruzione` enum('NESSUN_TITOLO','LICENZA_ELEMENTARE','LICENZA_MEDIA','QUALIFICA_PROFESSIONALE','DIPLOMA_SUPERIORE','DIPLOMA_TECNICO_SUPERIORE','LAUREA_TRIENNALE','LAUREA_MAGISTRALE','DOTTORATO') DEFAULT NULL,
  `condizione_occupazionale` enum('DISOCCUPATO','INOCCUPATO','OCCUPATO_DIPENDENTE','OCCUPATO_AUTONOMO','OCCUPATO_CIGO','OCCUPATO_CIGS','STUDENTE') DEFAULT NULL,
  `disabilita_vulnerabilita` enum('NESSUNA','DSA','DISABILITA','EES','SVANTAGGIO_CULTURALE') DEFAULT NULL,
  `svantaggio_abitativo` enum('SVANTAGGIO','NESSUNA') DEFAULT NULL,
  `documenti_allegati` text DEFAULT NULL COMMENT 'Nomi file separati da virgola',
  PRIMARY KEY (`id`),
  KEY `ix_allievi_id` (`id`),
  KEY `ix_allievi_codice_fiscale` (`codice_fiscale`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `allievi`
--

LOCK TABLES `allievi` WRITE;
/*!40000 ALTER TABLE `allievi` DISABLE KEYS */;
INSERT INTO `allievi` VALUES (1,'Sara','Colombo','CLMSRA95C46L219Z','1995-03-06',NULL,NULL,NULL,'F','COMUNITARIA',NULL,'ITALIA','TO','Torino',NULL,NULL,NULL,NULL,NULL,NULL,'2025-01-07','2025-01-07',NULL,NULL,1,4,48,0,'DIPLOMA_SUPERIORE','DISOCCUPATO','NESSUNA','NESSUNA',NULL),(2,'Ahmed','Ben Ali','BNLHMD88T10Z330K','1988-12-10',NULL,NULL,NULL,'M','EXTRA_COMUNITARIA',NULL,'ITALIA','TO','Torino',NULL,NULL,NULL,NULL,NULL,NULL,'2025-01-07','2025-01-07',NULL,NULL,2,8,48,0,'LICENZA_MEDIA','DISOCCUPATO','NESSUNA','SVANTAGGIO',NULL),(3,'Marta','Ferrara','FRRMRT90D50H501P','1990-04-10',NULL,NULL,NULL,'F','COMUNITARIA',NULL,'ITALIA','TO','Moncalieri',NULL,NULL,NULL,NULL,NULL,NULL,'2025-01-07','2025-01-07',NULL,NULL,3,0,48,0,'LAUREA_TRIENNALE','INOCCUPATO','NESSUNA','NESSUNA',NULL),(4,'Davide','Greco','GRCDVD85M20L219R','1985-08-20',NULL,NULL,NULL,'M','COMUNITARIA',NULL,'ITALIA','TO','Torino',NULL,NULL,NULL,NULL,NULL,NULL,'2025-03-03','2025-03-03',NULL,NULL,1,0,24,0,'LAUREA_MAGISTRALE','OCCUPATO_DIPENDENTE','NESSUNA','NESSUNA',NULL),(5,'Chiara','Martini','MRTCHR92P50L219Y','1992-09-10',NULL,NULL,NULL,'F','COMUNITARIA',NULL,'ITALIA','TO','Collegno',NULL,NULL,NULL,NULL,NULL,NULL,'2025-03-03','2025-03-03',NULL,NULL,2,2,24,0,'DIPLOMA_SUPERIORE','OCCUPATO_AUTONOMO','DSA','NESSUNA',NULL),(6,'Fabio','Serra','SRRFBZ79A01H501W','1979-01-01',NULL,NULL,NULL,'M','COMUNITARIA',NULL,'ITALIA','TO','Torino',NULL,NULL,NULL,NULL,NULL,NULL,'2025-01-07','2025-01-07','2025-02-14','Inserimento lavorativo',4,0,20,0,'QUALIFICA_PROFESSIONALE','DISOCCUPATO','NESSUNA','NESSUNA',NULL);
/*!40000 ALTER TABLE `allievi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attrezzature`
--

DROP TABLE IF EXISTS `attrezzature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attrezzature` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` enum('PC','PROIETTORE','LAVAGNA','CASSE_AUDIO','MICROFONO','WEBCAM') NOT NULL,
  `descrizione` varchar(255) DEFAULT NULL,
  `quantita_disponibile` int(11) NOT NULL,
  `sede_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sede_id` (`sede_id`),
  KEY `ix_attrezzature_id` (`id`),
  CONSTRAINT `attrezzature_ibfk_1` FOREIGN KEY (`sede_id`) REFERENCES `sedi` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attrezzature`
--

LOCK TABLES `attrezzature` WRITE;
/*!40000 ALTER TABLE `attrezzature` DISABLE KEYS */;
/*!40000 ALTER TABLE `attrezzature` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aule`
--

DROP TABLE IF EXISTS `aule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `capienza` int(11) NOT NULL COMMENT 'Numero massimo di partecipanti nell''aula',
  `sede_id` int(11) NOT NULL,
  `note` varchar(500) DEFAULT NULL,
  `attiva` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sede_id` (`sede_id`),
  KEY `ix_aule_id` (`id`),
  CONSTRAINT `aule_ibfk_1` FOREIGN KEY (`sede_id`) REFERENCES `sedi` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aule`
--

LOCK TABLES `aule` WRITE;
/*!40000 ALTER TABLE `aule` DISABLE KEYS */;
INSERT INTO `aule` VALUES (1,'Aula Mango',25,2,'Aula 1 - informatica',1),(2,'Aula Lime',21,2,'Aula 2',1),(3,'Aula Gialla',18,3,NULL,1),(4,'Aula Arancio',21,3,'Aula informatica - PC',1),(5,'Aula Verde',25,3,NULL,1),(6,'Aula Azzurra',20,3,NULL,1),(7,'Aula Viola',25,3,NULL,1),(8,'Aula 1',15,4,NULL,1),(9,'Aula 1',21,5,NULL,1),(10,'Aula 2',16,5,NULL,1),(11,'Aula 1',26,6,'Aula informatica - PC',1),(12,'Aula 2',17,6,NULL,1),(13,'Aula 3',22,6,NULL,1),(14,'Aula 1',24,7,NULL,1),(15,'Aula 2',23,7,NULL,1),(16,'Aula 3',23,7,NULL,1),(17,'Aula 4',31,7,NULL,1),(21,'Aula 1',10,9,'Sala riunioni',1),(25,'Aula Dragonfruit',3,2,'Aula Cm 1',0),(26,'Aula Cocco',5,2,'Aula CM2',0),(27,'Sala Riunioni',15,7,NULL,1),(28,'Corsi fuori sede',20,7,NULL,1),(29,'Salone',25,9,NULL,0),(30,'Biblioteca',15,9,NULL,0),(31,'Aula 4',20,6,NULL,1);
/*!40000 ALTER TABLE `aule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogo`
--

DROP TABLE IF EXISTS `catalogo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stato` smallint(6) NOT NULL,
  `profilo_formativo` varchar(255) DEFAULT NULL,
  `tipologia_utilizzo_parziale` smallint(6) NOT NULL,
  `formazione_normata` smallint(6) NOT NULL,
  `tipologia` varchar(100) DEFAULT NULL,
  `sep` varchar(100) DEFAULT NULL,
  `area_professionale` varchar(255) DEFAULT NULL,
  `sottoarea_professionale` varchar(255) DEFAULT NULL,
  `codice_ada` varchar(50) DEFAULT NULL,
  `titolo_ada` varchar(255) DEFAULT NULL,
  `competenze` text DEFAULT NULL,
  `professioni_nup_istat` text DEFAULT NULL,
  `attivita_economiche_ateco_istat` text DEFAULT NULL,
  `titolo_percorso` varchar(255) DEFAULT NULL,
  `titolo_attestato` varchar(255) DEFAULT NULL,
  `certificazione_uscita` varchar(255) DEFAULT NULL,
  `tipologia_prova_finale` varchar(100) DEFAULT NULL,
  `durata_prova_ore` decimal(5,2) DEFAULT NULL,
  `prova_ingresso_orientamento` varchar(255) DEFAULT NULL,
  `ore_corso_minime` decimal(6,2) DEFAULT NULL,
  `ore_stage_minime` decimal(6,2) DEFAULT NULL,
  `ore_elearning_minime_perc` decimal(5,2) DEFAULT NULL,
  `ore_corso_massime` decimal(6,2) DEFAULT NULL,
  `ore_stage_massime` decimal(6,2) DEFAULT NULL,
  `ore_elearning_massime_perc` decimal(5,2) DEFAULT NULL,
  `normativa_riferimento` text DEFAULT NULL,
  `ore_assenza_massime` decimal(6,2) DEFAULT NULL,
  `assegnazione_credito_ingresso` smallint(6) NOT NULL,
  `data_inizio_validita` date DEFAULT NULL,
  `data_fine_validita` date DEFAULT NULL,
  `eta` varchar(100) DEFAULT NULL,
  `livello_minimo_scolarita` varchar(100) DEFAULT NULL,
  `livello_massimo_scolarita` varchar(100) DEFAULT NULL,
  `obbligo_scolastico_assolto` smallint(6) DEFAULT NULL,
  `esperienze_lavorative_pregresse` text DEFAULT NULL,
  `stato_occupazionale_ammesso` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogo`
--

LOCK TABLES `catalogo` WRITE;
/*!40000 ALTER TABLE `catalogo` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conflitti_prenotazione`
--

DROP TABLE IF EXISTS `conflitti_prenotazione`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conflitti_prenotazione` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prenotazione_id_1` int(11) NOT NULL,
  `prenotazione_id_2` int(11) NOT NULL,
  `slot_id_1` int(11) DEFAULT NULL,
  `slot_id_2` int(11) DEFAULT NULL,
  `tipo_conflitto` enum('OVERLAP_ORARIO','DOPPIA_PRENOTAZIONE','ALTRO') NOT NULL,
  `rilevato_il` datetime NOT NULL,
  `stato_risoluzione` enum('RISOLTO_MANTENUTA_1','RISOLTO_MANTENUTA_2','RISOLTO_ELIMINATE_ENTRAMBE') DEFAULT NULL,
  `risolto_il` datetime DEFAULT NULL,
  `risolto_da` int(11) DEFAULT NULL,
  `note_risoluzione` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `risolto_da` (`risolto_da`),
  KEY `ix_conflitti_prenotazione_stato_risoluzione` (`stato_risoluzione`),
  KEY `ix_conflitti_prenotazione_prenotazione_id_2` (`prenotazione_id_2`),
  KEY `ix_conflitti_prenotazione_id` (`id`),
  KEY `ix_conflitti_prenotazione_prenotazione_id_1` (`prenotazione_id_1`),
  KEY `ix_conflitti_prenotazione_rilevato_il` (`rilevato_il`),
  KEY `fk_conflitto_slot1` (`slot_id_1`),
  KEY `fk_conflitto_slot2` (`slot_id_2`),
  CONSTRAINT `conflitti_prenotazione_ibfk_1` FOREIGN KEY (`prenotazione_id_1`) REFERENCES `prenotazioni` (`id`) ON DELETE CASCADE,
  CONSTRAINT `conflitti_prenotazione_ibfk_2` FOREIGN KEY (`prenotazione_id_2`) REFERENCES `prenotazioni` (`id`) ON DELETE CASCADE,
  CONSTRAINT `conflitti_prenotazione_ibfk_3` FOREIGN KEY (`risolto_da`) REFERENCES `utenti` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_conflitto_slot1` FOREIGN KEY (`slot_id_1`) REFERENCES `slot_orari` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_conflitto_slot2` FOREIGN KEY (`slot_id_2`) REFERENCES `slot_orari` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=239 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conflitti_prenotazione`
--

LOCK TABLES `conflitti_prenotazione` WRITE;
/*!40000 ALTER TABLE `conflitti_prenotazione` DISABLE KEYS */;
INSERT INTO `conflitti_prenotazione` VALUES (126,228,265,445,574,'OVERLAP_ORARIO','2026-03-23 09:48:33','RISOLTO_MANTENUTA_2','2026-03-23 09:48:46',8,''),(127,228,265,446,575,'OVERLAP_ORARIO','2026-03-23 09:48:33','RISOLTO_MANTENUTA_1','2026-03-23 09:48:54',8,''),(128,228,265,449,577,'OVERLAP_ORARIO','2026-03-23 09:48:33','RISOLTO_MANTENUTA_2','2026-03-23 09:48:55',8,''),(129,228,265,454,580,'OVERLAP_ORARIO','2026-03-23 09:48:33','RISOLTO_ELIMINATE_ENTRAMBE','2026-03-23 09:48:56',8,''),(161,248,299,494,658,'OVERLAP_ORARIO','2026-03-24 15:54:00','RISOLTO_MANTENUTA_2','2026-03-25 09:04:23',9,''),(162,248,299,497,660,'OVERLAP_ORARIO','2026-03-24 15:54:00','RISOLTO_MANTENUTA_1','2026-03-25 09:04:26',9,''),(163,248,299,500,662,'OVERLAP_ORARIO','2026-03-24 15:54:00','RISOLTO_MANTENUTA_2','2026-03-25 09:04:27',9,''),(164,270,312,599,685,'OVERLAP_ORARIO','2026-03-25 08:28:35','RISOLTO_ELIMINATE_ENTRAMBE','2026-03-25 09:04:25',9,''),(165,270,312,604,686,'OVERLAP_ORARIO','2026-03-25 08:28:35','RISOLTO_ELIMINATE_ENTRAMBE','2026-03-25 09:04:31',9,''),(166,270,312,609,687,'OVERLAP_ORARIO','2026-03-25 08:28:35','RISOLTO_MANTENUTA_2','2026-03-25 09:04:22',9,''),(167,270,312,614,688,'OVERLAP_ORARIO','2026-03-25 08:28:35','RISOLTO_ELIMINATE_ENTRAMBE','2026-03-25 09:04:32',9,''),(171,279,321,630,709,'OVERLAP_ORARIO','2026-03-26 08:05:23','RISOLTO_MANTENUTA_1','2026-03-26 14:42:47',NULL,'Chiuso automaticamente per modifica slot'),(173,315,319,691,707,'OVERLAP_ORARIO','2026-03-26 09:43:56','RISOLTO_MANTENUTA_1','2026-03-26 09:48:54',NULL,'Chiuso automaticamente per modifica slot'),(174,299,323,658,711,'OVERLAP_ORARIO','2026-03-26 09:56:09','RISOLTO_MANTENUTA_1','2026-03-26 10:02:22',NULL,'Chiuso automaticamente per modifica slot'),(175,248,323,505,711,'OVERLAP_ORARIO','2026-03-26 10:02:22','RISOLTO_MANTENUTA_1','2026-03-26 10:02:30',NULL,'Chiuso automaticamente per modifica slot'),(176,248,323,497,711,'OVERLAP_ORARIO','2026-03-26 10:02:30','RISOLTO_MANTENUTA_1','2026-03-26 10:02:41',NULL,'Chiuso automaticamente per modifica slot'),(177,248,323,497,711,'OVERLAP_ORARIO','2026-03-26 10:15:36','RISOLTO_MANTENUTA_2','2026-03-26 15:18:47',NULL,NULL),(178,328,331,716,719,'OVERLAP_ORARIO','2026-03-26 11:06:10','RISOLTO_MANTENUTA_1','2026-03-26 11:29:10',NULL,'Chiuso automaticamente per modifica slot'),(179,339,340,763,771,'OVERLAP_ORARIO','2026-03-26 11:14:09','RISOLTO_MANTENUTA_1','2026-03-26 11:34:31',NULL,'Chiuso automaticamente per modifica slot'),(180,339,340,765,772,'OVERLAP_ORARIO','2026-03-26 11:14:09','RISOLTO_MANTENUTA_1','2026-03-26 11:35:59',NULL,'Chiuso automaticamente per modifica slot'),(181,339,340,767,773,'OVERLAP_ORARIO','2026-03-26 11:14:09','RISOLTO_MANTENUTA_1','2026-03-26 11:41:01',NULL,'Chiuso automaticamente per modifica slot'),(182,339,340,769,774,'OVERLAP_ORARIO','2026-03-26 11:14:09','RISOLTO_MANTENUTA_1','2026-03-26 11:47:27',NULL,'Chiuso automaticamente per modifica slot'),(183,326,331,714,719,'OVERLAP_ORARIO','2026-03-26 11:29:10','RISOLTO_MANTENUTA_1','2026-03-26 11:29:31',NULL,'Chiuso automaticamente per modifica slot'),(191,279,321,630,709,'OVERLAP_ORARIO','2026-03-26 14:42:47','RISOLTO_MANTENUTA_1','2026-03-26 14:45:03',NULL,'Chiuso automaticamente per modifica slot'),(192,279,321,630,709,'OVERLAP_ORARIO','2026-03-26 14:45:03','RISOLTO_MANTENUTA_1','2026-03-26 14:49:22',NULL,'Chiuso automaticamente per modifica slot'),(193,279,321,630,709,'OVERLAP_ORARIO','2026-03-26 14:49:22','RISOLTO_MANTENUTA_1','2026-03-26 14:49:42',NULL,'Chiuso automaticamente per modifica slot'),(194,279,321,630,709,'OVERLAP_ORARIO','2026-03-26 14:49:42','RISOLTO_MANTENUTA_1','2026-03-26 14:50:41',NULL,'Chiuso automaticamente per modifica slot'),(195,279,321,630,709,'OVERLAP_ORARIO','2026-03-26 14:50:41','RISOLTO_MANTENUTA_1','2026-03-26 14:50:57',NULL,'Chiuso automaticamente per modifica slot'),(218,265,371,574,811,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_2','2026-03-27 13:11:58',NULL,NULL),(219,228,371,446,812,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-27 13:12:10',NULL,NULL),(220,228,371,447,813,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-27 13:13:43',NULL,NULL),(221,265,371,576,814,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-27 13:25:29',NULL,NULL),(222,265,371,577,815,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_2','2026-03-27 14:56:53',NULL,NULL),(223,265,371,578,817,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-27 14:56:10',NULL,NULL),(224,265,371,579,818,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-28 12:38:06',NULL,NULL),(225,265,371,581,821,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-28 12:38:11',NULL,NULL),(226,265,371,583,824,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_2','2026-03-28 12:38:17',NULL,NULL),(227,265,371,584,826,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-28 12:38:20',NULL,NULL),(228,265,371,585,827,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_2','2026-03-28 12:38:26',NULL,NULL),(229,265,371,586,829,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_2','2026-03-28 12:38:29',NULL,NULL),(230,265,371,587,830,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_2','2026-03-28 12:38:32',NULL,NULL),(231,265,371,588,832,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-28 12:38:35',NULL,NULL),(232,265,371,589,833,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_2','2026-03-28 12:38:39',NULL,NULL),(233,265,371,590,835,'OVERLAP_ORARIO','2026-03-27 13:11:15','RISOLTO_MANTENUTA_1','2026-03-28 12:38:42',NULL,NULL),(236,228,388,459,889,'OVERLAP_ORARIO','2026-03-28 14:59:32','RISOLTO_MANTENUTA_1','2026-03-28 15:00:23',NULL,'Chiuso automaticamente per modifica slot'),(238,317,392,693,893,'OVERLAP_ORARIO','2026-03-29 16:43:00','RISOLTO_MANTENUTA_2','2026-03-29 16:43:43',NULL,NULL);
/*!40000 ALTER TABLE `conflitti_prenotazione` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corsi`
--

DROP TABLE IF EXISTS `corsi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `corsi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codice` varchar(50) NOT NULL COMMENT 'Formato: B164-{progressivo}-{anno}-{accorpamento}',
  `titolo` varchar(255) NOT NULL,
  `descrizione` text DEFAULT NULL COMMENT 'Derivato dal repertorio regionale',
  `tipo_finanziamento` enum('FINANZIATO_PUBBLICO','A_PAGAMENTO','MISTO') NOT NULL,
  `stato_del_corso` enum('APPROVATO','AVVIATO','IN_CORSO','CONCLUSO','RENDICONTATO','SALDATO','RINUNCIA') DEFAULT NULL COMMENT 'Codice stato Sistema Piemonte',
  `numero_proposta` int(11) DEFAULT NULL,
  `id_corso_finanziato` int(11) DEFAULT NULL COMMENT '15xxxx=GOL · 10xxxx=FSE',
  `id_attivita` int(11) DEFAULT NULL,
  `criterio_selezione_destinatari` varchar(500) DEFAULT NULL,
  `responsabile_id` int(11) NOT NULL,
  `sede_id` int(11) DEFAULT NULL,
  `data_creazione` datetime DEFAULT NULL,
  `data_avvio_corso` date DEFAULT NULL COMMENT 'Data avvio formale su Sistema Piemonte',
  `data_inizio_corso` date NOT NULL,
  `data_fine_presunta` date NOT NULL,
  `attivo` tinyint(1) DEFAULT NULL,
  `num_partecipanti` int(11) NOT NULL,
  `ore_totali` float DEFAULT NULL COMMENT 'Ore totali previste dal progetto formativo',
  `ore_erogate` float NOT NULL,
  `ore_stage` float DEFAULT NULL,
  `ore_verifica_finale` float DEFAULT NULL,
  `ente_stage` varchar(255) DEFAULT NULL COMMENT 'Derivato da mapping allievi',
  `ore_aggiuntive` float DEFAULT NULL COMMENT 'Ore discrezionali del docente (test ITA/Informatica)',
  `ore_accertamento_stranieri` enum('ITALIANO','MATEMATICA','INGLESE') DEFAULT NULL COMMENT 'Tipo prova accertamento: 40 min × prova fissa',
  `ore_selezione_allievi` float DEFAULT NULL COMMENT 'Inserite dal RC dal frontend, modificabili',
  `ore_prova_finale` float DEFAULT NULL COMMENT 'Inserite dal RC dal frontend, modificabili',
  `avvio_anticipato` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_corsi_codice` (`codice`),
  KEY `responsabile_id` (`responsabile_id`),
  KEY `sede_id` (`sede_id`),
  KEY `ix_corsi_id` (`id`),
  CONSTRAINT `corsi_ibfk_1` FOREIGN KEY (`responsabile_id`) REFERENCES `utenti` (`id`),
  CONSTRAINT `corsi_ibfk_2` FOREIGN KEY (`sede_id`) REFERENCES `sedi` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corsi`
--

LOCK TABLES `corsi` WRITE;
/*!40000 ALTER TABLE `corsi` DISABLE KEYS */;
INSERT INTO `corsi` VALUES (1,'SSMTO-2026-01','GOL - Segreteria Studio Medico','Percorso GOL per disoccupati — Segreteria Studio Medico','FINANZIATO_PUBBLICO','IN_CORSO',1042,1500234,NULL,NULL,1,3,'2026-03-04 14:42:37',NULL,'2026-02-01','2026-05-07',1,15,144,48,100,NULL,NULL,NULL,NULL,NULL,NULL,0),(2,'CARRTO-2025-10','GOL - Carrellisti','Percorso GOL per disoccupati — Carrellisti','FINANZIATO_PUBBLICO','IN_CORSO',2018,1000891,NULL,NULL,1,3,'2026-03-04 14:42:37',NULL,'2025-03-03','2025-09-30',1,20,12,9,0,NULL,NULL,NULL,NULL,NULL,NULL,0),(3,'VERAT2026-01','FSE - Manutentore del Verde (Asti)','Corso FSE finanziato - Manutentore del verde','FINANZIATO_PUBBLICO','IN_CORSO',1058,1500402,NULL,NULL,3,5,'2026-03-04 14:42:37',NULL,'2025-02-01','2025-07-31',1,18,172,32,0,NULL,NULL,NULL,NULL,NULL,NULL,0);
/*!40000 ALTER TABLE `corsi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corso_allievi`
--

DROP TABLE IF EXISTS `corso_allievi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `corso_allievi` (
  `corso_id` int(11) NOT NULL,
  `allievo_id` int(11) NOT NULL,
  PRIMARY KEY (`corso_id`,`allievo_id`),
  KEY `allievo_id` (`allievo_id`),
  CONSTRAINT `corso_allievi_ibfk_1` FOREIGN KEY (`corso_id`) REFERENCES `corsi` (`id`),
  CONSTRAINT `corso_allievi_ibfk_2` FOREIGN KEY (`allievo_id`) REFERENCES `allievi` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corso_allievi`
--

LOCK TABLES `corso_allievi` WRITE;
/*!40000 ALTER TABLE `corso_allievi` DISABLE KEYS */;
INSERT INTO `corso_allievi` VALUES (1,1),(1,2),(1,3),(1,6),(2,4),(2,5);
/*!40000 ALTER TABLE `corso_allievi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corso_docenti`
--

DROP TABLE IF EXISTS `corso_docenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `corso_docenti` (
  `corso_id` int(11) NOT NULL,
  `docente_id` int(11) NOT NULL,
  PRIMARY KEY (`corso_id`,`docente_id`),
  KEY `docente_id` (`docente_id`),
  CONSTRAINT `corso_docenti_ibfk_1` FOREIGN KEY (`corso_id`) REFERENCES `corsi` (`id`),
  CONSTRAINT `corso_docenti_ibfk_2` FOREIGN KEY (`docente_id`) REFERENCES `docenti` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corso_docenti`
--

LOCK TABLES `corso_docenti` WRITE;
/*!40000 ALTER TABLE `corso_docenti` DISABLE KEYS */;
INSERT INTO `corso_docenti` VALUES (1,1),(1,3),(2,2),(2,4),(3,1);
/*!40000 ALTER TABLE `corso_docenti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `docente_sedi`
--

DROP TABLE IF EXISTS `docente_sedi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `docente_sedi` (
  `docente_id` int(11) NOT NULL,
  `sede_id` int(11) NOT NULL,
  PRIMARY KEY (`docente_id`,`sede_id`),
  KEY `sede_id` (`sede_id`),
  CONSTRAINT `docente_sedi_ibfk_1` FOREIGN KEY (`docente_id`) REFERENCES `docenti` (`id`),
  CONSTRAINT `docente_sedi_ibfk_2` FOREIGN KEY (`sede_id`) REFERENCES `sedi` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `docente_sedi`
--

LOCK TABLES `docente_sedi` WRITE;
/*!40000 ALTER TABLE `docente_sedi` DISABLE KEYS */;
INSERT INTO `docente_sedi` VALUES (1,3),(1,4),(2,3),(3,3),(3,5),(4,3);
/*!40000 ALTER TABLE `docente_sedi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `docenti`
--

DROP TABLE IF EXISTS `docenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `docenti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cognome` varchar(100) NOT NULL,
  `codice_fiscale` varchar(16) DEFAULT NULL,
  `livello_istruzione` enum('NESSUN_TITOLO','LICENZA_ELEMENTARE','LICENZA_MEDIA','QUALIFICA_PROFESSIONALE','DIPLOMA_SUPERIORE','DIPLOMA_TECNICO_SUPERIORE','LAUREA_TRIENNALE','LAUREA_MAGISTRALE','DOTTORATO') DEFAULT NULL,
  `tipologia` enum('T','P','S') NOT NULL COMMENT 'T=Teoria · P=Pratica · S=Stage',
  `webinar` tinyint(1) DEFAULT NULL COMMENT 'Se True il docente opera in remoto e non occupa aula fisica',
  `ore_di_incarico` float DEFAULT NULL COMMENT 'Ore totali contrattualizzate per il corso',
  `ore_svolte` float NOT NULL,
  `unita_formative` varchar(1000) DEFAULT NULL COMMENT 'Unità formative assegnate, separate da virgola',
  PRIMARY KEY (`id`),
  KEY `ix_docenti_codice_fiscale` (`codice_fiscale`),
  KEY `ix_docenti_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `docenti`
--

LOCK TABLES `docenti` WRITE;
/*!40000 ALTER TABLE `docenti` DISABLE KEYS */;
INSERT INTO `docenti` VALUES (1,'Francesca','Amato','AMTFNC80A41L219X','LAUREA_MAGISTRALE','T',0,120,0,'Comunicazione efficace,Orientamento al lavoro'),(2,'Giorgio','Ferretti','FRTGRG75C12F205K','LAUREA_TRIENNALE','P',0,80,0,'Excel base,Excel avanzato,Power BI'),(3,'Simona','Ricci','RCCSMN82D52G224P','DIPLOMA_SUPERIORE','S',0,60,0,'Stage orientamento'),(4,'Marco','Testa','TSTMRC90H10L219Q','LAUREA_MAGISTRALE','T',1,40,0,'Python per l\'automazione,Introduzione AI');
/*!40000 ALTER TABLE `docenti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lezione_presenze`
--

DROP TABLE IF EXISTS `lezione_presenze`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lezione_presenze` (
  `lezione_id` int(11) NOT NULL,
  `allievo_id` int(11) NOT NULL,
  PRIMARY KEY (`lezione_id`,`allievo_id`),
  KEY `allievo_id` (`allievo_id`),
  CONSTRAINT `lezione_presenze_ibfk_1` FOREIGN KEY (`lezione_id`) REFERENCES `lezioni` (`id`),
  CONSTRAINT `lezione_presenze_ibfk_2` FOREIGN KEY (`allievo_id`) REFERENCES `allievi` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lezione_presenze`
--

LOCK TABLES `lezione_presenze` WRITE;
/*!40000 ALTER TABLE `lezione_presenze` DISABLE KEYS */;
/*!40000 ALTER TABLE `lezione_presenze` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lezioni`
--

DROP TABLE IF EXISTS `lezioni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lezioni` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `corso_id` int(11) NOT NULL,
  `data` date NOT NULL COMMENT 'Inserita due volte su Sistema Piemonte',
  `ora_inizio` time NOT NULL,
  `ora_fine` time NOT NULL,
  `tipo_lezione` enum('NORMALE','RECUPERO_SOLO_DIDATTICO','RECUPERO_AMMINISTRATIVO_DIDATTICO','FAD') NOT NULL,
  `note` text DEFAULT NULL,
  `si_ripete` tinyint(1) NOT NULL COMMENT 'Se True → al salvataggio viene generata una PrenotazioneMassiva',
  `numero_variazione` int(11) NOT NULL COMMENT 'Contatore incrementale delle modifiche apportate alla lezione',
  PRIMARY KEY (`id`),
  KEY `corso_id` (`corso_id`),
  KEY `ix_lezioni_data` (`data`),
  KEY `ix_lezioni_id` (`id`),
  CONSTRAINT `lezioni_ibfk_1` FOREIGN KEY (`corso_id`) REFERENCES `corsi` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lezioni`
--

LOCK TABLES `lezioni` WRITE;
/*!40000 ALTER TABLE `lezioni` DISABLE KEYS */;
/*!40000 ALTER TABLE `lezioni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prenotazioni`
--

DROP TABLE IF EXISTS `prenotazioni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prenotazioni` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` enum('SINGOLA','MASSIVA') NOT NULL,
  `richiedente_id` int(11) NOT NULL,
  `stato` enum('IN_ATTESA','CONFERMATA','RIFIUTATA','ANNULLATA','CONFLITTO') NOT NULL,
  `google_event_id` varchar(255) DEFAULT NULL,
  `data_creazione` datetime NOT NULL,
  `data_aggiornamento` datetime NOT NULL,
  `ha_conflitti_attivi` tinyint(1) NOT NULL,
  `tipo_ricorrenza` enum('GIORNALIERA','SETTIMANALE','BISETTIMANALE','MENSILE') DEFAULT NULL,
  `giorni_settimana` varchar(20) DEFAULT NULL COMMENT 'Es: ''1,3,5'' per Lun/Mer/Ven',
  `data_inizio_range` date DEFAULT NULL,
  `data_fine_range` date DEFAULT NULL,
  `intervallo` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `richiedente_id` (`richiedente_id`),
  KEY `ix_prenotazioni_id` (`id`),
  CONSTRAINT `prenotazioni_ibfk_3` FOREIGN KEY (`richiedente_id`) REFERENCES `utenti` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=393 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prenotazioni`
--

LOCK TABLES `prenotazioni` WRITE;
/*!40000 ALTER TABLE `prenotazioni` DISABLE KEYS */;
INSERT INTO `prenotazioni` VALUES (196,'MASSIVA',16,'CONFERMATA',NULL,'2026-03-16 16:35:18','2026-03-23 16:49:03',0,'SETTIMANALE','2,3','2026-03-26','2026-03-29',1),(199,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-18 11:42:52','2026-03-23 16:49:03',0,NULL,NULL,NULL,NULL,1),(227,'SINGOLA',8,'CONFERMATA',NULL,'2026-03-20 08:16:53','2026-03-23 16:49:03',0,NULL,NULL,NULL,NULL,1),(228,'MASSIVA',8,'CONFERMATA',NULL,'2026-03-20 08:17:28','2026-03-27 13:13:43',0,'SETTIMANALE','1,3,4','2026-03-27','2026-04-30',1),(233,'SINGOLA',8,'CONFERMATA',NULL,'2026-03-20 09:15:17','2026-03-23 16:49:03',0,NULL,NULL,NULL,NULL,1),(237,'MASSIVA',8,'CONFERMATA',NULL,'2026-03-20 11:18:20','2026-03-23 16:49:03',0,'SETTIMANALE','1,3,5','2026-03-27','2026-04-30',1),(248,'MASSIVA',8,'CONFERMATA',NULL,'2026-03-20 13:24:11','2026-03-26 10:02:41',0,'SETTIMANALE','1,3,4','2026-03-27','2026-08-21',1),(249,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-20 15:44:23','2026-03-23 16:49:03',0,NULL,NULL,NULL,NULL,1),(252,'SINGOLA',7,'CONFERMATA',NULL,'2026-03-20 15:56:16','2026-03-23 16:49:03',0,NULL,NULL,NULL,NULL,1),(257,'MASSIVA',18,'CONFERMATA',NULL,'2026-03-23 09:20:41','2026-03-23 16:49:03',0,'SETTIMANALE','3','2026-03-26','2026-03-26',1),(258,'MASSIVA',18,'CONFERMATA',NULL,'2026-03-23 09:28:06','2026-03-23 16:49:03',0,'SETTIMANALE','1','2026-03-26','2026-03-26',1),(264,'SINGOLA',8,'CONFERMATA',NULL,'2026-03-23 09:48:11','2026-03-23 16:49:03',0,NULL,NULL,NULL,NULL,1),(265,'MASSIVA',8,'CONFERMATA',NULL,'2026-03-23 09:48:33','2026-03-28 12:38:42',0,'SETTIMANALE','1,3','2026-03-23','2026-05-25',1),(270,'MASSIVA',7,'CONFERMATA',NULL,'2026-03-23 11:30:54','2026-03-25 09:04:32',0,'GIORNALIERA','1,2,3,4,5','2026-04-01','2026-04-30',1),(272,'MASSIVA',7,'CONFERMATA',NULL,'2026-03-23 11:34:26','2026-03-23 16:49:03',0,'BISETTIMANALE','2,3','2026-04-01','2026-04-30',1),(274,'SINGOLA',7,'CONFERMATA',NULL,'2026-03-23 14:40:56','2026-03-23 16:49:03',0,NULL,NULL,NULL,NULL,1),(279,'MASSIVA',7,'CONFERMATA',NULL,'2026-03-24 10:32:54','2026-03-26 14:42:47',1,'BISETTIMANALE','3,4','2026-03-24','2026-04-30',1),(280,'MASSIVA',7,'CONFERMATA',NULL,'2026-03-24 10:33:19','2026-03-24 10:33:19',0,'MENSILE','4,5','2026-04-01','2026-04-30',1),(281,'MASSIVA',7,'CONFERMATA',NULL,'2026-03-24 10:34:24','2026-03-24 10:34:24',0,'MENSILE','','2026-09-01','2026-09-30',1),(299,'MASSIVA',19,'CONFERMATA',NULL,'2026-03-24 15:54:00','2026-03-25 09:04:27',0,'SETTIMANALE','3,5','2026-03-25','2026-04-18',1),(303,'SINGOLA',7,'CONFERMATA',NULL,'2026-03-24 16:04:42','2026-03-24 16:04:42',0,NULL,NULL,NULL,NULL,1),(309,'MASSIVA',18,'CONFERMATA',NULL,'2026-03-24 16:19:40','2026-03-24 16:19:40',0,'SETTIMANALE','4,5','2026-04-01','2026-04-30',1),(310,'SINGOLA',18,'CONFERMATA',NULL,'2026-03-24 16:20:10','2026-03-24 16:20:10',0,NULL,NULL,NULL,NULL,1),(311,'SINGOLA',20,'CONFERMATA',NULL,'2026-03-25 08:26:18','2026-03-25 08:26:18',0,NULL,NULL,NULL,NULL,1),(312,'MASSIVA',20,'CONFERMATA',NULL,'2026-03-25 08:28:35','2026-03-25 09:04:32',0,'SETTIMANALE','2','2026-03-26','2026-04-30',1),(315,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-25 09:02:27','2026-03-26 09:43:56',1,NULL,NULL,NULL,NULL,1),(317,'MASSIVA',1,'CONFERMATA',NULL,'2026-03-25 10:39:58','2026-03-25 10:39:58',0,'SETTIMANALE','2','2026-04-01','2026-06-30',1),(319,'SINGOLA',18,'CONFERMATA',NULL,'2026-03-26 08:03:27','2026-03-26 08:03:27',0,NULL,NULL,NULL,NULL,1),(321,'SINGOLA',18,'CONFERMATA',NULL,'2026-03-26 08:05:23','2026-03-26 14:50:57',0,NULL,NULL,NULL,NULL,1),(323,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-26 09:56:09','2026-03-26 09:56:09',1,NULL,NULL,NULL,NULL,1),(324,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 10:59:39','2026-03-26 10:59:39',0,NULL,NULL,NULL,NULL,1),(325,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:00:09','2026-03-26 11:00:09',0,NULL,NULL,NULL,NULL,1),(326,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:00:32','2026-03-26 11:00:32',0,NULL,NULL,NULL,NULL,1),(327,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:01:12','2026-03-26 11:01:12',0,NULL,NULL,NULL,NULL,1),(328,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:01:24','2026-03-26 11:01:24',0,NULL,NULL,NULL,NULL,1),(330,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:03:18','2026-03-26 11:03:18',0,NULL,NULL,NULL,NULL,1),(331,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:06:10','2026-03-26 11:06:10',1,NULL,NULL,NULL,NULL,1),(332,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:08:30','2026-03-26 11:08:30',0,NULL,NULL,NULL,NULL,1),(333,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:09:02','2026-03-26 11:09:02',0,NULL,NULL,NULL,NULL,1),(334,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:09:24','2026-03-26 11:09:24',0,NULL,NULL,NULL,NULL,1),(335,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:12:52','2026-03-26 11:12:52',0,'SETTIMANALE','3,4,5','2026-04-02','2026-04-30',1),(336,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:13:02','2026-03-26 11:13:02',0,'SETTIMANALE','3,4','2026-04-02','2026-04-30',1),(337,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:13:08','2026-03-26 11:13:08',0,'SETTIMANALE','5','2026-04-02','2026-04-30',1),(338,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:13:57','2026-03-26 11:13:57',0,'SETTIMANALE','3,4,5','2026-04-02','2026-04-30',1),(339,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:14:04','2026-03-26 11:47:27',0,'SETTIMANALE','4,5','2026-04-02','2026-04-30',1),(340,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:14:09','2026-03-26 11:14:09',1,'SETTIMANALE','5','2026-04-02','2026-04-30',1),(341,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:14:59','2026-03-26 11:14:59',0,'SETTIMANALE','2','2026-04-02','2026-04-21',1),(342,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:15:47','2026-03-26 11:15:47',0,'SETTIMANALE','4','2026-04-02','2026-04-16',1),(343,'MASSIVA',3,'CONFERMATA',NULL,'2026-03-26 11:15:59','2026-03-26 11:15:59',0,'SETTIMANALE','4','2026-04-02','2026-04-16',1),(344,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:16:25','2026-03-26 11:16:25',0,NULL,NULL,NULL,NULL,1),(345,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:17:49','2026-03-26 11:17:49',0,NULL,NULL,NULL,NULL,1),(346,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:18:09','2026-03-26 11:18:09',0,NULL,NULL,NULL,NULL,1),(347,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:18:26','2026-03-26 11:18:26',0,NULL,NULL,NULL,NULL,1),(348,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 11:52:35','2026-03-26 11:52:35',0,NULL,NULL,NULL,NULL,1),(358,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-26 14:56:54','2026-03-26 14:56:54',1,NULL,NULL,NULL,NULL,1),(359,'SINGOLA',7,'CONFERMATA',NULL,'2026-03-26 15:19:25','2026-03-26 15:19:25',1,NULL,NULL,NULL,NULL,1),(366,'SINGOLA',7,'CONFERMATA',NULL,'2026-03-26 15:54:10','2026-03-26 15:54:18',0,NULL,NULL,NULL,NULL,1),(370,'SINGOLA',8,'CONFERMATA',NULL,'2026-03-27 13:10:47','2026-03-27 13:10:47',0,NULL,NULL,NULL,NULL,1),(371,'MASSIVA',8,'CONFERMATA',NULL,'2026-03-27 13:11:14','2026-03-27 13:11:15',1,'SETTIMANALE','1,3,4','2026-03-30','2026-05-25',1),(372,'SINGOLA',3,'CONFERMATA',NULL,'2026-03-27 13:40:52','2026-03-27 13:40:52',0,NULL,NULL,NULL,NULL,1),(379,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-27 14:56:02','2026-03-27 14:56:02',0,NULL,NULL,NULL,NULL,1),(383,'MASSIVA',9,'CONFERMATA',NULL,'2026-03-28 12:37:11','2026-03-28 12:37:41',0,'SETTIMANALE','3,4','2026-04-01','2026-04-30',1),(384,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-28 12:45:30','2026-03-28 12:45:30',0,NULL,NULL,NULL,NULL,1),(385,'MASSIVA',9,'CONFERMATA',NULL,'2026-03-28 14:42:34','2026-03-28 14:42:34',0,'BISETTIMANALE','3,5','2026-03-30','2026-04-30',1),(386,'MASSIVA',9,'CONFERMATA',NULL,'2026-03-28 14:43:45','2026-03-28 14:43:45',0,'SETTIMANALE','2,3,5','2026-03-30','2026-03-30',1),(387,'MASSIVA',9,'CONFERMATA',NULL,'2026-03-28 14:46:06','2026-03-28 14:46:06',0,'SETTIMANALE','2,3,4,5','2026-04-01','2026-04-30',1),(388,'MASSIVA',22,'CONFERMATA',NULL,'2026-03-28 14:59:32','2026-03-28 14:59:32',1,'SETTIMANALE','2,4','2026-04-01','2026-04-30',1),(391,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-29 16:42:15','2026-03-29 16:42:15',0,NULL,NULL,NULL,NULL,1),(392,'SINGOLA',9,'CONFERMATA',NULL,'2026-03-29 16:43:00','2026-03-29 16:43:43',0,NULL,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `prenotazioni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `richieste_attrezzatura`
--

DROP TABLE IF EXISTS `richieste_attrezzatura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `richieste_attrezzatura` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prenotazione_id` int(11) NOT NULL,
  `attrezzatura_id` int(11) NOT NULL,
  `quantita` int(11) NOT NULL,
  `stato` enum('INVIATA','IN_REVISIONE','APPROVATA','RIFIUTATA') NOT NULL,
  `note` text DEFAULT NULL,
  `data_richiesta` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prenotazione_id` (`prenotazione_id`),
  KEY `attrezzatura_id` (`attrezzatura_id`),
  KEY `ix_richieste_attrezzatura_id` (`id`),
  CONSTRAINT `richieste_attrezzatura_ibfk_1` FOREIGN KEY (`prenotazione_id`) REFERENCES `prenotazioni` (`id`),
  CONSTRAINT `richieste_attrezzatura_ibfk_2` FOREIGN KEY (`attrezzatura_id`) REFERENCES `attrezzature` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `richieste_attrezzatura`
--

LOCK TABLES `richieste_attrezzatura` WRITE;
/*!40000 ALTER TABLE `richieste_attrezzatura` DISABLE KEYS */;
/*!40000 ALTER TABLE `richieste_attrezzatura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `richieste_prenotazione`
--

DROP TABLE IF EXISTS `richieste_prenotazione`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `richieste_prenotazione` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prenotazione_id` int(11) NOT NULL,
  `segreteria_id` int(11) DEFAULT NULL COMMENT 'Segreteria che ha gestito la richiesta',
  `stato` enum('INVIATA','IN_REVISIONE','APPROVATA','RIFIUTATA') NOT NULL,
  `data_richiesta` datetime NOT NULL,
  `data_gestione` datetime DEFAULT NULL,
  `note_rifiuto` text DEFAULT NULL,
  `ha_conflitti` tinyint(1) DEFAULT NULL COMMENT 'True se esistono conflitti rilevati al momento della richiesta',
  PRIMARY KEY (`id`),
  UNIQUE KEY `prenotazione_id` (`prenotazione_id`),
  KEY `segreteria_id` (`segreteria_id`),
  KEY `ix_richieste_prenotazione_id` (`id`),
  CONSTRAINT `richieste_prenotazione_ibfk_1` FOREIGN KEY (`prenotazione_id`) REFERENCES `prenotazioni` (`id`),
  CONSTRAINT `richieste_prenotazione_ibfk_2` FOREIGN KEY (`segreteria_id`) REFERENCES `utenti` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=320 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `richieste_prenotazione`
--

LOCK TABLES `richieste_prenotazione` WRITE;
/*!40000 ALTER TABLE `richieste_prenotazione` DISABLE KEYS */;
INSERT INTO `richieste_prenotazione` VALUES (136,196,NULL,'APPROVATA','2026-03-16 16:35:18','2026-03-16 16:35:18',NULL,0),(139,199,NULL,'APPROVATA','2026-03-18 11:42:52','2026-03-18 11:42:52',NULL,0),(167,227,NULL,'APPROVATA','2026-03-20 08:16:53','2026-03-20 08:16:53',NULL,0),(168,228,NULL,'APPROVATA','2026-03-20 08:17:28','2026-03-20 08:17:28',NULL,0),(172,233,NULL,'APPROVATA','2026-03-20 09:15:17','2026-03-20 09:15:17',NULL,0),(176,237,NULL,'APPROVATA','2026-03-20 11:18:20','2026-03-20 11:18:20',NULL,0),(187,248,NULL,'APPROVATA','2026-03-20 13:24:11','2026-03-20 13:24:11',NULL,0),(188,249,NULL,'APPROVATA','2026-03-20 15:44:23','2026-03-20 15:44:23',NULL,0),(191,252,NULL,'APPROVATA','2026-03-20 15:56:16','2026-03-20 15:56:16',NULL,0),(194,257,NULL,'APPROVATA','2026-03-23 09:20:41','2026-03-23 09:20:41',NULL,0),(195,258,NULL,'APPROVATA','2026-03-23 09:28:06','2026-03-23 09:28:06',NULL,0),(198,264,NULL,'APPROVATA','2026-03-23 09:48:11','2026-03-23 09:48:11',NULL,0),(199,265,NULL,'APPROVATA','2026-03-23 09:48:33','2026-03-23 09:48:33',NULL,0),(201,270,NULL,'APPROVATA','2026-03-23 11:30:54','2026-03-23 11:30:54',NULL,0),(202,272,NULL,'APPROVATA','2026-03-23 11:34:26','2026-03-23 11:34:26',NULL,0),(203,274,NULL,'APPROVATA','2026-03-23 14:40:56','2026-03-23 14:40:56',NULL,0),(208,279,NULL,'APPROVATA','2026-03-24 10:32:54','2026-03-24 10:32:54',NULL,0),(209,280,NULL,'APPROVATA','2026-03-24 10:33:19','2026-03-24 10:33:19',NULL,0),(210,281,NULL,'APPROVATA','2026-03-24 10:34:24','2026-03-24 10:34:24',NULL,0),(227,299,NULL,'APPROVATA','2026-03-24 15:54:00','2026-03-24 15:54:00',NULL,0),(231,303,NULL,'APPROVATA','2026-03-24 16:04:42','2026-03-24 16:04:42',NULL,0),(237,309,NULL,'APPROVATA','2026-03-24 16:19:40','2026-03-24 16:19:40',NULL,0),(238,310,NULL,'APPROVATA','2026-03-24 16:20:10','2026-03-24 16:20:10',NULL,0),(239,311,NULL,'APPROVATA','2026-03-25 08:26:18','2026-03-25 08:26:18',NULL,0),(240,312,NULL,'APPROVATA','2026-03-25 08:28:35','2026-03-25 08:28:35',NULL,0),(243,315,NULL,'APPROVATA','2026-03-25 09:02:27','2026-03-25 09:02:27',NULL,0),(245,317,NULL,'APPROVATA','2026-03-25 10:39:58','2026-03-25 10:39:58',NULL,0),(247,319,NULL,'APPROVATA','2026-03-26 08:03:27','2026-03-26 08:03:27',NULL,0),(249,321,NULL,'APPROVATA','2026-03-26 08:05:23','2026-03-26 08:05:23',NULL,0),(251,323,NULL,'APPROVATA','2026-03-26 09:56:09','2026-03-26 09:56:09',NULL,1),(252,324,NULL,'APPROVATA','2026-03-26 10:59:39','2026-03-26 10:59:39',NULL,0),(253,325,NULL,'APPROVATA','2026-03-26 11:00:09','2026-03-26 11:00:09',NULL,0),(254,326,NULL,'APPROVATA','2026-03-26 11:00:32','2026-03-26 11:00:32',NULL,0),(255,327,NULL,'APPROVATA','2026-03-26 11:01:12','2026-03-26 11:01:12',NULL,0),(256,328,NULL,'APPROVATA','2026-03-26 11:01:25','2026-03-26 11:01:25',NULL,0),(257,330,NULL,'APPROVATA','2026-03-26 11:03:18','2026-03-26 11:03:18',NULL,0),(258,331,NULL,'APPROVATA','2026-03-26 11:06:10','2026-03-26 11:06:10',NULL,0),(259,332,NULL,'APPROVATA','2026-03-26 11:08:30','2026-03-26 11:08:30',NULL,0),(260,333,NULL,'APPROVATA','2026-03-26 11:09:02','2026-03-26 11:09:02',NULL,0),(261,334,NULL,'APPROVATA','2026-03-26 11:09:24','2026-03-26 11:09:24',NULL,0),(262,335,NULL,'APPROVATA','2026-03-26 11:12:52','2026-03-26 11:12:52',NULL,0),(263,336,NULL,'APPROVATA','2026-03-26 11:13:02','2026-03-26 11:13:02',NULL,0),(264,337,NULL,'APPROVATA','2026-03-26 11:13:08','2026-03-26 11:13:08',NULL,0),(265,338,NULL,'APPROVATA','2026-03-26 11:13:58','2026-03-26 11:13:58',NULL,0),(266,339,NULL,'APPROVATA','2026-03-26 11:14:04','2026-03-26 11:14:04',NULL,0),(267,340,NULL,'APPROVATA','2026-03-26 11:14:09','2026-03-26 11:14:09',NULL,0),(268,341,NULL,'APPROVATA','2026-03-26 11:14:59','2026-03-26 11:14:59',NULL,0),(269,342,NULL,'APPROVATA','2026-03-26 11:15:47','2026-03-26 11:15:47',NULL,0),(270,343,NULL,'APPROVATA','2026-03-26 11:15:59','2026-03-26 11:15:59',NULL,0),(271,344,NULL,'APPROVATA','2026-03-26 11:16:25','2026-03-26 11:16:25',NULL,0),(272,345,NULL,'APPROVATA','2026-03-26 11:17:49','2026-03-26 11:17:49',NULL,0),(273,346,NULL,'APPROVATA','2026-03-26 11:18:09','2026-03-26 11:18:09',NULL,0),(274,347,NULL,'APPROVATA','2026-03-26 11:18:26','2026-03-26 11:18:26',NULL,0),(275,348,NULL,'APPROVATA','2026-03-26 11:52:35','2026-03-26 11:52:35',NULL,0),(285,358,NULL,'APPROVATA','2026-03-26 14:56:54','2026-03-26 14:56:54',NULL,1),(286,359,NULL,'APPROVATA','2026-03-26 15:19:25','2026-03-26 15:19:25',NULL,1),(293,366,NULL,'APPROVATA','2026-03-26 15:54:10','2026-03-26 15:54:10',NULL,0),(297,370,NULL,'APPROVATA','2026-03-27 13:10:47','2026-03-27 13:10:47',NULL,0),(298,371,NULL,'APPROVATA','2026-03-27 13:11:15','2026-03-27 13:11:15',NULL,0),(299,372,NULL,'APPROVATA','2026-03-27 13:40:52','2026-03-27 13:40:52',NULL,0),(306,379,NULL,'APPROVATA','2026-03-27 14:56:02','2026-03-27 14:56:02',NULL,0),(310,383,NULL,'APPROVATA','2026-03-28 12:37:12','2026-03-28 12:37:12',NULL,0),(311,384,NULL,'APPROVATA','2026-03-28 12:45:30','2026-03-28 12:45:30',NULL,0),(312,385,NULL,'APPROVATA','2026-03-28 14:42:34','2026-03-28 14:42:34',NULL,0),(313,386,NULL,'APPROVATA','2026-03-28 14:43:45','2026-03-28 14:43:45',NULL,0),(314,387,NULL,'APPROVATA','2026-03-28 14:46:06','2026-03-28 14:46:06',NULL,0),(315,388,NULL,'APPROVATA','2026-03-28 14:59:32','2026-03-28 14:59:32',NULL,0),(318,391,NULL,'APPROVATA','2026-03-29 16:42:15','2026-03-29 16:42:15',NULL,0),(319,392,NULL,'APPROVATA','2026-03-29 16:43:00','2026-03-29 16:43:00',NULL,0);
/*!40000 ALTER TABLE `richieste_prenotazione` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sedi`
--

DROP TABLE IF EXISTS `sedi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sedi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(150) NOT NULL,
  `indirizzo` varchar(255) NOT NULL,
  `citta` varchar(100) NOT NULL,
  `capienza_massima` int(11) NOT NULL COMMENT 'Numero massimo di persone contemporaneamente presenti in sede',
  `attiva` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_sedi_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sedi`
--

LOCK TABLES `sedi` WRITE;
/*!40000 ALTER TABLE `sedi` DISABLE KEYS */;
INSERT INTO `sedi` VALUES (2,'Sede Livorno 53','Via Livorno 53','Torino',69,1),(3,'Sede Svizzera','C.so Svizzera 161','Torino',99,1),(4,'Sede Cuneo','Via Cascina Colombaro 26/D','Cuneo',41,1),(5,'Sede Asti','Piazza Roma 13','Asti',56,1),(6,'Sede Novara','Via Porzio Giovanola 7','Novara',95,1),(7,'Sede Biella','Strada Campagnè 7/A','Biella',96,1),(9,'Sede Livorno 49','Via Livorno 49','Torino',34,1);
/*!40000 ALTER TABLE `sedi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `slot_orari`
--

DROP TABLE IF EXISTS `slot_orari`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `slot_orari` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prenotazione_id` int(11) NOT NULL,
  `aula_id` int(11) NOT NULL,
  `corso_id` int(11) NOT NULL,
  `note` text DEFAULT NULL,
  `data` date NOT NULL,
  `ora_inizio` time NOT NULL,
  `ora_fine` time NOT NULL,
  `annullato` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prenotazione_id` (`prenotazione_id`),
  KEY `ix_slot_orari_id` (`id`),
  KEY `ix_slot_orari_data` (`data`),
  KEY `fk_slot_aula` (`aula_id`),
  KEY `fk_slot_corso` (`corso_id`),
  CONSTRAINT `fk_slot_aula` FOREIGN KEY (`aula_id`) REFERENCES `aule` (`id`),
  CONSTRAINT `fk_slot_corso` FOREIGN KEY (`corso_id`) REFERENCES `corsi` (`id`),
  CONSTRAINT `slot_orari_ibfk_1` FOREIGN KEY (`prenotazione_id`) REFERENCES `prenotazioni` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=894 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slot_orari`
--

LOCK TABLES `slot_orari` WRITE;
/*!40000 ALTER TABLE `slot_orari` DISABLE KEYS */;
INSERT INTO `slot_orari` VALUES (407,199,9,3,NULL,'2026-03-18','08:00:00','13:00:00',0),(444,227,4,1,'PC','2026-03-27','09:00:00','13:00:00',0),(445,228,3,1,'PC','2026-03-30','09:00:00','11:30:00',1),(446,228,5,1,'PC','2026-04-01','09:00:00','13:00:00',0),(447,228,5,1,'PC','2026-04-02','09:00:00','13:00:00',0),(448,228,3,1,'PC','2026-04-06','09:00:00','13:00:00',1),(449,228,3,1,'PC','2026-04-08','09:00:00','13:00:00',1),(450,228,3,1,'PC','2026-04-09','09:00:00','13:00:00',1),(451,228,3,1,'PC','2026-04-13','09:00:00','13:00:00',1),(452,228,3,1,'PC','2026-04-15','09:00:00','13:00:00',1),(453,228,3,1,'PC','2026-04-16','09:00:00','13:00:00',1),(454,228,3,1,'PC','2026-04-20','09:00:00','13:00:00',1),(455,228,3,1,'PC','2026-04-22','09:00:00','13:00:00',1),(456,228,3,1,'PC','2026-04-23','09:00:00','13:00:00',1),(457,228,3,1,'PC','2026-04-27','09:00:00','13:00:00',1),(458,228,3,1,'PC','2026-04-29','09:00:00','13:00:00',1),(459,228,7,1,'PC','2026-04-30','09:00:00','13:00:00',0),(464,233,10,3,NULL,'2026-03-30','09:00:00','13:00:00',0),(468,237,2,1,'PC','2026-03-27','14:00:00','18:00:00',0),(469,237,2,1,'PC','2026-03-30','14:00:00','18:00:00',0),(470,237,2,1,'PC','2026-04-01','14:00:00','18:00:00',0),(471,237,2,1,'PC','2026-04-03','14:00:00','18:00:00',0),(472,237,2,1,'PC','2026-04-06','14:00:00','18:00:00',0),(473,237,2,1,'PC','2026-04-08','14:00:00','18:00:00',0),(474,237,2,1,'PC','2026-04-10','14:00:00','18:00:00',0),(475,237,2,1,'PC','2026-04-13','14:00:00','18:00:00',0),(476,237,2,1,'PC','2026-04-15','14:00:00','18:00:00',0),(477,237,2,1,'PC','2026-04-17','14:00:00','18:00:00',0),(478,237,2,1,'PC','2026-04-20','14:00:00','18:00:00',0),(479,237,2,1,'PC','2026-04-22','14:00:00','18:00:00',0),(480,237,2,1,'PC','2026-04-24','14:00:00','18:00:00',0),(481,237,2,1,'PC','2026-04-27','14:00:00','18:00:00',0),(482,237,2,1,'PC','2026-04-29','14:00:00','18:00:00',0),(493,248,1,1,NULL,'2026-03-30','09:00:00','13:00:00',0),(494,248,1,1,NULL,'2026-04-01','09:00:00','13:00:00',1),(495,248,1,1,NULL,'2026-04-02','09:00:00','13:00:00',0),(496,248,1,1,NULL,'2026-04-06','09:00:00','13:00:00',0),(497,248,1,1,NULL,'2026-04-08','09:00:00','13:00:00',1),(498,248,1,1,NULL,'2026-04-09','09:00:00','13:00:00',0),(499,248,1,1,NULL,'2026-04-13','09:00:00','13:00:00',0),(500,248,1,1,NULL,'2026-04-15','09:00:00','13:00:00',1),(501,248,1,1,NULL,'2026-04-16','09:00:00','13:00:00',0),(502,248,1,1,NULL,'2026-04-20','09:00:00','13:00:00',0),(503,248,1,1,NULL,'2026-04-22','09:00:00','13:00:00',0),(504,248,1,1,NULL,'2026-04-23','09:00:00','13:00:00',0),(505,248,1,1,NULL,'2026-04-27','09:00:00','13:00:00',0),(506,248,1,1,NULL,'2026-04-29','09:00:00','13:00:00',0),(507,248,1,1,NULL,'2026-04-30','09:00:00','13:00:00',0),(508,248,1,1,NULL,'2026-05-04','09:00:00','13:00:00',0),(509,248,1,1,NULL,'2026-05-06','09:00:00','13:00:00',0),(510,248,1,1,NULL,'2026-05-07','09:00:00','13:00:00',0),(511,248,1,1,NULL,'2026-05-11','09:00:00','13:00:00',0),(512,248,1,1,NULL,'2026-05-13','09:00:00','13:00:00',0),(513,248,1,1,NULL,'2026-05-14','09:00:00','13:00:00',0),(514,248,1,1,NULL,'2026-05-18','09:00:00','13:00:00',0),(515,248,1,1,NULL,'2026-05-20','09:00:00','13:00:00',0),(516,248,1,1,NULL,'2026-05-21','09:00:00','13:00:00',0),(517,248,1,1,NULL,'2026-05-25','09:00:00','13:00:00',0),(518,248,1,1,NULL,'2026-05-27','09:00:00','13:00:00',0),(519,248,1,1,NULL,'2026-05-28','09:00:00','13:00:00',0),(520,248,1,1,NULL,'2026-06-01','09:00:00','13:00:00',0),(521,248,1,1,NULL,'2026-06-03','09:00:00','13:00:00',0),(522,248,1,1,NULL,'2026-06-04','09:00:00','13:00:00',0),(523,248,1,1,NULL,'2026-06-08','09:00:00','13:00:00',0),(524,248,1,1,NULL,'2026-06-10','09:00:00','13:00:00',0),(525,248,1,1,NULL,'2026-06-11','09:00:00','13:00:00',0),(526,248,1,1,NULL,'2026-06-15','09:00:00','13:00:00',0),(527,248,1,1,NULL,'2026-06-17','09:00:00','13:00:00',0),(528,248,1,1,NULL,'2026-06-18','09:00:00','13:00:00',0),(529,248,1,1,NULL,'2026-06-22','09:00:00','13:00:00',0),(530,248,1,1,NULL,'2026-06-24','09:00:00','13:00:00',0),(531,248,1,1,NULL,'2026-06-25','09:00:00','13:00:00',0),(532,248,1,1,NULL,'2026-06-29','09:00:00','13:00:00',0),(533,248,1,1,NULL,'2026-07-01','09:00:00','13:00:00',0),(534,248,1,1,NULL,'2026-07-02','09:00:00','13:00:00',0),(535,248,1,1,NULL,'2026-07-06','09:00:00','13:00:00',0),(536,248,1,1,NULL,'2026-07-08','09:00:00','13:00:00',0),(537,248,1,1,NULL,'2026-07-09','09:00:00','13:00:00',0),(538,248,1,1,NULL,'2026-07-13','09:00:00','13:00:00',0),(539,248,1,1,NULL,'2026-07-15','09:00:00','13:00:00',0),(540,248,1,1,NULL,'2026-07-16','09:00:00','13:00:00',0),(541,248,1,1,NULL,'2026-07-20','09:00:00','13:00:00',0),(542,248,1,1,NULL,'2026-07-22','09:00:00','13:00:00',0),(543,248,1,1,NULL,'2026-07-23','09:00:00','13:00:00',0),(544,248,1,1,NULL,'2026-07-27','09:00:00','13:00:00',0),(545,248,1,1,NULL,'2026-07-29','09:00:00','13:00:00',0),(546,248,1,1,NULL,'2026-07-30','09:00:00','13:00:00',0),(547,248,1,1,NULL,'2026-08-03','09:00:00','13:00:00',0),(548,248,1,1,NULL,'2026-08-05','09:00:00','13:00:00',0),(549,248,1,1,NULL,'2026-08-06','09:00:00','13:00:00',0),(550,248,1,1,NULL,'2026-08-10','09:00:00','13:00:00',0),(551,248,1,1,NULL,'2026-08-12','09:00:00','13:00:00',0),(552,248,1,1,NULL,'2026-08-13','09:00:00','13:00:00',0),(553,248,1,1,NULL,'2026-08-17','09:00:00','13:00:00',0),(554,248,1,1,NULL,'2026-08-19','09:00:00','13:00:00',1),(555,248,1,1,NULL,'2026-08-20','09:00:00','13:00:00',0),(556,249,8,3,'qwd','2026-03-20','09:00:00','13:00:00',0),(559,252,11,1,'test','2026-03-23','09:00:00','15:30:00',0),(571,264,10,1,NULL,'2026-04-16','14:00:00','18:00:00',0),(572,265,3,1,NULL,'2026-03-25','09:00:00','13:00:00',1),(574,265,3,1,NULL,'2026-03-30','09:00:00','13:00:00',1),(575,265,3,1,NULL,'2026-04-01','09:00:00','13:00:00',1),(576,265,5,1,NULL,'2026-04-06','09:00:00','13:00:00',0),(577,265,3,1,NULL,'2026-04-08','09:00:00','13:00:00',1),(578,265,3,1,NULL,'2026-04-13','09:00:00','13:00:00',0),(579,265,3,1,NULL,'2026-04-15','09:00:00','13:00:00',0),(580,265,3,1,NULL,'2026-04-20','09:00:00','13:00:00',1),(581,265,3,1,NULL,'2026-04-22','09:00:00','13:00:00',0),(582,265,3,1,NULL,'2026-04-27','09:00:00','13:00:00',1),(583,265,3,1,NULL,'2026-04-29','09:00:00','13:00:00',1),(584,265,3,1,NULL,'2026-05-04','09:00:00','13:00:00',0),(585,265,3,1,NULL,'2026-05-06','09:00:00','13:00:00',1),(586,265,3,1,NULL,'2026-05-11','09:00:00','13:00:00',1),(587,265,3,1,NULL,'2026-05-13','09:00:00','13:00:00',1),(588,265,3,1,NULL,'2026-05-18','09:00:00','13:00:00',0),(589,265,3,1,NULL,'2026-05-20','09:00:00','13:00:00',1),(590,265,3,1,NULL,'2026-05-25','09:00:00','13:00:00',0),(595,270,4,2,NULL,'2026-04-01','09:00:00','13:00:00',0),(596,270,4,2,NULL,'2026-04-02','09:00:00','13:00:00',0),(597,270,4,2,NULL,'2026-04-03','09:00:00','13:00:00',0),(598,270,4,2,NULL,'2026-04-06','09:00:00','13:00:00',0),(599,270,4,2,NULL,'2026-04-07','09:00:00','13:00:00',1),(600,270,4,2,NULL,'2026-04-08','09:00:00','13:00:00',0),(601,270,4,2,NULL,'2026-04-09','09:00:00','13:00:00',0),(602,270,4,2,NULL,'2026-04-10','09:00:00','13:00:00',0),(603,270,4,2,NULL,'2026-04-13','09:00:00','13:00:00',0),(604,270,4,2,NULL,'2026-04-14','09:00:00','13:00:00',1),(605,270,4,2,NULL,'2026-04-15','09:00:00','13:00:00',0),(606,270,4,2,NULL,'2026-04-16','09:00:00','13:00:00',0),(607,270,4,2,NULL,'2026-04-17','09:00:00','13:00:00',0),(608,270,4,2,NULL,'2026-04-20','09:00:00','13:00:00',0),(609,270,4,2,NULL,'2026-04-21','09:00:00','13:00:00',1),(610,270,4,2,NULL,'2026-04-22','09:00:00','13:00:00',0),(611,270,4,2,NULL,'2026-04-23','09:00:00','13:00:00',0),(612,270,4,2,NULL,'2026-04-24','09:00:00','13:00:00',0),(613,270,4,2,NULL,'2026-04-27','09:00:00','13:00:00',0),(614,270,4,2,NULL,'2026-04-28','09:00:00','13:00:00',1),(615,270,4,2,NULL,'2026-04-29','09:00:00','13:00:00',0),(616,270,4,2,NULL,'2026-04-30','09:00:00','13:00:00',0),(618,272,10,1,NULL,'2026-04-01','15:30:00','16:00:00',0),(619,272,10,1,NULL,'2026-04-14','15:30:00','16:00:00',0),(620,272,10,1,NULL,'2026-04-15','15:30:00','16:00:00',0),(621,272,10,1,NULL,'2026-04-28','15:30:00','16:00:00',0),(622,272,10,1,NULL,'2026-04-29','15:30:00','16:00:00',0),(624,274,3,1,'prova','2026-03-24','12:00:00','13:00:00',0),(629,279,4,1,NULL,'2026-03-25','14:30:00','17:30:00',0),(630,279,4,1,NULL,'2026-03-26','07:00:00','08:30:00',0),(631,279,4,1,NULL,'2026-04-08','14:30:00','17:30:00',0),(632,279,4,1,NULL,'2026-04-09','14:30:00','17:30:00',0),(633,279,4,1,NULL,'2026-04-22','14:30:00','17:30:00',0),(634,279,4,1,NULL,'2026-04-23','14:30:00','17:30:00',0),(656,299,1,1,'iovine','2026-03-25','09:00:00','13:00:00',1),(657,299,1,1,'iovine','2026-03-27','09:00:00','13:00:00',1),(658,299,1,1,'iovine','2026-04-01','09:00:00','13:00:00',0),(659,299,1,1,'iovine','2026-04-03','09:00:00','13:00:00',0),(660,299,1,1,'iovine','2026-04-08','09:00:00','13:00:00',1),(661,299,1,1,'iovine','2026-04-10','09:00:00','13:00:00',0),(662,299,1,1,'iovine','2026-04-15','09:00:00','13:00:00',0),(663,299,1,1,'iovine','2026-04-17','09:00:00','13:00:00',0),(667,303,11,1,NULL,'2026-03-27','09:00:00','13:00:00',0),(673,309,2,2,NULL,'2026-04-02','09:00:00','13:00:00',0),(674,309,2,2,NULL,'2026-04-03','09:00:00','13:00:00',0),(675,309,2,2,NULL,'2026-04-09','09:00:00','13:00:00',0),(676,309,2,2,NULL,'2026-04-10','09:00:00','13:00:00',0),(677,309,2,2,NULL,'2026-04-16','09:00:00','13:00:00',0),(678,309,2,2,NULL,'2026-04-17','09:00:00','13:00:00',0),(679,309,2,2,NULL,'2026-04-23','09:00:00','13:00:00',0),(680,309,2,2,NULL,'2026-04-24','09:00:00','13:00:00',0),(681,309,2,2,NULL,'2026-04-30','09:00:00','13:00:00',0),(682,310,1,1,NULL,'2026-05-26','09:00:00','13:00:00',0),(683,311,1,2,'DINARDO - PC','2026-03-26','19:00:00','21:00:00',0),(684,312,4,1,'PIPPO','2026-03-31','09:00:00','13:00:00',0),(685,312,4,1,'PIPPO','2026-04-07','09:00:00','13:00:00',1),(686,312,4,1,'PIPPO','2026-04-14','09:00:00','13:00:00',1),(687,312,4,1,'PIPPO','2026-04-21','09:00:00','13:00:00',0),(688,312,4,1,'PIPPO','2026-04-28','09:00:00','13:00:00',1),(691,315,1,1,'1','2026-03-31','09:00:00','21:00:00',0),(693,317,2,1,'Giorgetti - PC e proiettore','2026-04-07','09:00:00','12:00:00',1),(694,317,2,1,'Giorgetti - PC e proiettore','2026-04-14','09:00:00','12:00:00',0),(695,317,2,1,'Giorgetti - PC e proiettore','2026-04-21','09:00:00','12:00:00',0),(696,317,2,1,'Giorgetti - PC e proiettore','2026-04-28','09:00:00','12:00:00',0),(697,317,2,1,'Giorgetti - PC e proiettore','2026-05-05','09:00:00','12:00:00',0),(698,317,2,1,'Giorgetti - PC e proiettore','2026-05-12','09:00:00','12:00:00',0),(699,317,2,1,'Giorgetti - PC e proiettore','2026-05-19','09:00:00','12:00:00',0),(700,317,2,1,'Giorgetti - PC e proiettore','2026-05-26','09:00:00','12:00:00',0),(701,317,2,1,'Giorgetti - PC e proiettore','2026-06-02','09:00:00','12:00:00',0),(702,317,2,1,'Giorgetti - PC e proiettore','2026-06-09','09:00:00','12:00:00',0),(703,317,2,1,'Giorgetti - PC e proiettore','2026-06-16','09:00:00','12:00:00',0),(704,317,2,1,'Giorgetti - PC e proiettore','2026-06-23','09:00:00','12:00:00',0),(705,317,2,1,'Giorgetti - PC e proiettore','2026-06-30','09:00:00','12:00:00',0),(707,319,1,3,'tè caldo','2026-03-31','09:00:00','13:00:00',0),(709,321,4,3,'io antipatico','2026-03-26','14:30:00','18:30:00',0),(711,323,1,2,'test','2026-04-08','08:30:00','21:00:00',0),(712,324,17,1,'PALMA - PC','2026-04-01','09:00:00','13:00:00',0),(713,325,15,2,NULL,'2026-04-01','09:00:00','13:00:00',0),(714,326,15,2,NULL,'2026-04-01','14:00:00','18:00:00',0),(715,327,16,3,NULL,'2026-04-01','09:00:00','13:00:00',0),(716,328,16,3,NULL,'2026-04-01','14:00:00','18:00:00',0),(718,330,17,1,'BARALE + MIELE - PC','2026-04-01','14:30:00','16:30:00',0),(719,331,14,3,'supervisione','2026-04-01','14:00:00','16:00:00',0),(720,332,27,1,'valdocco','2026-04-01','15:00:00','17:00:00',0),(721,333,28,3,'MANUTENTORE - PRATICA','2026-04-01','08:30:00','12:30:00',0),(722,334,28,1,'MANUTENTORE - PRATICA','2026-04-01','13:00:00','17:00:00',0),(723,335,15,1,NULL,'2026-04-02','09:00:00','13:00:00',0),(724,335,15,1,NULL,'2026-04-03','09:00:00','13:00:00',0),(725,335,15,1,NULL,'2026-04-08','09:00:00','13:00:00',0),(726,335,15,1,NULL,'2026-04-09','09:00:00','13:00:00',0),(727,335,15,1,NULL,'2026-04-10','09:00:00','13:00:00',0),(728,335,15,1,NULL,'2026-04-15','09:00:00','13:00:00',0),(729,335,15,1,NULL,'2026-04-16','09:00:00','13:00:00',0),(730,335,15,1,NULL,'2026-04-17','09:00:00','13:00:00',0),(731,335,15,1,NULL,'2026-04-22','09:00:00','13:00:00',0),(732,335,15,1,NULL,'2026-04-23','09:00:00','13:00:00',0),(733,335,15,1,NULL,'2026-04-24','09:00:00','13:00:00',0),(734,335,15,1,NULL,'2026-04-29','09:00:00','13:00:00',0),(735,335,15,1,NULL,'2026-04-30','09:00:00','13:00:00',0),(736,336,15,1,NULL,'2026-04-02','14:00:00','18:00:00',0),(737,336,15,1,NULL,'2026-04-08','14:00:00','18:00:00',0),(738,336,15,1,NULL,'2026-04-09','14:00:00','18:00:00',0),(739,336,15,1,NULL,'2026-04-15','14:00:00','18:00:00',0),(740,336,15,1,NULL,'2026-04-16','14:00:00','18:00:00',0),(741,336,15,1,NULL,'2026-04-22','14:00:00','18:00:00',0),(742,336,15,1,NULL,'2026-04-23','14:00:00','18:00:00',0),(743,336,15,1,NULL,'2026-04-29','14:00:00','18:00:00',0),(744,336,15,1,NULL,'2026-04-30','14:00:00','18:00:00',0),(745,337,15,1,NULL,'2026-04-03','14:00:00','16:00:00',0),(746,337,15,1,NULL,'2026-04-10','14:00:00','16:00:00',0),(747,337,15,1,NULL,'2026-04-17','14:00:00','16:00:00',0),(748,337,15,1,NULL,'2026-04-24','14:00:00','16:00:00',0),(749,338,16,2,NULL,'2026-04-02','09:00:00','13:00:00',0),(750,338,16,2,NULL,'2026-04-03','09:00:00','13:00:00',0),(751,338,16,2,NULL,'2026-04-08','09:00:00','13:00:00',0),(752,338,16,2,NULL,'2026-04-09','09:00:00','13:00:00',0),(753,338,16,2,NULL,'2026-04-10','09:00:00','13:00:00',0),(754,338,16,2,NULL,'2026-04-15','09:00:00','13:00:00',0),(755,338,16,2,NULL,'2026-04-16','09:00:00','13:00:00',0),(756,338,16,2,NULL,'2026-04-17','09:00:00','13:00:00',0),(757,338,16,2,NULL,'2026-04-22','09:00:00','13:00:00',0),(758,338,16,2,NULL,'2026-04-23','09:00:00','13:00:00',0),(759,338,16,2,NULL,'2026-04-24','09:00:00','13:00:00',0),(760,338,16,2,NULL,'2026-04-29','09:00:00','13:00:00',0),(761,338,16,2,NULL,'2026-04-30','09:00:00','13:00:00',0),(762,339,16,2,NULL,'2026-04-02','14:00:00','18:00:00',0),(763,339,16,2,NULL,'2026-04-03','14:00:00','18:00:00',0),(764,339,16,2,NULL,'2026-04-09','14:00:00','18:00:00',0),(765,339,16,2,NULL,'2026-04-10','14:00:00','18:00:00',0),(766,339,16,2,NULL,'2026-04-16','14:00:00','18:00:00',0),(767,339,16,2,NULL,'2026-04-17','14:00:00','18:00:00',0),(768,339,16,2,NULL,'2026-04-23','14:00:00','18:00:00',0),(769,339,16,2,NULL,'2026-04-24','14:00:00','18:00:00',0),(770,339,16,2,NULL,'2026-04-30','14:00:00','18:00:00',0),(771,340,14,2,NULL,'2026-04-03','14:00:00','16:00:00',0),(772,340,14,2,NULL,'2026-04-10','14:00:00','16:00:00',0),(773,340,14,2,NULL,'2026-04-17','14:00:00','16:00:00',0),(774,340,14,2,NULL,'2026-04-24','14:00:00','16:00:00',0),(775,341,14,3,NULL,'2026-04-07','14:00:00','18:00:00',0),(776,341,14,3,NULL,'2026-04-14','14:00:00','18:00:00',0),(777,341,14,3,NULL,'2026-04-21','14:00:00','18:00:00',0),(778,342,28,3,'MANUTENTORE - PRATICA','2026-04-02','08:30:00','12:30:00',0),(779,342,28,3,'MANUTENTORE - PRATICA','2026-04-09','08:30:00','12:30:00',0),(780,342,28,3,'MANUTENTORE - PRATICA','2026-04-16','08:30:00','12:30:00',0),(781,343,28,3,'MANUTENTORE - PRATICA','2026-04-02','13:30:00','17:30:00',0),(782,343,28,3,'MANUTENTORE - PRATICA','2026-04-09','13:30:00','17:30:00',0),(783,343,28,3,'MANUTENTORE - PRATICA','2026-04-16','13:30:00','17:30:00',0),(784,344,28,3,'MANUTENTORE - PRATICA','2026-04-21','09:00:00','13:00:00',0),(785,345,17,3,'esame manutentore','2026-04-23','09:00:00','10:00:00',0),(786,346,17,2,'studio medico - barale','2026-04-23','10:00:00','13:00:00',0),(787,347,14,1,'studio medico - barale','2026-04-23','09:00:00','10:00:00',0),(788,348,14,2,NULL,'2026-04-04','09:00:00','13:00:00',0),(798,358,14,1,NULL,'2026-03-26','09:00:00','13:00:00',0),(799,359,1,2,NULL,'2026-03-26','09:00:00','13:00:00',0),(806,366,2,1,NULL,'2026-03-26','09:00:00','13:00:00',0),(810,370,1,1,NULL,'2026-04-02','14:00:00','18:00:00',0),(811,371,5,1,NULL,'2026-03-30','09:00:00','13:00:00',0),(812,371,3,1,NULL,'2026-04-01','09:00:00','13:00:00',1),(813,371,3,1,NULL,'2026-04-02','09:00:00','13:00:00',1),(814,371,3,1,NULL,'2026-04-06','09:00:00','13:00:00',1),(815,371,5,1,NULL,'2026-04-08','09:00:00','13:00:00',0),(816,371,5,1,NULL,'2026-04-09','09:00:00','13:00:00',0),(817,371,3,1,NULL,'2026-04-13','09:00:00','13:00:00',1),(818,371,3,1,NULL,'2026-04-15','09:00:00','13:00:00',1),(819,371,3,1,NULL,'2026-04-16','09:00:00','13:00:00',0),(820,371,3,1,NULL,'2026-04-20','09:00:00','13:00:00',0),(821,371,3,1,NULL,'2026-04-22','09:00:00','13:00:00',1),(822,371,3,1,NULL,'2026-04-23','09:00:00','13:00:00',0),(823,371,3,1,NULL,'2026-04-27','09:00:00','13:00:00',0),(824,371,3,1,NULL,'2026-04-29','09:00:00','13:00:00',0),(825,371,3,1,NULL,'2026-04-30','09:00:00','13:00:00',0),(826,371,3,1,NULL,'2026-05-04','09:00:00','13:00:00',1),(827,371,3,1,NULL,'2026-05-06','09:00:00','13:00:00',0),(828,371,3,1,NULL,'2026-05-07','09:00:00','13:00:00',0),(829,371,3,1,NULL,'2026-05-11','09:00:00','13:00:00',0),(830,371,3,1,NULL,'2026-05-13','09:00:00','13:00:00',0),(831,371,3,1,NULL,'2026-05-14','09:00:00','13:00:00',0),(832,371,3,1,NULL,'2026-05-18','09:00:00','13:00:00',1),(833,371,3,1,NULL,'2026-05-20','09:00:00','13:00:00',0),(834,371,3,1,NULL,'2026-05-21','09:00:00','13:00:00',0),(835,371,3,1,NULL,'2026-05-25','09:00:00','13:00:00',1),(836,372,14,1,NULL,'2026-03-27','09:00:00','13:00:00',0),(843,379,1,1,NULL,'2026-03-27','09:00:00','13:00:00',0),(847,383,8,2,'test','2026-04-01','09:00:00','13:00:00',0),(848,383,8,2,'test','2026-04-02','09:00:00','13:00:00',0),(849,383,8,2,'test','2026-04-08','09:00:00','13:00:00',0),(850,383,8,2,'test','2026-04-09','09:00:00','13:00:00',0),(851,383,8,2,'test','2026-04-15','09:00:00','13:00:00',0),(852,383,8,2,'test','2026-04-16','09:00:00','13:00:00',0),(853,383,8,2,'test','2026-04-22','09:00:00','13:00:00',0),(854,383,8,2,'test','2026-04-23','09:00:00','13:00:00',0),(855,383,8,2,'test','2026-04-29','09:00:00','13:00:00',0),(856,383,8,2,'test','2026-04-30','09:00:00','13:00:00',0),(857,384,7,2,'Riunione IMPORTANTISSIMA!','2026-03-28','09:00:00','17:00:00',0),(858,385,7,2,'DOCENTE - Attrezzatura','2026-04-01','09:00:00','13:00:00',0),(859,385,7,2,'DOCENTE - Attrezzatura','2026-04-03','09:00:00','13:00:00',0),(860,385,7,2,'DOCENTE - Attrezzatura','2026-04-15','09:00:00','13:00:00',0),(861,385,7,2,'DOCENTE - Attrezzatura','2026-04-17','09:00:00','13:00:00',0),(862,385,7,2,'DOCENTE - Attrezzatura','2026-04-29','09:00:00','13:00:00',0),(863,387,6,3,NULL,'2026-04-01','09:00:00','16:00:00',0),(864,387,6,3,NULL,'2026-04-02','09:00:00','16:00:00',0),(865,387,6,3,NULL,'2026-04-03','09:00:00','16:00:00',0),(866,387,6,3,NULL,'2026-04-07','09:00:00','16:00:00',0),(867,387,6,3,NULL,'2026-04-08','09:00:00','16:00:00',0),(868,387,6,3,NULL,'2026-04-09','09:00:00','16:00:00',0),(869,387,6,3,NULL,'2026-04-10','09:00:00','16:00:00',0),(870,387,6,3,NULL,'2026-04-14','09:00:00','16:00:00',0),(871,387,6,3,NULL,'2026-04-15','09:00:00','16:00:00',0),(872,387,6,3,NULL,'2026-04-16','09:00:00','16:00:00',0),(873,387,6,3,NULL,'2026-04-17','09:00:00','16:00:00',0),(874,387,6,3,NULL,'2026-04-21','09:00:00','16:00:00',0),(875,387,6,3,NULL,'2026-04-22','09:00:00','16:00:00',0),(876,387,6,3,NULL,'2026-04-23','09:00:00','16:00:00',0),(877,387,6,3,NULL,'2026-04-24','09:00:00','16:00:00',0),(878,387,6,3,NULL,'2026-04-28','09:00:00','16:00:00',0),(879,387,6,3,NULL,'2026-04-29','09:00:00','16:00:00',0),(880,387,6,3,NULL,'2026-04-30','09:00:00','16:00:00',0),(881,388,7,3,'DOCENTE TEST - PC','2026-04-02','09:00:00','13:00:00',0),(882,388,7,3,'DOCENTE TEST - PC','2026-04-07','09:00:00','13:00:00',0),(883,388,7,3,'DOCENTE TEST - PC','2026-04-09','09:00:00','13:00:00',0),(884,388,7,3,'DOCENTE TEST - PC','2026-04-14','09:00:00','13:00:00',0),(885,388,7,3,'DOCENTE TEST - PC','2026-04-16','09:00:00','13:00:00',0),(886,388,7,3,'DOCENTE TEST - PC','2026-04-21','09:00:00','13:00:00',0),(887,388,7,3,'DOCENTE TEST - PC','2026-04-23','09:00:00','13:00:00',0),(888,388,7,3,'DOCENTE TEST - PC','2026-04-28','09:00:00','13:00:00',0),(889,388,5,3,'DOCENTE TEST - PC','2026-04-30','09:00:00','13:00:00',0),(892,391,2,2,'test','2026-04-07','14:00:00','18:00:00',0),(893,392,2,1,'test2','2026-04-07','09:00:00','13:00:00',0);
/*!40000 ALTER TABLE `slot_orari` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utenti`
--

DROP TABLE IF EXISTS `utenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `utenti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `cognome` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `attivo` tinyint(1) DEFAULT NULL,
  `ruolo` varchar(20) NOT NULL,
  `sede_id` int(11) DEFAULT NULL,
  `data_creazione` datetime NOT NULL,
  `ultimo_accesso` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_utenti_email` (`email`),
  KEY `sede_id` (`sede_id`),
  KEY `ix_utenti_id` (`id`),
  CONSTRAINT `utenti_ibfk_1` FOREIGN KEY (`sede_id`) REFERENCES `sedi` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utenti`
--

LOCK TABLES `utenti` WRITE;
/*!40000 ALTER TABLE `utenti` DISABLE KEYS */;
INSERT INTO `utenti` VALUES (1,'Chiara','Giorgetti','giorgetti@inforcoopecipa.it','$2b$12$1J50nAcvEZScKSfJv.L5Juncr7hHgX11uLxLI2HlDGMlgUoZSStka',1,'OPERATIVO',9,'2026-03-04 14:42:37','2026-03-25 10:44:51'),(3,'Valeria','Nagliato','nagliato@inforcoopecipa.it','$2b$12$iack.Lp9HqqJKKki3ZrA1eLUJHvmoO0aImR7vfGvxYGx2O2shorY2',1,'COORDINAMENTO',7,'2026-03-04 14:42:37','2026-03-27 13:40:28'),(7,'Simone','Dardanello','dardanello@inforcoopecipa.it','$2b$12$ph4arhtQNUd0JGj0.GJvQ.M9JbwZlcFJz8EaIKkHNDKElL7XmecyK',1,'COORDINAMENTO',4,'2026-03-04 14:42:37','2026-03-27 15:06:42'),(8,'Stefano','Ramello','ramello@inforcoopecipa.it','$2b$12$YIdhIXZWLRJzYrneGiERY.3lg4OmjGdxuUnmuu70zPl0Nn1cj5bAy',1,'OPERATIVO',3,'2026-03-04 14:42:37','2026-03-28 09:30:49'),(9,'Roberto','Falconi','dev@inforcoopecipa.it','$2b$12$o7GDl7LtdZ2/nG8RMBg5xeCpd/TLVW9.bjqB4sCFpulPx10fRRMEy',1,'COORDINAMENTO',3,'2026-03-04 14:45:27','2026-03-30 08:13:09'),(16,'Rosangela','Colline','colline@inforcoopecipa.it','$2b$12$p6XpiJOvvwm4x5UY9qcv5eh3NxOC/7zLKu/CRCjQpkYhSnAxiwnAa',1,'OPERATIVO',9,'2026-03-11 10:33:11','2026-03-29 16:39:35'),(18,'Stefano','Castello','castello@inforcoopecipa.it','$2b$12$PZjG.qGmd98c8z8XyY9D0eKPw65wM.1C2qq7.vM4.7PSo2C/KqoHC',1,'OPERATIVO',3,'2026-03-20 14:17:10','2026-03-27 11:25:44'),(19,'Margherita','Sciolti','sciolti@inforcoopecipa.it','$2b$12$csZ.IXeJIITbh1oLOswrj.8ypsir4hgLm3ncBvBv4yekESXVi/Ph.',1,'COORDINAMENTO',2,'2026-03-24 09:00:41','2026-03-26 13:09:49'),(20,'Antonietta','Dinardo','dinardo@inforcoopecipa.it','$2b$12$ZU3jmKpifqsZ0Fnsb8mWZucc1Qo5mHpYmWVPoD70XNC8fVP/r7mDq',1,'COORDINAMENTO',NULL,'2026-03-25 08:12:12','2026-03-25 08:19:53'),(22,'Test','Utente','test@inforcoopecipa.it','$2b$12$aqk/kEPr9QzW5rXOrQCut.60JoWzegtWstmyFTS3mbC6hK73RVwuy',1,'OPERATIVO',3,'2026-03-28 12:36:00','2026-03-28 15:14:41'),(23,'test2','test2','test2@inforcoopecipa.it','$2b$12$6GfrB1loqHWDhfx09ukSgOgiavZp9xBQwGo/ox02exMHCw3sgM22C',1,'OPERATIVO',5,'2026-03-28 15:07:41',NULL);
/*!40000 ALTER TABLE `utenti` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-30 12:42:59
