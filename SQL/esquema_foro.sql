-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema esquema_perfumes
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_perfumes` ;

-- -----------------------------------------------------
-- Schema esquema_perfumes
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_perfumes` DEFAULT CHARACTER SET utf8 ;
USE `esquema_perfumes` ;

-- -----------------------------------------------------
-- Table `esquema_perfumes`.`suscripciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`suscripciones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(255) NULL,
  `precio` FLOAT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `apellido` VARCHAR(255) NULL,
  `nombre_usuario` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `suscripcion_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_usuarios_suscripciones_idx` (`suscripcion_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_suscripciones`
    FOREIGN KEY (`suscripcion_id`)
    REFERENCES `esquema_perfumes`.`suscripciones` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`temas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`temas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `usuario_id` INT NOT NULL,
  `tema_id` INT NOT NULL,
  PRIMARY KEY (`id`, `tema_id`),
  INDEX `fk_temas_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_posts_temas1_idx` (`tema_id` ASC) VISIBLE,
  CONSTRAINT `fk_temas_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_perfumes`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_temas1`
    FOREIGN KEY (`tema_id`)
    REFERENCES `esquema_perfumes`.`temas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`participantes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`participantes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `post_id` INT NOT NULL,
  PRIMARY KEY (`id`, `usuario_id`, `post_id`),
  INDEX `fk_usuarios_has_temas_temas1_idx` (`post_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_temas_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_temas_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_perfumes`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_temas_temas1`
    FOREIGN KEY (`post_id`)
    REFERENCES `esquema_perfumes`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `mensaje` TEXT NULL,
  `created_by` DATETIME NULL,
  `usuario_id` INT NOT NULL,
  `post_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comentarios_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_comentarios_temas1_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_comentarios_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_perfumes`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comentarios_temas1`
    FOREIGN KEY (`post_id`)
    REFERENCES `esquema_perfumes`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`categorias` (
  `id` INT NOT NULL,
  `tipo` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`productos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `descripcion` TEXT NULL,
  `precio` FLOAT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `categoria_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_productos_categorias1_idx` (`categoria_id` ASC) VISIBLE,
  CONSTRAINT `fk_productos_categorias1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `esquema_perfumes`.`categorias` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`regiones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`regiones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`comunas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`comunas` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`direcciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`direcciones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `calle` VARCHAR(255) NULL,
  `numero` INT NULL,
  `referencia` TEXT NULL,
  `nombre_de` VARCHAR(255) NULL,
  `region_id` INT NOT NULL,
  `comuna_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_direcciones_regiones1_idx` (`region_id` ASC) VISIBLE,
  INDEX `fk_direcciones_comunas1_idx` (`comuna_id` ASC) VISIBLE,
  CONSTRAINT `fk_direcciones_regiones1`
    FOREIGN KEY (`region_id`)
    REFERENCES `esquema_perfumes`.`regiones` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_direcciones_comunas1`
    FOREIGN KEY (`comuna_id`)
    REFERENCES `esquema_perfumes`.`comunas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`compras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`compras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `bolsa_id` INT NOT NULL,
  `direccion_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_compras_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_compras_direcciones1_idx` (`direccion_id` ASC) VISIBLE,
  CONSTRAINT `fk_compras_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_perfumes`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_compras_direcciones1`
    FOREIGN KEY (`direccion_id`)
    REFERENCES `esquema_perfumes`.`direcciones` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`bolsa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`bolsa` (
  `id` INT NOT NULL,
  `producto_id` INT NOT NULL,
  `compra_id` INT NOT NULL,
  PRIMARY KEY (`id`, `producto_id`, `compra_id`),
  INDEX `fk_productos_has_compras_compras1_idx` (`compra_id` ASC) VISIBLE,
  INDEX `fk_productos_has_compras_productos1_idx` (`producto_id` ASC) VISIBLE,
  CONSTRAINT `fk_productos_has_compras_productos1`
    FOREIGN KEY (`producto_id`)
    REFERENCES `esquema_perfumes`.`productos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_productos_has_compras_compras1`
    FOREIGN KEY (`compra_id`)
    REFERENCES `esquema_perfumes`.`compras` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`subcategorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`subcategorias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `categoria_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_subcategorias_categorias1_idx` (`categoria_id` ASC) VISIBLE,
  CONSTRAINT `fk_subcategorias_categorias1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `esquema_perfumes`.`categorias` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_perfumes`.`clasificaciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_perfumes`.`clasificaciones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `producto_id` INT NOT NULL,
  `subcategoria_id` INT NOT NULL,
  PRIMARY KEY (`id`, `producto_id`, `subcategoria_id`),
  INDEX `fk_productos_has_subcategorias_subcategorias1_idx` (`subcategoria_id` ASC) VISIBLE,
  INDEX `fk_productos_has_subcategorias_productos1_idx` (`producto_id` ASC) VISIBLE,
  CONSTRAINT `fk_productos_has_subcategorias_productos1`
    FOREIGN KEY (`producto_id`)
    REFERENCES `esquema_perfumes`.`productos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_productos_has_subcategorias_subcategorias1`
    FOREIGN KEY (`subcategoria_id`)
    REFERENCES `esquema_perfumes`.`subcategorias` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
