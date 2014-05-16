# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
import openerp.addons.decimal_precision as dp

LISTA_ESTADOS = [    
    ('draft', 'Nuevo'),
    ('pending_recommend', 'Pendiente de recomendar'),
	('recommend', 'Recomendada'),
	('closed', 'Cerrada'),
	('adjudicated', 'Adjudicada'),   
]
class pedido_cotizacion(osv.osv):
    _name="cotizaciones"
    _description="Cotizaciones"
	
    _columns = {
        'name': fields.char('', size=256, required=True),
        'state': fields.selection(LISTA_ESTADOS, 'Estado', size=86, readonly=True),
		'supplier': fields.many2one('res.partner','Proveedores', size=256, required=True),
		'pdc': fields.char('Pedido de compra', size=256, required=True),
		'buyer': fields.many2one('res.users','Comprador', size=256, required=True),
		'currency': fields.many2one('res.currency','Moneda', size=256, required=True),
		'answer_date': fields.date('Fecha de respuesta', required=True),
		'delivery_date': fields.date ('Plazo de entrega', required=True),
		'company_id': fields.many2one ( 'res.company','Compañía' ),
		'pd_ids_solicitado' : fields.one2many ('pedido.cotizacion.line', 'pd_solicitud_id', 'Productos solicitados'),
		'pd_ids_solicitado2' : fields.one2many ('pedido.cotizacion.line', 'pd_solicitud_id', 'Productos solicitados'),
		'pd_ids_solicitado3' : fields.one2many ('pedido.cotizacion.line', 'pd_solicitud_id', 'Productos solicitados'),
		'op1':fields.boolean('Recomendada CAA'),
		'cant_min': fields.integer ('Cantidad mínima'),
		'cant_max': fields.integer ('Cantidad máxima'),
		'nota_proveedor': fields.char ('Nota del proveedor', size = 256),
		'plazo_pago': fields.many2one ('account.payment.term', 'Plazo de pago'),
		'terminos_condiciones': fields.text ( 'Términos y condiciones', size=256),
    }

    def create(self, cr, uid, values, context=None):
         values['name'] = self.pool.get ( 'ir.sequence' ).get ( cr, uid, 'resource.requisition.number' )
         return super(pedido_cotizacion, self).create(cr, uid, values, context=context)

    ############ Señal ###########
    def action_Pendiente_de_recomendar(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'pending_recommend'},context)
        return True
    ############ Señal ###########
    def action_Adjudicada(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'adjudicated'},context)
        return True      
	############ Señal ###########
    def action_Recomendada(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'recommend'},context)
        return True
	############ Señal ###########
    def action_Cerrada(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'closed'},context)
        return True	
		
    _defaults = {
        'state': 'draft',
        'currency': 47,
        'name' : 'COT borrador',
		#'name' : lambda obj, cr, uid, context: obj.pool.get ('ir.sequence').get ( cr, uid, 'cotizacion.requisition.number' ),
    }

class pedido_cotizacion_line (osv.osv):
	_name = "pedido.cotizacion.line"
	_description="Lineas de cotización de pedidos"
	_rec_name = 'product_id'

	def _get_uom_id(self, cr, uid, *args):
		cr.execute('select id from product_uom order by id limit 1')
		res = cr.fetchone()
		return res and res[0] or False
	
	_columns = {
		'product_id': fields.many2one ('product.product', 'Producto', required=True), # Producto
		'pd_solicitud_id' : fields.many2one('cotizaciones','Solicitado', ondelete='cascade'),
		'state': fields.related ( 'pd_solicitud_id', 'state', type = 'char', readonly=True ),
		'product_uom_id': fields.many2one('product.uom', 'Unidad de medida', required=True),
		'product_requested_qty': fields.float ( 'Cantidad', digits_compute=dp.get_precision('Unidad de medida'), required=True),
		'precio': fields.float ( 'Precio', required=True),
		'descripcion': fields.text ( 'Descripción', required=True),
	}
	
	_defaults = {
		'product_uom_id': _get_uom_id,
	}
	
	def onchange_product_id(self, cr, uid, ids, product_id, product_uom_id, context=None):
		""" Changes UoM and name if product_id changes.
		@param name: Name of the field
		@param product_id: Changed product_id
		@return:  Dictionary of changed values
		"""
		value = {'product_uom_id': ''}
		if product_id:
				prod = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
				value = {'product_uom_id': prod.uom_id.id,'product_requested_qty':1.0}
		return {'value': value}
