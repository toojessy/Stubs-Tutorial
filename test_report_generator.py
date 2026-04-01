import unittest
from unittest.mock import MagicMock

from interfaces import SaleRecord
from report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):

    def test_empty_month_returns_zero_revenue(self):
        repo_stub = MagicMock()
        repo_stub.get_sales.return_value = []

        gen = ReportGenerator(repo_stub)
        result = gen.monthly_summary(1, 2024)

        self.assertEqual(result["total_revenue"], 0.0)
        self.assertIsNone(result["top_product"])

    def test_identifies_top_product_by_revenue(self):
        repo_stub = MagicMock()
        repo_stub.get_sales.return_value = [
            SaleRecord("SKU-A", 10, 500.00),
            SaleRecord("SKU-B", 3, 1200.00),
            SaleRecord("SKU-C", 20, 300.00),
        ]

        gen = ReportGenerator(repo_stub)
        result = gen.monthly_summary(3, 2024)

        self.assertEqual(result["total_revenue"], 2000.00)
        self.assertEqual(result["top_product"], "SKU-B")

    def test_stub_simulates_repository_exception(self):
        repo_stub = MagicMock()
        repo_stub.get_sales.side_effect = ConnectionError("DB down")

        gen = ReportGenerator(repo_stub)

        with self.assertRaises(ConnectionError):
            gen.monthly_summary(6, 2024)

    def test_single_product_summary(self):
        repo_stub = MagicMock()
        repo_stub.get_sales.return_value = [
            SaleRecord("SKU-ONE", 5, 250.00)
        ]

        gen = ReportGenerator(repo_stub)
        result = gen.monthly_summary(2, 2024)

        self.assertEqual(result["total_revenue"], 250.00)
        self.assertEqual(result["top_product"], "SKU-ONE")

    def test_tied_revenue_products(self):
        repo_stub = MagicMock()
        repo_stub.get_sales.return_value = [
            SaleRecord("SKU-A", 5, 500.00),
            SaleRecord("SKU-B", 3, 500.00),
        ]

        gen = ReportGenerator(repo_stub)
        result = gen.monthly_summary(4, 2024)

        self.assertEqual(result["total_revenue"], 1000.00)
        self.assertIn(result["top_product"], ["SKU-A", "SKU-B"])

    def test_invalid_month_argument(self):
        repo_stub = MagicMock()
        repo_stub.get_sales.return_value = [
            SaleRecord("SKU-A", 1, 100.00)
        ]

        gen = ReportGenerator(repo_stub)
        result = gen.monthly_summary(13, 2024)

        self.assertEqual(result["total_revenue"], 100.00)
