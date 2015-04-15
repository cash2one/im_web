/*
SQLyog Ultimate v10.42 
MySQL - 5.5.5-10.0.17-MariaDB-1~wheezy-log : Database - gobelieve
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`gobelieve` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `gobelieve`;

/*Table structure for table `_object` */

DROP TABLE IF EXISTS `_object`;

CREATE TABLE `_object` (
  `id` bigint(13) unsigned NOT NULL AUTO_INCREMENT,
  `type` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1005 DEFAULT CHARSET=utf8;

/*Table structure for table `account` */

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `id` bigint(15) unsigned NOT NULL COMMENT '全局id',
  `name` varchar(64) NOT NULL COMMENT '姓名',
  `email` varchar(128) CHARACTER SET ascii NOT NULL COMMENT '账号（空值为僵尸账号）',
  `email_removed` varchar(128) CHARACTER SET ascii NOT NULL DEFAULT '' COMMENT '删除邮箱账号',
  `email_checked` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '邮箱是否已经校验',
  `password` varchar(128) CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '密码',
  `ctime` int(10) unsigned NOT NULL COMMENT '注册时间',
  `role` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '1：开发者，2：渠道，3：平台管理员',
  `mobile_zone` varchar(5) CHARACTER SET ascii NOT NULL COMMENT '区号',
  `mobile` varchar(18) CHARACTER SET ascii NOT NULL COMMENT '手机号码',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_unique` (`email`),
  KEY `email` (`email`),
  KEY `role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账号';

/*Table structure for table `app` */

DROP TABLE IF EXISTS `app`;

CREATE TABLE `app` (
  `id` bigint(15) unsigned NOT NULL COMMENT '全局id',
  `name` varchar(256) NOT NULL COMMENT '名称',
  `developer_id` bigint(15) unsigned NOT NULL COMMENT '开发商',
  `ctime` int(10) unsigned NOT NULL COMMENT '创建时间',
  `key` varchar(32) CHARACTER SET ascii NOT NULL COMMENT 'app key',
  `secret` varchar(32) CHARACTER SET ascii NOT NULL COMMENT 'app secret',
  `status` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '应用状态，0开发 1生产',
  PRIMARY KEY (`id`),
  KEY `developer_id` (`developer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='应用';

/*Table structure for table `client` */

DROP TABLE IF EXISTS `client`;

CREATE TABLE `client` (
  `id` bigint(15) unsigned NOT NULL COMMENT '全局id',
  `app_id` bigint(15) unsigned NOT NULL COMMENT '应用',
  `developer_id` bigint(15) unsigned NOT NULL COMMENT '开发商',
  `platform_type` tinyint(1) unsigned NOT NULL COMMENT '1：android，2：ios',
  `platform_identity` varchar(128) CHARACTER SET ascii NOT NULL COMMENT '客户端唯一标示，android为pakcage name；ios为bundle id',
  `ctime` int(10) unsigned NOT NULL COMMENT '创建时间',
  `utime` int(10) unsigned NOT NULL COMMENT '更新时间',
  `is_active` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '是否激活',
  PRIMARY KEY (`id`),
  KEY `app_id` (`app_id`),
  KEY `developer_id` (`developer_id`),
  KEY `is_active` (`is_active`),
  KEY `ctime` (`ctime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户端';

/*Table structure for table `client_apns` */

DROP TABLE IF EXISTS `client_apns`;

CREATE TABLE `client_apns` (
  `client_id` bigint(15) unsigned NOT NULL COMMENT '客户端',
  `sandbox_key` blob NOT NULL COMMENT '沙盒模式的证书',
  `sandbox_key_secret` varchar(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '沙盒模式的证书秘钥',
  `production_key` blob NOT NULL COMMENT '生产模式的证书',
  `production_key_secret` varchar(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '生产模式的证书秘钥',
  `sandbox_key_utime` int(10) unsigned NOT NULL COMMENT '沙盒证书修改时间，0为未上传',
  `production_key_utime` int(10) unsigned NOT NULL COMMENT '生产证书修改时间，0为未上传',
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='iOS客户端apns证书';

/*Table structure for table `client_certificate` */

DROP TABLE IF EXISTS `client_certificate`;

CREATE TABLE `client_certificate` (
  `client_id` bigint(15) unsigned NOT NULL COMMENT '客户端',
  `pkey` text NOT NULL COMMENT '私钥',
  `cer` text CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '证书',
  `update_time` int(10) unsigned NOT NULL COMMENT '修改时间',
  `xinge_access_id` bigint(20) DEFAULT NULL COMMENT '信鸽ID',
  `xinge_secret_key` varchar(64) CHARACTER SET ascii DEFAULT NULL COMMENT '信鸽密钥',
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='android证书';

/*Table structure for table `verify_email` */

DROP TABLE IF EXISTS `verify_email`;

CREATE TABLE `verify_email` (
  `email` varchar(128) CHARACTER SET ascii NOT NULL COMMENT '邮件',
  `usage_type` tinyint(3) unsigned NOT NULL COMMENT '1：开发者邮箱验证',
  `code` varchar(128) CHARACTER SET ascii NOT NULL COMMENT '验证码',
  `ctime` int(10) unsigned NOT NULL COMMENT '创建时间',
  `ro_id` bigint(15) unsigned NOT NULL COMMENT '邮箱所有者',
  PRIMARY KEY (`usage_type`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='邮箱验证';

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
