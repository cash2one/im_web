USE `gobelieve`;

REPLACE INTO `_object` (`id`, `type`)
VALUES (7, 5), (8, 6), (9, 6), (10, 2), (17, 5), (18, 6), (19, 6);

REPLACE INTO `account` (`id`, `name`, `email`, `email_removed`, `email_checked`, `password`, `ctime`, `role`, `mobile_zone`, `mobile`)
VALUES (10, '演示账号', 'demo@gobelieve.io', '', 1, 'pbkdf2:sha1:1000$brLwvV1C$1ce07023f7d2c88131c5749f224b8de7cdac5ae6',
        1403633136, 1, '', '');

REPLACE INTO `app` (`id`, `name`, `developer_id`, `ctime`, `key`, `secret`)
VALUES (7, 'SDK测试', 10, 1403633136, 'sVDIlIiDUm7tWPYWhi6kfNbrqui3ez44', '0WiCxAU1jh76SbgaaFC7qIaBPm2zkyM1'),
(17, '羊蹄甲', 10, 1403633136, 'lc83RwzODvxaGELdHiOiOmI4vqWC6GkA', '5tFTKsZTYTmrZBCW71JZWOczZQBrxRHK');

REPLACE INTO `client` (`id`, `app_id`, `developer_id`, `platform_type`, `platform_identity`, `ctime`, `utime`, `is_active`)
VALUES (8, 7, 10, 1, 'io.gobelieve.im.demo', 1403633136, 1403633136, 1),
  (9, 7, 10, 2, 'io.gobelieve.im.demo', 1403633136, 1403633136, 1),
  (18, 17, 10, 1, 'com.beetle.bauhinia', 1403633136, 1403633136, 1),
  (19, 17, 10, 2, 'com.beetle.bauhinia', 1403633136, 1403633136, 1);

