# -*- coding: utf-8 -*-
from datetime import date
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


def aitool(input_schema: dict, output_schema: dict, required_inputs: list = None):
    """
    OCA-inspired decorator for registering and introspecting AI tools
    with OpenAPI / JSON Schema validation metadata.
    """
    def decorator(func):
        func._ai_tool = {
            "input_schema": {
                "type": "object",
                "properties": input_schema or {},
                "required": required_inputs or [],
            },
            "output_schema": {
                "type": "object",
                "properties": output_schema or {},
            },
        }
        return func
    return decorator


class AiTool(models.Model):
    _name = 'ai.tool'
    _description = 'Odoo AI Tool Registry (OCA Standard)'

    name = fields.Char(string='Tool Name', required=True)
    code = fields.Char(string='Technical Code', required=True, index=True)
    description = fields.Text(string='Tool Description')
    category = fields.Selection([
        ('contacts', 'Contacts & Partners'),
        ('inventory', 'Products & Inventory'),
        ('sales', 'Sales & CRM'),
        ('accounting', 'Invoicing & Finance'),
        ('system', 'System & Custom Workflows'),
    ], string='Category', default='contacts', required=True)
    model_name = fields.Char(string='Target Odoo Model', required=True, default='ai.tool')
    method_name = fields.Char(string='Python Method Name', required=True)
    active = fields.Boolean(string='Active', default=True)

    def execute_tool(self, **kwargs):
        """Dynamically invokes the configured Python method on the target model."""
        self.ensure_one()
        if self.model_name not in self.env:
            return {"success": False, "error": f"Model '{self.model_name}' is not installed in this database."}
        model_obj = self.env[self.model_name]
        if hasattr(model_obj, self.method_name):
            func = getattr(model_obj, self.method_name)
            return func(**kwargs)
        raise AttributeError(f"Method '{self.method_name}' not found on model '{self.model_name}'.")

    @api.model
    @aitool(
        input_schema={
            "query": {"type": "string", "description": "Name, email, or tax ID (VAT) of the contact/partner"}
        },
        output_schema={
            "success": {"type": "boolean"},
            "count": {"type": "integer"},
            "partners": {"type": "array"},
        },
        required_inputs=[]
    )
    def action_tool_search_partners(self, query="", **kwargs):
        """Searches contacts, customers, and suppliers in res.partner."""
        Partner = self.env['res.partner']
        domain = []
        if query:
            domain = ['|', '|', ('name', 'ilike', query), ('email', 'ilike', query), ('vat', 'ilike', query)]

        fields_to_read = ['id', 'name', 'email', 'phone', 'city', 'vat', 'is_company']
        available_fields = [f for f in fields_to_read if f in Partner._fields]

        partners = Partner.search_read(domain, available_fields, limit=15)
        return {
            "success": True,
            "count": len(partners),
            "partners": partners,
        }

    @api.model
    @aitool(
        input_schema={
            "query": {"type": "string", "description": "Product name, internal reference, or barcode"}
        },
        output_schema={
            "success": {"type": "boolean"},
            "count": {"type": "integer"},
            "products": {"type": "array"},
        },
        required_inputs=[]
    )
    def action_tool_check_product_stock(self, query="", **kwargs):
        """Queries products, list prices, and available stock if the product/stock modules are installed."""
        if 'product.product' not in self.env:
            return {"success": False, "error": "The Product module is not installed."}

        Product = self.env['product.product']
        domain = []
        if query:
            domain = ['|', ('name', 'ilike', query), ('default_code', 'ilike', query)]

        fields_to_read = ['id', 'name', 'default_code', 'lst_price', 'qty_available']
        available_fields = [f for f in fields_to_read if f in Product._fields]

        products = Product.search_read(domain, available_fields, limit=15)
        return {
            "success": True,
            "count": len(products),
            "products": products,
        }

    @api.model
    @aitool(
        input_schema={
            "target_date": {"type": "string", "description": "Target date in YYYY-MM-DD format (defaults to today)"}
        },
        output_schema={
            "success": {"type": "boolean"},
            "date": {"type": "string"},
            "order_count": {"type": "integer"},
            "total_sales": {"type": "number"},
        },
        required_inputs=[]
    )
    def action_tool_sales_summary(self, target_date="", **kwargs):
        """Returns consolidated sales orders and revenue for the specified date."""
        today_str = target_date or date.today().strftime('%Y-%m-%d')
        start_dt = f"{today_str} 00:00:00"
        end_dt = f"{today_str} 23:59:59"

        total_sales = 0.0
        order_count = 0

        if 'sale.order' in self.env:
            orders = self.env['sale.order'].search([
                ('date_order', '>=', start_dt),
                ('date_order', '<=', end_dt),
                ('state', 'in', ['sale', 'done']),
            ])
            total_sales += sum(orders.mapped('amount_total'))
            order_count += len(orders)

        if order_count == 0 and 'pos.order' in self.env:
            pos_orders = self.env['pos.order'].search([
                ('date_order', '>=', start_dt),
                ('date_order', '<=', end_dt),
                ('state', 'in', ['paid', 'done', 'invoiced']),\
            ])
            total_sales += sum(pos_orders.mapped('amount_total'))
            order_count += len(pos_orders)

        return {
            "success": True,
            "date": today_str,
            "order_count": order_count,
            "total_sales": round(total_sales, 2),
        }

    @api.model
    @aitool(
        input_schema={
            "report_type": {"type": "string", "description": "'receivables' for customer invoices or 'payables' for vendor bills"}
        },
        output_schema={
            "success": {"type": "boolean"},
            "report_type": {"type": "string"},
            "total_amount": {"type": "number"},
            "invoice_count": {"type": "integer"},
        },
        required_inputs=[]
    )
    def action_tool_financial_summary(self, report_type="receivables", **kwargs):
        """Queries open accounts receivable or accounts payable in account.move."""
        if 'account.move' not in self.env:
            return {"success": False, "error": "The Accounting/Invoicing module is not installed."}

        move_types = ['out_invoice', 'out_refund'] if report_type in ('receivables', 'receber') else ['in_invoice', 'in_refund']
        moves = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('payment_state', 'in', ['not_paid', 'partial']),
            ('move_type', 'in', move_types),
        ])
        total_amount = sum(moves.mapped('amount_residual'))
        return {
            "success": True,
            "report_type": report_type,
            "total_amount": round(total_amount, 2),
            "invoice_count": len(moves),
        }
