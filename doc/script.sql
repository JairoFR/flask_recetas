-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema db_recetas
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `db_recetas` ;

-- -----------------------------------------------------
-- Schema db_recetas
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_recetas` DEFAULT CHARACTER SET utf8mb3 ;
USE `db_recetas` ;

-- -----------------------------------------------------
-- Table `db_recetas`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_recetas`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL DEFAULT NULL,
  `apellido` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `db_recetas`.`recetas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_recetas`.`recetas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_creador` INT NOT NULL,
  `nombre` VARCHAR(255) NULL,
  `descripcion` TEXT NULL,
  `instruccion` TEXT NULL,
  `fecha_cocinado` DATE NULL,
  `tiempo` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_recetas_usuarios_idx` (`usuario_creador` ASC) VISIBLE,
  CONSTRAINT `fk_recetas_usuarios`
    FOREIGN KEY (`usuario_creador`)
    REFERENCES `db_recetas`.`usuarios` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