REPLACE into `client_certificate` (`client_id`, `pkey`, `cer`, `update_time`, `xinge_access_id`, `xinge_secret_key`) values('8','-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDW+AcMgZ4nrrS2\n1ikCKphxtRhW/D9UhBn4gaSTuxj8xoL55Hbo4xB3GRT9Kc0gj2zSi5kOXNIKx6qI\ncaQdTvR0oKDD15BSon80Akh6pGtJm53MiZvcKp+03sV8bN3AWhLQsNqa8EogiJbl\ng3JC3UKx/wKUOgNGYLnDmlGRB3thtQMm1rHROGWk16cqdTFzIvzLE+pNhfPIHCve\nfYLepP7r5fDMc9ve5vasngZwqTfPOgkSC2t2hay93gJx+7PQ5lcV/HeFpWMeeX1x\nHZ6vUawJcPVE30A4Lx01aCva1Ktt6PaCsgeDzDy0hs0LiIAUUQUNIwQwryiM/D/M\nj+ODp5nFAgMBAAECggEAGPVZFCmkbCULlELPJhI9+s200rycubpQrZqXuhM59ncx\n08Ojzqw2SC2gUzhcOZCNaPCOR62dMWU3NnpDPKfjF/tiTvqjJgT50dcGBT87uaMY\nshuz/d7xBfXrZePZ5zBOCO7PoreNU7OoGWOmi37W9IWQDheiM7SdPMmY+Maum4xL\nBiZsR2LymXxiG6AarAkphqGMIhUY9qESUX1sMSIPf/z3dfBlLV0NbpB6ELgB4kt4\n18pnotomD+0M8uq3RoQFzCUmIVQzU2thRFHuY3a2NvAie3lkA8/yKPVqvLKSiZda\nOzm5yrpfKmADdOuxQa9XFJ4htbsGY91TTNhFx0I/TQKBgQD6w9Z4OUJ4M0yy3O5Q\nz8CjlalWUBX2Nt+oz/I1RYqNki7mWFS6gayXB5d65uj2ppiUZbRO2qvDD3Brqz+S\nSTpO76g81pMsKpk+dx8wFtV4RzXtIRZ0aWDgzmj87q7DYSdc3dYCsGZYJ9Pxsv6c\nCfWVipOTTmTpEXEYsJMkrUc3twKBgQDbdOJ4C0CVt9OSkM73pXEqr3nCdx8TAgt1\n0NDBe/VyQdhvQVtqyMgF9i3Jb+jga8XatS4vk1iwC8mTrp+G2+hP37YXaJM4Aias\nmZiZrkiJBnu3PPz+6CQhhhCWcTwalAKkBUkgf/RYu2y2xtHiPp7VSR9LEoLmqkkA\nnUwGNn9iYwKBgQDvHiF7wLYWYmyHvk5ttr1t/79as8FNZ+P8WFYQ4EAPYU7hjWc1\n9YM6/R1AL8IDuLaUAytdaf0RYr6DnOdguf0k2jil0sLCAdjhDLwrogpqyBSvCrcb\nyIR9ubW5QmxZmGHtlweExurAszHSLynEZ2bL8zln5QAqktwye+XDuovHnwKBgQCr\nO8h5Yk5Cg+zRr6vOD4j9hW28DrZwXmgSxZwdXFtni3kVVim+aGuqOyv+wRM0COOY\ng0ZGWPIaaxgd42MWFwBtUmECYtZ8HTGP+0jWoOZ4BFcD4tKFEx0eCz1mJXSASHzG\n/ljQwwYlNhjdhMS/g5zrTuLb8NWypavQjuuC7YL3gQKBgFKv8wQFW9rGKsK+uyNd\nm5pRisjwmKb55WxauPr8i5SR7enuGz0pfG3+Q+eH+rLGsBqkWR4QsdbNkaOV/STu\nlxx/85A8Cp0fzo04eLMGJYvq4g1aeQcpXms0evhifGmj7aLVcbreBoK4BoGifrGt\nEf53WOhu0qi0AKEidf1/UUJJ\n-----END PRIVATE KEY-----\n','-----BEGIN CERTIFICATE-----\nMIIDlzCCAn+gAwIBAgIBBDANBgkqhkiG9w0BAQUFADBkMREwDwYDVQQKEwhOZXcg\nR2FtZTEbMBkGA1UECxMSTmV3IEdhbWUgRGV2ZWxvcGVyMSUwIwYDVQQDExxOZXcg\nR2FtZSBEZXZlbG9wZXIgQXV0aG9yaXR5MQswCQYDVQQGEwJDTjAeFw0xNDExMjAx\nNjAyMjNaFw0xNTExMjAxNjAyMjNaMBkxCzAJBgNVBAYTAkNOMQowCAYDVQQDEwE4\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1vgHDIGeJ660ttYpAiqY\ncbUYVvw/VIQZ+IGkk7sY/MaC+eR26OMQdxkU/SnNII9s0ouZDlzSCseqiHGkHU70\ndKCgw9eQUqJ/NAJIeqRrSZudzImb3CqftN7FfGzdwFoS0LDamvBKIIiW5YNyQt1C\nsf8ClDoDRmC5w5pRkQd7YbUDJtax0ThlpNenKnUxcyL8yxPqTYXzyBwr3n2C3qT+\n6+XwzHPb3ub2rJ4GcKk3zzoJEgtrdoWsvd4Ccfuz0OZXFfx3haVjHnl9cR2er1Gs\nCXD1RN9AOC8dNWgr2tSrbej2grIHg8w8tIbNC4iAFFEFDSMEMK8ojPw/zI/jg6eZ\nxQIDAQABo4GeMIGbMAkGA1UdEwQCMAAwHQYDVR0OBBYEFI5A/to6W/klokK/dPU5\ng5LIHR9CMB8GA1UdIwQYMBaAFMKWC8lmqP/rB9FJMWHeBuyOcff9MAsGA1UdDwQE\nAwIFoDATBgNVHSUEDDAKBggrBgEFBQcDAjAsBgNVHR8EJTAjMCGgH6AdhhtodHRw\nOi8vcGF0aC50by5jcmwvbXljYS5jcmwwDQYJKoZIhvcNAQEFBQADggEBALhgc5A4\n3yRoEorCTLZBdUksusYYvvP06AHpL1B3fZ7W2WJYk/OIkbZlHXlUZoHAf+JKQIKC\n8D38D59r7gXi87gTypLqXuaG8bssxZmKPYm3hqDWjWK2K/kkD3eo9P8XrArfhLaj\nlyhIcAv9Mj9+tE6CCqy5Y1KbbQIiGHByR+J2/CV0CuhVCHRBLJSjUvQBmuCxEfxu\nIhO6T563IbVIvFWy5Ew2x79T9Q4/Axvhkw06TRWtobtDI5RxXGtbDUZIikde1gbA\nrsS4ROby+cxhxq52qhP9QA34mou1NTQclw2m/+tQm1lPksiNBstSdK12fWuFMnMl\n2r7lVxOT5NIWPYQ=\n-----END CERTIFICATE-----\n','1416499343', '2100103204', '53c1be217035aa75c1ccb5770b5df9f9');
REPLACE into `client_certificate` (`client_id`, `pkey`, `cer`, `update_time`) values('18','-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxS4wZIDFr9Y+x\ntTOmavA7S1TFyrKSVX3kZI186W52mS1K+ZE3m22K/ID42m7Evdrik7Uw2jK3Z/kg\nrImD0rKTA4or4w6Ld9WBvK1n41mys7MUtuqp55tpMJkUy1ItPEbUkOxawZMBkgjg\npirzbtWyA67PX7ha1om4ERp8KP/JgjPU2arTYTL6mkIX+YSVwF7IpIEP3LND4Ii9\nOs/WGSsSdxjJFv21qH6rmXQVj0e5xVtZUKsuk9wPU9ILI7DywGYMe/++6enyMwFF\nh5qxT71rnQbXqZyjm68zUFPaN1dYe9arxqKp7T8QfTQzwZp+LgFWddYg+tKGFzju\nPlGtS5kTAgMBAAECggEAfQS9vLXzw6H7+p7A1hfQYK9lDrg5JXD9fgDduHhOeXjX\n9Gd5XBHQs9IMC+7Tbw5Fe8IWYWVrn+LETKL9sSPw4jP7yaiph/Uva/Wk/X3WsWl/\n3RqC7N4xu4IWYBBjWRyJAblTwUeApvnYIrlpzhCYxZdNPFPOBtgDcvU0jNrIS8nD\nWA+sMXvQMLI5+66AW+thnTUWrW8RUiZZtWM4Ykzx66UnP61qAZ/S/8I9jXjN2khZ\nBL7lDEPBP7o2NY1oiD1EKwEHdW850AROT0ZmE5bDEUWAH9EAnlyMbIL/lwJpmWlB\njO+6M3qNneIGiJioZIdJS13TuuqNEwcQG1nn2v+bYQKBgQDradf7UHmvshOPq7TE\nvlZ4/wuk85RMVDBMPFxBoszGhY8fzupU76YnsoYxQDW7N9uiSiRJyfGdfBYFKGcB\ne1al4dCOwqK7My7U5hGsQUd2jKQaMKghpywd3q3AXLrQqodHy0IFaONuUZLyBCrB\nxUIrHWFaLfLxPFduGK8Ea1PH8QKBgQDAzJ6DzaTmvk/I9sQgPoR8DO6kALr9SNJm\nTnFtYZAj9K8ZMkDbuHztSS58fxBDngwdy7fyB8Ir8WOrTl956AXDxugTK5q08kSJ\nJuGTBhVeZbgb+w0nyQntzWDv7za2ja1TNZOXrhu1KtmX3Oj/l6tDV+EcFUCuzBmX\n7zPNue+VQwKBgQDTS9ou2SmPmE9UafLDkG+/BHSoJnTaGcqL8rV/uCcCnMg87ZSI\njd1dzjACLrbLhrRdMxzlGhwClWiSUpQ50UGRfGCccnhre+Ix9xqvuJvy/QMh+sA+\nDHVdjgv4F4MaXaU0vGxSvLU9xHwXO8RAzdO5LRK/RXTEL7vttrwIRGkbkQKBgCiJ\n3bqw/r9VvMjwugRdoNXEklkBnk+rhDHmxIrPPNOSm06c9m48uGfcP14GCZFuJfYN\n47uMThOXSfG3JPQpCS1FIX8GaB0r46VC+6NCYDPdB306qGV5LBFIYd2RWtu/pnYc\nidAW19ScEeyQkp1LcsNSMw8ImPUoDSmZLjdPpUSpAoGALz/AdP2SSmuwmQf2Rx/M\n5Of2ZuIjdQ60GNqvnXjlszphh5GJfw0M4Fw5sjY3ol8mXgoukyDTBE3m/GIYDhQP\n8/gdipZm7xZFtOZyz9zddvVte9xDvg94thV316xPBkQ0knB4b5Zph7qMvPHsinWc\nX0X5WSKT1wKdgXysqgjGYmU=\n-----END PRIVATE KEY-----\n','-----BEGIN CERTIFICATE-----\nMIIDlzCCAn+gAwIBAgIBAzANBgkqhkiG9w0BAQUFADBkMREwDwYDVQQKEwhOZXcg\nR2FtZTEbMBkGA1UECxMSTmV3IEdhbWUgRGV2ZWxvcGVyMSUwIwYDVQQDExxOZXcg\nR2FtZSBEZXZlbG9wZXIgQXV0aG9yaXR5MQswCQYDVQQGEwJDTjAeFw0xNDExMjAx\nNjAyMjNaFw0xNTExMjAxNjAyMjNaMBkxCzAJBgNVBAYTAkNOMQowCAYDVQQDEwE1\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsUuMGSAxa/WPsbUzpmrw\nO0tUxcqyklV95GSNfOludpktSvmRN5ttivyA+NpuxL3a4pO1MNoyt2f5IKyJg9Ky\nkwOKK+MOi3fVgbytZ+NZsrOzFLbqqeebaTCZFMtSLTxG1JDsWsGTAZII4KYq827V\nsgOuz1+4WtaJuBEafCj/yYIz1Nmq02Ey+ppCF/mElcBeyKSBD9yzQ+CIvTrP1hkr\nEncYyRb9tah+q5l0FY9HucVbWVCrLpPcD1PSCyOw8sBmDHv/vunp8jMBRYeasU+9\na50G16mco5uvM1BT2jdXWHvWq8aiqe0/EH00M8Gafi4BVnXWIPrShhc47j5RrUuZ\nEwIDAQABo4GeMIGbMAkGA1UdEwQCMAAwHQYDVR0OBBYEFPAYE4rMrxKefn62WnH7\n+xIix9WUMB8GA1UdIwQYMBaAFMKWC8lmqP/rB9FJMWHeBuyOcff9MAsGA1UdDwQE\nAwIFoDATBgNVHSUEDDAKBggrBgEFBQcDAjAsBgNVHR8EJTAjMCGgH6AdhhtodHRw\nOi8vcGF0aC50by5jcmwvbXljYS5jcmwwDQYJKoZIhvcNAQEFBQADggEBADMUqAuR\nR5gUXQr0PPLMzM/AFN0DW7sEGzXSQh5nl5NA6gMVfg61op+Rn0+YBmFranKSwWfd\npFCvUQSFbK9QXPaZ0p7XWaHPInmqREaczZYqWMJSO0pzzxz5fRAAnGpdoyyV6kuC\nNwARVSrQX3pDUasKRhtQkotF9i22rIRmYNol726sAdxiWsLJkODyInTjcSZLAHJa\noDRyN8K8YeSUHU3e7wQQ93eiS1t89lizFhxpldJLoUqI7VG6Jadpu0vEqW/m5DTT\nVsLvVQZyWAs3QhL+UL4BARWV7SkpcswsB7bStp6lGbb9/e1fuJ1FmYSCVVGcjfHl\n2QtxtHsu/nO8Kjo=\n-----END CERTIFICATE-----\n','1416499343');
