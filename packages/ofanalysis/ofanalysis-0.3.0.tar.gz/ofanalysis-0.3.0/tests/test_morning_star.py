from unittest import TestCase

from ofanalysis.morningstar.morning_star import MorningStar


class TestMorningStar(TestCase):
    def setUp(self) -> None:
        self.morning_star = MorningStar(
            web_driver_path='./tests/drivers/chromedriver',
            assets_path='./tests/assets',
            cookie_str='ASP.NET_SessionId=4odhi1umlj2znmv5flcqiw21; Hm_lvt_eca85e284f8b74d1200a42c9faa85464=1651049184; MS_LocalEmailAddr=laye0619@gmail.com=; user=username=laye0619@gmail.com&nickname=laye0619&status=Free&memberId=458975&password=trWMrjKv97VkUvhSrVRdJw==; MSCC=HjoB8XCQiko=; Hm_lpvt_eca85e284f8b74d1200a42c9faa85464=1651057823; authWeb=CFA76934BD25E778915164538713CF88E6BDF70446F69A8B6BD81A7BE959A37158D3FA9640B84913F8C5673C4B7A72693E0D2BF60BA344388ED6B13FD0E3F69E13C87857A369E963104FAE1C31414CAF769A822AE573E2BA7D838D6CFF961E8DADB3144B1AFE196E9E85235610561D951B4371DC; AWSALB=uVQy5Ebw2Q533c9B/ccqiIe2nZaomdIWoLn5/1IZJCQsNkJYKOGDOcuPW2iSJMuqX/j5m7Lfo5Tezc0BqtRYbtI6T92b5Ypod8qBCsVRhYKMDYFzh+Z6wKDkTMvk; AWSALBCORS=uVQy5Ebw2Q533c9B/ccqiIe2nZaomdIWoLn5/1IZJCQsNkJYKOGDOcuPW2iSJMuqX/j5m7Lfo5Tezc0BqtRYbtI6T92b5Ypod8qBCsVRhYKMDYFzh+Z6wKDkTMvk'
        )

    def test_get_fund_list(self):
        self.morning_star.get_fund_list()

    def test_write_to_db(self):
        self.morning_star.write_to_db()
        pass
