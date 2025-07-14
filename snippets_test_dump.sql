
DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
                           `ID` int(11) NOT NULL AUTO_INCREMENT,
                           `STREET` varchar(128) NOT NULL COMMENT 'Full Street Address including house number',
                           `CODE` varchar(128) DEFAULT NULL COMMENT 'ZIP CODE/POST CODE',
                           `TOWN` varchar(128) DEFAULT NULL,
                           `REGION` varchar(128) DEFAULT NULL COMMENT 'Municipality/State/Prefecture',
                           `tag_id` int(11) DEFAULT NULL,
                           `country_id` smallint(6) DEFAULT NULL,
                           PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `associate_notetag_note`
--

DROP TABLE IF EXISTS `associate_notetag_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `associate_notetag_note` (
                                          `notetag_id` int(11) NOT NULL,
                                          `note_id` int(11) NOT NULL,
                                          PRIMARY KEY (`notetag_id`,`note_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `associate_notetag_note`
--

LOCK TABLES `associate_notetag_note` WRITE;
/*!40000 ALTER TABLE `associate_notetag_note` DISABLE KEYS */;
INSERT INTO `associate_notetag_note` VALUES (113,190),(113,191),(113,192),(114,196),(115,176),(115,184),(115,185),(115,190),(116,177),(116,179),(116,180),(116,181),(116,182),(116,183),(116,184),(116,185),(116,186),(116,187),(116,188),(116,193),(116,194),(116,195),(116,197),(116,198),(116,199),(116,200),(116,201),(116,202),(116,203),(117,177),(117,196),(117,204),(117,205),(117,206),(117,207),(117,208),(117,209),(117,210),(118,189),(119,208),(119,209),(119,210),(123,217),(124,217),(125,217),(125,218),(125,219),(125,220),(125,221),(125,222),(126,218),(127,218),(128,219),(128,220),(128,221),(128,222);
/*!40000 ALTER TABLE `associate_notetag_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `associate_source_author`
--

DROP TABLE IF EXISTS `associate_source_author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `associate_source_author` (
                                           `source_id` int(11) NOT NULL,
                                           `author_id` int(11) NOT NULL,
                                           PRIMARY KEY (`source_id`,`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `associate_source_author`
--

LOCK TABLES `associate_source_author` WRITE;
/*!40000 ALTER TABLE `associate_source_author` DISABLE KEYS */;
INSERT INTO `associate_source_author` VALUES (52,60),(53,61),(54,62),(57,67),(58,68),(59,69),(60,70);
/*!40000 ALTER TABLE `associate_source_author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `associate_source_note`
--

DROP TABLE IF EXISTS `associate_source_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `associate_source_note` (
                                         `source_id` int(11) NOT NULL,
                                         `note_id` int(11) NOT NULL,
                                         PRIMARY KEY (`source_id`,`note_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `associate_source_note`
--

LOCK TABLES `associate_source_note` WRITE;
/*!40000 ALTER TABLE `associate_source_note` DISABLE KEYS */;
INSERT INTO `associate_source_note` VALUES (52,175),(52,176),(52,178),(53,177),(53,179),(53,180),(53,181),(53,182),(53,183),(53,184),(53,185),(53,186),(53,187),(53,188),(53,190),(53,191),(53,192),(53,193),(53,194),(53,195),(53,197),(53,198),(53,199),(53,200),(53,201),(53,202),(53,203),(54,189),(56,204),(56,205),(56,206),(56,207),(56,208),(56,209),(56,210),(56,211),(57,217),(58,218),(59,219),(59,220),(59,221),(59,222);
/*!40000 ALTER TABLE `associate_source_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author` (
                          `id` int(11) NOT NULL AUTO_INCREMENT,
                          `forename` varchar(128) DEFAULT NULL,
                          `surname` varchar(128) DEFAULT NULL,
                          `title` varchar(128) DEFAULT NULL,
                          `middlename` varchar(256) DEFAULT NULL,
                          `postnominal` varchar(32) DEFAULT NULL,
                          `birthyear` varchar(16) DEFAULT NULL,
                          `deathyear` varchar(16) DEFAULT NULL,
                          `full_name` varchar(512) DEFAULT NULL,
                          `comment` varchar(1024) DEFAULT NULL,
                          PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES (60,'Steven','Pinker','','','','','','Steven Pinker','None'),(61,'Chris','Anderson','','','','','','Chris Anderson','None'),(62,'Adam','Kjems','','','','','','Adam Kjems','None'),(63,'Martin','','Mr. ','','M. D. ','','','Martin','None'),(64,NULL,NULL,NULL,NULL,NULL,'1967','-','Zanny Minto Beddoes','Editor in chief af the Economist magazine'),(65,NULL,NULL,NULL,NULL,NULL,'1942','2020','Douglas Walton','A Canadian academic and author, known for his books and papers on argumentation, logical fallacies and informal logic. '),(66,NULL,NULL,NULL,NULL,NULL,'1952','2001','Douglas Adams','writer, hitchhikers guide to the galaxy'),(67,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Liz Cantrell',NULL),(68,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'George T. Doran',NULL),(69,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Naomi S. Baron',NULL),(70,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'RYAN BRODERICK',NULL);
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
                           `id` int(11) NOT NULL AUTO_INCREMENT,
                           `English_name` varchar(512) DEFAULT NULL,
                           `iso_code` varchar(2) DEFAULT NULL,
                           PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genre`
--

DROP TABLE IF EXISTS `genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `genre` (
                         `id` int(11) NOT NULL AUTO_INCREMENT,
                         `genre` varchar(50) DEFAULT NULL,
                         PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genre`
--

LOCK TABLES `genre` WRITE;
/*!40000 ALTER TABLE `genre` DISABLE KEYS */;
/*!40000 ALTER TABLE `genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `note`
--

DROP TABLE IF EXISTS `note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `note` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `content` varchar(4096) DEFAULT NULL,
                        `entry_datetime` datetime DEFAULT NULL,
                        `update_datetime` datetime DEFAULT NULL,
                        `object_type_id` smallint(6) DEFAULT NULL,
                        `temp_source` varchar(512) DEFAULT NULL,
                        `url_source` varchar(512) DEFAULT NULL,
                        PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `note`
--

LOCK TABLES `note` WRITE;
/*!40000 ALTER TABLE `note` DISABLE KEYS */;
INSERT INTO `note` VALUES (175,'language makes community possible','2023-08-22 10:25:56',NULL,NULL,NULL,NULL),(176,'Hunters would cause stampeds to mass kill horses 17.000 years ago','2023-08-22 10:27:57',NULL,NULL,NULL,NULL),(177,'We are nervous when giving speeches because it is about our reputation','2023-08-22 19:26:21',NULL,NULL,NULL,NULL),(178,'# A list\r\n\r\n* point 1\r\n* point 2\r\n\r\nI made a list','2023-08-22 19:28:19',NULL,NULL,NULL,NULL),(179,'\'a talk can still open doors or transform a career\'','2023-08-23 15:17:55',NULL,NULL,NULL,NULL),(180,'giving a speech is mix a skills resulting in a wide variety of speeches that can be given. Speakers can choose their own style for sucess','2023-08-23 15:21:17',NULL,NULL,NULL,NULL),(181,'frame the story and have a natural narrative sequence','2023-08-23 15:22:30',NULL,NULL,NULL,NULL),(182,'Be yourself during the speech, that\'s the poin','2023-08-23 15:23:16',NULL,NULL,NULL,NULL),(183,'\'Presentation literacy\' can be used for speeches to large/small audiences or a camera and the internet','2023-08-23 15:24:12',NULL,NULL,NULL,NULL),(184,'laughter is \'social stress in pleasurable alignment\' ','2023-08-23 15:27:01',NULL,NULL,NULL,NULL),(185,'The point of a speech is to put your idea inside the mind of the listener','2023-08-23 15:27:27',NULL,NULL,NULL,NULL),(186,'topic of a talk doesn\'t need to be a new idea, retelling an old story in a new way also has values, for example religious sermons repeat the same stories','2023-08-23 15:30:48',NULL,NULL,NULL,NULL),(187,'Find the idea you want to spread to others and make that the speech topic','2023-08-23 15:31:13',NULL,NULL,NULL,NULL),(188,'You can use a talk as the starting point to deeper research on a topic. The speech flow can be in the same order you looked for and asked questions during the research phase','2023-08-23 15:32:12',NULL,NULL,NULL,NULL),(189,'Describe idea I want to share with others for snippets','2023-08-23 15:35:20',NULL,NULL,NULL,NULL),(190,'language only works if shared by speaker and listener','2023-08-23 15:36:35',NULL,NULL,NULL,NULL),(191,'Dr Uri Hasson in a 2015 experiment at Prince University used fMRI to demonstrate that the mental experince of watching a movie, could be replicated in particpates who only recieved an audio description of the movie. ','2023-08-23 15:38:56',NULL,NULL,NULL,NULL),(192,'Albert Mehrabian 1967 results are often misinterepreted. That only 7% of what comes across in communication is due to language. The study looked at emotion. ','2023-08-23 15:44:06',NULL,NULL,NULL,NULL),(193,'A useful metaphor for a speech is a journey, where the speaker and audience start in the same place and the speaker is a tour guide taking the audience somewhere new. ','2023-08-23 15:46:26',NULL,NULL,NULL,NULL),(194,'4 speech types to avoid\r\n\r\n1. The sales pitch\r\n2. The ramble\r\n3. The org bore\r\n4. The inspiration performance','2023-08-23 15:47:31',NULL,NULL,NULL,NULL),(195,'The goal of any speech should be to give to the audience. ','2023-08-23 15:50:12',NULL,NULL,NULL,NULL),(196,'Hejaz ','2023-08-23 16:32:47',NULL,NULL,NULL,NULL),(197,'People give there time by listeninger, therefore prepare a speech with a takeaway','2023-08-23 17:19:18',NULL,NULL,NULL,NULL),(198,'Don\'t make speeches self serving, instead provide a story, an idea, a gift. ','2023-08-23 17:20:38',NULL,NULL,NULL,NULL),(199,'An inspirational talk needs substance, not just style. Therefore dream about something bigger than yourself and share that vision. ','2023-08-23 17:23:38',NULL,NULL,NULL,NULL),(200,'An inspirational talk needs substance, not just style. Therefore dream about something bigger than yourself and share that vision. ','2023-08-24 05:41:41',NULL,NULL,NULL,NULL),(201,'A throughline, connects each part of a speech creating single narrative arc','2023-08-24 05:44:15',NULL,NULL,NULL,NULL),(202,'As an excerise, state your throughline as a 15 sentence statement','2023-08-24 05:45:38',NULL,NULL,NULL,NULL),(203,'In creating a throughline, first step is think about the audience. \r\n\r\n* \'Who are they?\'\r\n* \'What do they care, know about?\'\r\n* What do they expect to hear?','2023-08-24 05:50:08',NULL,NULL,NULL,NULL),(204,'An evaluator is sharing how they see the speech','2023-08-24 09:06:59',NULL,NULL,NULL,NULL),(205,'The evaluation is for the speech that was presented and not you as a person','2023-08-24 09:07:24',NULL,NULL,NULL,NULL),(206,'When recieving feedback, focus on what is being said and take note. Reactions and thoughts are for later.','2023-08-24 09:08:18',NULL,NULL,NULL,NULL),(207,'Ask evaluator, mentor, or friend for how to change the feedback into points you can improve or work on.','2023-08-24 09:09:02',NULL,NULL,NULL,NULL),(208,'When giving an evluation focus on feedback, which is what you observed as a listener. Avoid advice, which is advice for how you would change it. The purpose is for the speaker to be aware of how they are precieved not to conform the speaker to how you think the speech should be done.','2023-08-24 09:13:23',NULL,NULL,NULL,NULL),(209,'An effective evaluation:\r\n\r\n* 2-3 minutes\r\n* Uses \'I\' statements\r\n* feedback not advice\r\n* reference speakers goals\r\n* highlight what the speaker did well\r\n* ends with summary','2023-08-24 09:22:39',NULL,NULL,NULL,NULL),(210,'Points to add \r\n\r\n* reinforce positive behaviors\r\n* focus on project competencies\r\n* highlight areas for improvement','2023-08-24 09:24:21',NULL,NULL,NULL,NULL),(217,'Hästens mattresses go from $6.995 to $390.000. ','2023-10-30 09:35:08',NULL,NULL,NULL,NULL),(218,'SMART goals originally stood for Specific, Measurable, Assignable, Realistic, and Time-related','2023-10-30 09:42:12',NULL,NULL,NULL,NULL),(219,'ChatGPT launched in November 2022','2023-10-30 09:44:41',NULL,NULL,NULL,NULL),(220,'ChatGPT reduces the time for writing and increased the quality','2023-10-30 09:48:28',NULL,NULL,NULL,NULL),(221,'Writing something down is a tool to think it through','2023-10-30 09:52:32',NULL,NULL,NULL,NULL),(222,'AI writing assistants make mistakes, and being able to catch them requires a degree of knowledge a writer may not have, thus perpetuating the error. For example misplaced commas, or changing Indian to Native American, when referring to an individual from India.','2023-10-30 09:54:04',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notetag`
--

DROP TABLE IF EXISTS `notetag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notetag` (
                           `id` int(11) NOT NULL AUTO_INCREMENT,
                           `tag` varchar(512) NOT NULL,
                           `entry_datetime` datetime DEFAULT NULL,
                           `update_datetime` datetime DEFAULT NULL,
                           PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notetag`
--

LOCK TABLES `notetag` WRITE;
/*!40000 ALTER TABLE `notetag` DISABLE KEYS */;
INSERT INTO `notetag` VALUES (113,'language','2023-08-22 10:21:34','2023-08-22 10:21:34'),(114,'mind','2023-08-22 10:22:56','2023-08-22 10:22:56'),(115,'homo sapiens','2023-08-22 10:27:51','2023-08-22 10:27:51'),(116,'speeches','2023-08-22 19:26:04','2023-08-22 19:26:04'),(117,'toastmasters','2023-08-22 19:26:13','2023-08-22 19:26:13'),(118,'TO DO','2023-08-23 15:33:37','2023-08-23 15:33:37'),(119,'feedback','2023-08-24 09:10:15','2023-08-24 09:10:15'),(120,'vocabulary','2023-10-06 10:44:30','2023-10-06 10:44:30'),(121,'health','2023-10-06 10:44:42','2023-10-06 10:44:42'),(122,'','2023-10-07 16:02:05',NULL),(123,'sleep','2023-10-30 09:35:08',NULL),(124,'luxury','2023-10-30 09:35:08',NULL),(125,'article idea','2023-10-30 09:35:08',NULL),(126,'goals','2023-10-30 09:42:12',NULL),(127,'motivation','2023-10-30 09:42:12',NULL),(128,'chatgpt','2023-10-30 09:44:41',NULL),(129,'#Blog','2023-11-07 15:38:18',NULL);
/*!40000 ALTER TABLE `notetag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_type`
--

DROP TABLE IF EXISTS `object_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_type` (
                               `id` int(11) NOT NULL AUTO_INCREMENT,
                               `type` varchar(128) DEFAULT NULL,
                               PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_type`
--

LOCK TABLES `object_type` WRITE;
/*!40000 ALTER TABLE `object_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `object_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source` (
                          `id` int(11) NOT NULL AUTO_INCREMENT,
                          `entry_datetime` datetime DEFAULT NULL,
                          `update_datetime` datetime DEFAULT NULL,
                          `source_type_id` int(11) DEFAULT NULL,
                          `title` varchar(256) DEFAULT NULL,
                          `year` smallint(6) DEFAULT NULL,
                          `url` varchar(512) DEFAULT NULL,
                          PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `source`
--

LOCK TABLES `source` WRITE;
/*!40000 ALTER TABLE `source` DISABLE KEYS */;
INSERT INTO `source` VALUES (52,'2023-08-22 10:21:14',NULL,2,'The Language Instinct',2015,''),(53,'2023-08-22 19:24:25',NULL,2,'Ted Talks',2016,''),(54,'2023-08-23 15:34:48',NULL,2,'Thought',2023,''),(56,'2023-08-24 09:06:21',NULL,6,'Evaluation Feedback Project',2023,''),(57,'2023-10-30 09:35:08','2023-10-30 09:35:08',NULL,'We\'re All Having Trouble Sleeping These Days. Can a $390,000 Mattress Help?',NULL,'https://www.townandcountrymag.com/style/home-decor/a34194620/hastens-mattress-swedish-royals/'),(58,'2023-10-30 09:42:12','2023-10-30 09:42:12',NULL,'There\'s a S.M.A.R.T way to write management\'s goals and objectives',NULL,'https://community.mis.temple.edu/mis0855002fall2015/files/2015/10/S.M.A.R.T-Way-Management-Review.pdf'),(59,'2023-10-30 09:44:41','2023-10-30 09:44:41',NULL,'Why Human Writing Is Worth Defending In the Age of ChatGPT',NULL,'https://lithub.com/why-human-writing-is-worth-defending-in-the-age-of-chatgpt/'),(60,'2023-11-07 15:38:18','2023-11-07 15:38:18',NULL,'Garbage Day Blog',NULL,'https://www.garbageday.email/p/heres-where-the-fake-podcast-clips');
/*!40000 ALTER TABLE `source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `source_type`
--

DROP TABLE IF EXISTS `source_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source_type` (
                               `id` int(11) NOT NULL AUTO_INCREMENT,
                               `entry` varchar(100) DEFAULT NULL,
                               `type` varchar(128) DEFAULT NULL,
                               PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `source_type`
--

LOCK TABLES `source_type` WRITE;
/*!40000 ALTER TABLE `source_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `source_type` ENABLE KEYS */;
UNLOCK TABLES;

