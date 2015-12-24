/*
 Navicat Premium Data Transfer

 Source Server         : gobelieve_aliyun
 Source Server Type    : MySQL
 Source Server Version : 50505
 Source Host           : 10.251.43.254
 Source Database       : gobelieve

 Target Server Type    : MySQL
 Target Server Version : 50505
 File Encoding         : utf-8

 Date: 12/24/2015 15:45:58 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `_object`
-- ----------------------------
DROP TABLE IF EXISTS `_object`;
CREATE TABLE `_object` (
  `id` bigint(13) unsigned NOT NULL AUTO_INCREMENT,
  `type` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1452 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `account`
-- ----------------------------
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

-- ----------------------------
--  Table structure for `app`
-- ----------------------------
DROP TABLE IF EXISTS `app`;
CREATE TABLE `app` (
  `id` bigint(15) unsigned NOT NULL COMMENT '全局id',
  `name` varchar(256) NOT NULL COMMENT '名称',
  `developer_id` bigint(15) unsigned NOT NULL COMMENT '开发商',
  `ctime` int(10) unsigned NOT NULL COMMENT '创建时间',
  `key` varchar(32) CHARACTER SET ascii NOT NULL COMMENT 'app key',
  `secret` varchar(32) CHARACTER SET ascii NOT NULL COMMENT 'app secret',
  `status` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '应用状态，0开发 1生产',
  `publish_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '发布时间戳',
  PRIMARY KEY (`id`),
  KEY `developer_id` (`developer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='应用';

-- ----------------------------
--  Table structure for `client`
-- ----------------------------
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

-- ----------------------------
--  Table structure for `client_apns`
-- ----------------------------
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

-- ----------------------------
--  Table structure for `client_certificate`
-- ----------------------------
DROP TABLE IF EXISTS `client_certificate`;
CREATE TABLE `client_certificate` (
  `client_id` bigint(15) unsigned NOT NULL COMMENT '客户端',
  `pkey` text NOT NULL COMMENT '私钥',
  `cer` text CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '证书',
  `update_time` int(10) unsigned NOT NULL COMMENT '修改时间',
  `xinge_access_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '信鸽ID',
  `xinge_secret_key` varchar(64) CHARACTER SET ascii NOT NULL DEFAULT '' COMMENT '信鸽密钥',
  `mi_appid` bigint(20) NOT NULL DEFAULT '0' COMMENT '小米推送ID',
  `mi_secret_key` varchar(64) CHARACTER SET ascii NOT NULL DEFAULT '' COMMENT '小米推送密钥',
  `hw_appid` bigint(20) NOT NULL DEFAULT '0' COMMENT '华为推送ID',
  `hw_secret_key` varchar(64) CHARACTER SET ascii NOT NULL DEFAULT '' COMMENT '华为推送密钥',
  `gcm_sender_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '谷歌发送者ID',
  `gcm_api_key` varchar(64) CHARACTER SET ascii NOT NULL DEFAULT '' COMMENT '谷歌推送API密钥',
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='android证书';

-- ----------------------------
--  Table structure for `verify_email`
-- ----------------------------
DROP TABLE IF EXISTS `verify_email`;
CREATE TABLE `verify_email` (
  `email` varchar(128) CHARACTER SET ascii NOT NULL COMMENT '邮件',
  `usage_type` tinyint(3) unsigned NOT NULL COMMENT '1：开发者邮箱验证',
  `code` varchar(128) CHARACTER SET ascii NOT NULL COMMENT '验证码',
  `ctime` int(10) unsigned NOT NULL COMMENT '创建时间',
  `ro_id` bigint(15) unsigned NOT NULL COMMENT '邮箱所有者',
  PRIMARY KEY (`usage_type`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='邮箱验证';

SET FOREIGN_KEY_CHECKS = 1;
