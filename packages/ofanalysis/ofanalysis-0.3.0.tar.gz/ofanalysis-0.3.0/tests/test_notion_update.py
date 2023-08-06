from unittest import TestCase

import ofanalysis.notion.notion_update as notion_update


class TestNotionUpdate(TestCase):
    def test_update_profit_ratio_to_notion(self):
        notion_update.update_profit_ratio_to_notion()
