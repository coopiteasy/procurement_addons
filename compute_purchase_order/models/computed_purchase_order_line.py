from openerp import models, fields, api, _


class ComputedPurchaseOrderLine(models.TransientModel):
    _description = 'Computed Purchase Order Line'
    _name = 'computed.purchase.order.line'

    name = fields.Char('Product Name',
                       required=True,
                       read_only=True)

    category_id = fields.Many2one('product.category',
                                  'Internal Category',
                                  required=True,
                                  read_only=True)

    product_template_id = fields.Many2one('product.template',
                                          'Linked Product Template',
                                          required=True,
                                          help="Linked Product Template")

    stock_qty = fields.Float('Stock Quantity',
                             compute='_get_stock_quantity',
                             hep='Quantity currently in stock. Does not take '
                                 'into account incoming orders.')

    uom_id = fields.Many2one('product.uom',
                             'Unit of Measure',
                             required=True,
                             help="Default Unit of Measure used for all "
                                  "stock operation.")

    average_consumption = fields.Float('Average Consumption',
                                       read_only=True)

    stock_coverage = fields.Float('Stock Coverage',
                                  read_only=True)

    purchase_quantity = fields.Float('Purchase Quantity',
                                     required=True,
                                     default=0.)

    uom_po_id = fields.Many2one('product.uom',
                                'Purchase Unit of Measure',
                                required=True,
                                help="Default Unit of Measure used for all stock operation.")  # noqa

    # supplier_product_price = fields.Float('Supplier Product Price (w/o VAT)',
    #                                       help='Supplier Product Price by buying unit. Price is  without VAT')  # noqa
    #
    # supplier_product_vat = fields.Float('Supplier Product VAT')
    #
    # virtual_coverage = fields.Integer('Expected Stock Coverage',
    #                                   compute='_compute_virtual_coverage',
    #                                   help='Expected stock coverage (in days) based on current stocks and average daily consumption')  # noqa
    #
    # sub_total = fields.Float('Total Amount (w/o VAT)',
    #                          compute='_compute_sub_total')
    #
    # def _compute_virtual_coverage(self):
    #     return 231
    #
    # def _compute_sub_total(self):
    #     return 1234.5

    @api.multi
    def _get_stock_quantity(self):
        for pol in self:
            pol.stock_qty = pol.product_template_id.qty_available
