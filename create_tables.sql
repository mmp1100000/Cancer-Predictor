-- MySQL Script generated by MySQL Workbench
-- Wed Jan  9 09:27:48 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`usuario` ;

CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `rol` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`model`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`model` ;

CREATE TABLE IF NOT EXISTS `mydb`.`model` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `train_date` DATETIME NULL,
  `acc` DECIMAL(10) NOT NULL,
  `model_type` VARCHAR(45) NULL,
  `dataset_description` VARCHAR(500) NULL,
  `train_data_path` VARCHAR(500) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`patient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`patient` ;

CREATE TABLE IF NOT EXISTS `mydb`.`patient` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `patient_id` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`prediction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`prediction` ;

CREATE TABLE IF NOT EXISTS `mydb`.`prediction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `datetime` DATETIME NOT NULL,
  `expression_file_path` VARCHAR(45) NOT NULL,
  `result` VARCHAR(45) NOT NULL,
  `model_id` INT NOT NULL,
  `patient_id` INT NOT NULL,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`, `model_id`, `patient_id`, `usuario_id`),
  INDEX `fk_prediction_model_idx` (`model_id` ASC),
  INDEX `fk_prediction_patient1_idx` (`patient_id` ASC),
  INDEX `fk_prediction_usuario1_idx` (`usuario_id` ASC),
  CONSTRAINT `fk_prediction_model`
    FOREIGN KEY (`model_id`)
    REFERENCES `mydb`.`model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prediction_patient1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `mydb`.`patient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prediction_usuario1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `mydb`.`usuario` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
