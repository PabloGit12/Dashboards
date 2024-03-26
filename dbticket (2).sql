-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 26, 2024 at 08:59 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbticket`
--

-- --------------------------------------------------------

--
-- Table structure for table `departamentos`
--

CREATE TABLE `departamentos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `responsable` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `departamentos`
--

INSERT INTO `departamentos` (`id`, `nombre`, `responsable`) VALUES
(1, 'myriam', 'Juan'),
(2, 'Akemi', 'AAAAAAAAAAAAAAAA'),
(3, 'Marketing', 'Rene'),
(4, 'Contabilidad', 'Pablo'),
(5, 'Marketing', 'Andres'),
(6, 'Investigacion ', 'Mex'),
(7, 'Investigacion ', 'Isay'),
(8, 'Contabilidad', 'Pablo'),
(9, 'Investigacion ', 'df'),
(10, 'Investigacion ', 'Yo mero'),
(11, 'departamento Garritas', 'Akemi');

-- --------------------------------------------------------

--
-- Table structure for table `reportes`
--

CREATE TABLE `reportes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `departamento` varchar(255) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reportes`
--

INSERT INTO `reportes` (`id`, `nombre`, `departamento`, `fecha`, `descripcion`) VALUES
(1, 'Akemi', 'contabilidad', '2024-03-11', 'fallo los calculos'),
(2, 'mex', 'compras', '2024-03-12', 'kkk'),
(3, 'Akemi', 'compras', '2024-03-13', 'LO QUE SEA'),
(4, 'yo mero', 'produccion', '2024-03-13', 'esta saliendo mal la produccion '),
(5, 'yo mero', 'ventas', '2024-03-13', 'Las ventas estan bajas :('),
(6, 'yo mero', 'ventas', '2024-03-13', 'Las ventas estan bajas :('),
(7, 'yo mero', 'produccion', '2024-03-13', 'baja produccion '),
(9, 'yo mero', 'produccion', '2024-03-13', 'baja produccion '),
(10, 'Akemi', 'compras', '2024-03-13', 'estan robando la tienda'),
(13, 'Majo', 'compras', '2024-03-13', 'Se robaron las bolsas'),
(14, 'Pablo', 'logistica', '2024-03-14', 'sdhjhgfew'),
(15, 'Juan', 'logistica', '2024-03-14', 'holii'),
(16, 'sjdsjds', 'ventas', '2024-03-14', 'dhjidwkjdwhkdwdwhk'),
(17, 'Akemi', 'compras', '2024-03-14', 'sdfghj');

-- --------------------------------------------------------

--
-- Table structure for table `solicitudes`
--

CREATE TABLE `solicitudes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `departamento` varchar(255) DEFAULT NULL,
  `tipo_soporte` varchar(255) DEFAULT NULL,
  `detalles` text DEFAULT NULL,
  `fecha` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `solicitudes`
--

INSERT INTO `solicitudes` (`id`, `nombre`, `departamento`, `tipo_soporte`, `detalles`, `fecha`) VALUES
(1, 'Solicitud 1', 'logistica', 'Soporte técnico', 'Detalles de la solicitud 1', '2024-03-14'),
(2, 'Solicitud 2', 'ventas', 'Asistencia técnica', 'Detalles de la solicitud 2', '2024-03-15'),
(3, 'Solicitud 3', 'compras', 'Instalación de software', 'Detalles de la solicitud 3', '2024-03-16'),
(4, 'Solicitud 4', 'contabilidad', 'Soporte de red', 'Detalles de la solicitud 4', '2024-03-17'),
(5, 'Solicitud 5', 'produccion', 'Mantenimiento preventivo', 'Detalles de la solicitud 5', '2024-03-18'),
(6, 'Solicitud 6', 'logistica', 'Asistencia remota', 'Detalles de la solicitud 6', '2024-03-19'),
(7, 'Solicitud 7', 'ventas', 'Soporte técnico', 'Detalles de la solicitud 7', '2024-03-20'),
(8, 'Solicitud 8', 'compras', 'Instalación de hardware', 'Detalles de la solicitud 8', '2024-03-21'),
(9, 'Solicitud 9', 'contabilidad', 'Asistencia telefónica', 'Detalles de la solicitud 9', '2024-03-22'),
(10, 'Solicitud 10', 'produccion', 'Soporte de aplicaciones', 'Detalles de la solicitud 10', '2024-03-23'),
(11, 'yo mero', 'ventas', 'Errores de software', 'se chafio el epsel', '2024-03-14'),
(12, 'yo mero', 'ventas', 'Errores de software', 'se chafio el epsel', '2024-03-14'),
(13, 'Juan', 'logistica', 'Fallas en la red', 'no jala la lap', '2024-03-14'),
(14, 'yo mero', 'logistica', 'Fallas de office', 'no furula el Epsel', '2024-03-14'),
(15, 'yo mero', 'compras', 'Mantenimientos Preventivos', 'mi monitor esta muerto', '2024-03-14'),
(16, 'frt', 'compras', 'Mantenimientos Preventivos', 'edfghj', '2024-03-14');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `departamento` varchar(255) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `departamento`, `contraseña`) VALUES
(1, 'Contabilidad', 'contabilidad1234'),
(2, 'Produccion', 'produccion1234'),
(3, 'Compras', 'compras1234'),
(4, 'Ventas', 'ventas1234'),
(5, 'Jefe', 'jefe1234'),
(6, 'Logistica', 'logistica1234');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`) VALUES
(1, 'Juan', 'juanito45@gmail.com'),
(2, 'Akemi', 'japonesa89@gmail.com'),
(3, 'mex', 'ana12@gmail.com'),
(4, 'Pablo', 'pablito2003@gmail.com'),
(5, 'Juan', 'ana12@gmail.com'),
(6, 'IvanIsay', 'ivan@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `departamentos`
--
ALTER TABLE `departamentos`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reportes`
--
ALTER TABLE `reportes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `solicitudes`
--
ALTER TABLE `solicitudes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `solicitudes`
--
ALTER TABLE `solicitudes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
