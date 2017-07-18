/*
Navicat MySQL Data Transfer

Source Server         : 山东大数据
Source Server Version : 50173
Source Host           : 10.254.32.8:3306
Source Database       : airplaninfo

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2017-07-18 14:01:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for flight
-- ----------------------------
DROP TABLE IF EXISTS `flight`;
CREATE TABLE `flight` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `flight_number` varchar(32) DEFAULT NULL,
  `company` varchar(64) DEFAULT NULL,
  `line` varchar(64) DEFAULT NULL,
  `send_date` varchar(19) DEFAULT NULL,
  `plane_type` varchar(32) DEFAULT NULL,
  `start_plan` varchar(32) DEFAULT NULL,
  `start_estimate` varchar(32) DEFAULT NULL,
  `start_actual` varchar(32) DEFAULT NULL,
  `arrive_plan` varchar(32) DEFAULT NULL,
  `arrive_estimate` varchar(32) DEFAULT NULL,
  `arrive_actual` varchar(32) DEFAULT NULL,
  `status` varchar(16) DEFAULT NULL,
  `exception` varchar(64) DEFAULT NULL,
  `exception_reason` varchar(64) DEFAULT NULL,
  `flight_number_share` varchar(32) DEFAULT NULL,
  `flight_type` varchar(32) DEFAULT NULL COMMENT '1-出发  2到站',
  `port_name` varchar(64) DEFAULT NULL,
  `plan_port` varchar(32) DEFAULT NULL,
  `air_port` varchar(64) DEFAULT NULL,
  `create_time` varchar(19) DEFAULT NULL,
  `modify_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index1` (`flight_number`) USING BTREE,
  KEY `idnex2` (`send_date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=98559 DEFAULT CHARSET=utf8;
