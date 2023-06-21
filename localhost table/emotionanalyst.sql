-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 25, 2023 at 04:02 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `emotionanalyst`
--

-- --------------------------------------------------------

--
-- Table structure for table `uanswer`
--

CREATE TABLE `uanswer` (
  `Answer` varchar(1000) NOT NULL,
  `Cat` varchar(1000) NOT NULL,
  `question` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `uanswer`
--

INSERT INTO `uanswer` (`Answer`, `Cat`, `question`) VALUES
('I am happy', 'Happy', 'Why are you so happy?'),
('Don\'t talk to me.', 'Angry', 'Why are you so angry?'),
('I am scared.', 'Fearful', 'Why are you feeling scared?'),
('I am upset.', 'Sad', 'What is the reason for your sadness?');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
