# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
import netsvc
import datetime
import time
import openerp.addons.decimal_precision as dp
import openerp.addons.purchase_requisition




LISTA_ESTADOS = [
		('draft', 'Nuevo'),
		('sent_to_approval', 'Pendiente de aprobacion'),
		('approved', 'Aprobado'),
		('rejected', 'Rechazado'),
        ('affected', 'Afectado'),
        ('proveedores_invitados', 'Proveedores invitados'),
]

LISTA_TC = [
    ('cd', 'Compra directa'),
    ('nd', 'No definida'),
]


LISTA_STC = [
    ('nd', 'No Definida'),
    ('cdc', 'Compra directa común'),
    ('cda', 'Compra directa abreviada'),
    ('cde', 'Compra directa por excepción'),
]



class pedidos_compra(osv.osv):
    #_inherit = "mail.thread"
    _name="pedidos.compra"
    _description="Pedidos de Compra"
    _columns = {
	
        'name': fields.char('Referencia de pedido', size=80),
        'origin': fields.char('Documento original', size=32),
        'date_start': fields.date('Fecha creado', required=True),
        'date_end': fields.date('Fecha expiración', required=True),	
        'description': fields.text('Referencia de pedido', required=True),
        'user_id': fields.many2one('res.users', 'Creado por'),
        'company_id': fields.many2one('res.company', 'Empresa', required=True),
        'nro_ped_compra':fields.char('Nro. pedido', size=25),
        'usr_solicitado':fields.many2one('res.users', 'Solicitado por'),
        'usr_aprobado':fields.many2one('res.users', 'Aprobado por'),
        'inciso': fields.char('Inciso', size=02),
        'u_e': fields.char('UE', size=03),
		#nuevas lineas 
		'line_ids' : fields.one2many('pedidos.compra.line','pc_line_ids','Products to Purchase'),
		#'line_sc' : fields.one2many('pedidos.solicitud.compra.line','product_id_sc','Lineas S.C.'),
        #fields.many2many('other.object.name', 'relation object',  'actual.object.id',  'other.object.id',  'Field Name')
        'line_sc' : fields.many2many('purchase.requisition.line', 'pedidos_compra_purchase_requisition_line_rel',  'pedidos_compra_id',  'purchase_requisition_line_id',  'Lineas SC'),
		#'line_sc' : fields.many2many('pedidos.solicitud.compra.line','product_id_prl','Lineas S.C.'),
        'state': fields.selection(LISTA_ESTADOS, 'Estado', size=60, readonly=True),
        'tipo_compra':fields.selection(LISTA_TC, 'Tipo compra'),
        'sub_tipo_compra':fields.selection(LISTA_STC, 'Sub tipo compra'),
        'por_sc': fields.boolean('Ver solicitudes de compra'),        
    }
    
    
    def _get_company_id(self, cr, uid, context=None):
            res = self.pool.get('res.users').read(cr, uid, [uid], ['company_id'], context=context)
            if res and res[0]['company_id']:
                    return res[0]['company_id'][0]
            return False

    def _get_user_id(self, cr, uid, context=None):
            """
            If the user is logged in (i.e. not anonymous), get the user's name to
            pre-fill the partner_name field.
            Same goes for the other _get_user_attr methods.

            @return current user's name if the user isn't "anonymous", None otherwise
            """
            user_id = self.pool.get('res.users').read(cr, uid, uid, ['id'], context)

            return user_id['id']

    def _get_user_name(self, cr, uid, context=None):
            """
            If the user is logged in (i.e. not anonymous), get the user's name to
            pre-fill the partner_name field.
            Same goes for the other _get_user_attr methods.

            @return current user's name if the user isn't "anonymous", None otherwise
            """
            user = self.pool.get('res.users').read(cr, uid, uid, ['login'], context)

            if (user['login'] != 'anonymous'):
                    return self.pool.get('res.users').name_get(cr, uid, uid, context)[0][1]
            else:
                    return None


    
    def _check_dates(self, cr, uid, ids, context=None):
        leave = self.read(cr, uid, ids[0], ['date_start', 'date_end'])
        if leave['date_start'] and leave['date_end']:
            if leave['date_start'] > leave['date_end']:
                return False
        return True

    _constraints = [ 
        (_check_dates, '\n \n Error !!!  Fecha Solicitud es mayor que Fecha Expiración', ['date_start'])
                    ]

    ############ Senhal ###########
    def action_Aprobado(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'approved'},context)
        return True
    ############ Senhal ###########
    def action_Afectado(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'affected'},context)
        return True
    ############ Senhal ###########
    def action_Proveedores_invitados(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'proveedores_invitados'},context)
        return True
    ############ Senhal ###########
    def action_Recepcion_de_ofertas(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':''},context)
        return True
    ############ Senhal ###########
    def action_Pendiente_de_aprobacion(self, cr, uid, ids, context=None):
        subject = 'Pendiente de aprobacion'
        
        cr.execute("""  select partner_id from res_users where id = %s""", (uid,))
        cli = cr.fetchone()[0]
        
        """message = self.pool.get('mail.message')
        message.create(cr, uid, {
        'res_id': ids[0],
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'author_id': cli,
        'model': self._name,
        'subject' : subject,
        'body': 'Esperando por aprobacion'
        }, context=context)"""  
        self.write(cr,uid,ids,{'state':'sent_to_approval'
                            } ,context)
        return True
    ############ Senhal ###########
    def action_Rechazado(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'rejected'},context)
        return True
        
    ############ Sehnal ###########
    #def action_Solicitar_Aprobacion(self, cr, uid, ids, context=None):
    #    self.write(cr,uid,ids,{'state':'sent_to_approval'},context)
    #    return True
        
    ############ Consulta Solicitud de compras ###########
    def button_impotar_sc(self, cr, uid, ids, context=None):
    #    #self.write(cr,uid,ids,{'state':'rechazado'},context)
        return True
        
    _defaults = {
        'state': 'draft',
		'nro_ped_compra': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'pedido.compra.number') ,
		#'nro_ped_compra': 'Pedido borrador' ,
        'name': 'nro_ped_compra',
        'date_start':  lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
        'company_id': _get_company_id,
        'user_id': _get_user_id,
        'tipo_compra': 'cd',        
        'sub_tipo_compra': 'cdc',
        'por_sc': False,
        'inciso': '06',
        'u_e': '001'
           }

    
    #***********************************
    

class pedidos_compra_line(osv.osv):

    _name = "pedidos.compra.line"
    _description="Lineas de Pedidos DE Compra"
    _rec_name = 'product_id'

    _columns = {
        'product_id': fields.many2one('product.product', 'Articulo', required=True),
        'product_uom_id': fields.many2one('product.uom', 'Unidad de medida'),
        'product_qty': fields.float('Cantidad', digits_compute=dp.get_precision('Product Unit of Measure')),
        'pc_line_ids': fields.many2one('pedidos.compra.line','Pedido', ondelete='cascade'),
        'company_id': fields.related('pc_line_ids','company_id',type='many2one',relation='res.company',string='Company', store=True, readonly=True),
        'odg': fields.char('ODG', size=10),
        'iva': fields.char('I.V.A.', size=6),
        'nota': fields.text('Nota al proveedor'),
        
    }
    """_sql_constraints = [
        ('product_id_uniq', 'unique(product_id, x_pedido_id)', '\n \n Ya existe un registro para este producto!'),
                        ]"""
    def onchange_product_id(self, cr, uid, ids, product_id, product_uom_id, context=None):
        """ Changes UoM and name if product_id changes.
        @param name: Name of the field
        @param product_id: Changed product_id
        @return:  Dictionary of changed values
        """
        value = {'product_uom_id': ''}
        if product_id:
            prod = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            value = {'product_uom_id': prod.uom_id.id,'product_qty':1.0}
        return {'value': value}
    
    def _check_product_qty(self, cr, uid, ids, context=None):
        leave = self.read(cr, uid, ids, ['product_qty', 'product_id'])
        valor=all(map(lambda a: a['product_qty']>=0.001 ,leave))
        mi_log(valor)
        return valor

    _constraints = [ 
        (_check_product_qty, '\n \n Error !!!  La cantidad no puede ser menor que 1', ['product_qty'])
                    ]

class purchase_requisition_line(osv.osv):

    _inherit = "purchase.requisition.line"

    _columns = {
        'product_qty_2_buy_sc': fields.float('A Comprar', digits_compute=dp.get_precision('Product Unit of Measure')),       
        'seleccionado': fields.boolean('Seleccionado'),
        'odg': fields.char('ODG', size=10),
        'iva': fields.char('I.V.A.', size=6),
        'nota': fields.text('Nota al proveedor'),
        #'product_id': fields.many2one('product.product', 'Product' ),
        #'product_uom_id': fields.many2one('product.uom', 'Product Unit of Measure'),
        #'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        #'requisition_id' : fields.many2one('purchase.requisition','Purchase Requisition', ondelete='cascade'),
        #'company_id': fields.related('requisition_id','company_id',type='many2one',relation='res.company',string='Company', store=True, readonly=True),
    }

    def onchange_product_qty_2_buy_sc(self, cr, uid, ids, product_id, product_qty_2_buy_sc, seleccionado, context=None):
        value = {'seleccionado':seleccionado}
        if product_id:
            if product_qty_2_buy_sc != 0: 
                value = {'seleccionado':True}
        return {'value': value}

    def onchange_seleccionado(self, cr, uid, ids, id,product_id, product_qty_2_buy_sc, seleccionado, context=None):
        value = {'product_qty_2_buy_sc':product_qty_2_buy_sc}
        if seleccionado:
            prod = self.pool.get('purchase.requisition.line').browse(cr, uid, id, context=context)
            if product_qty_2_buy_sc == 0:
                value = {'product_qty_2_buy_sc':prod['product_qty']}                    
        return {'value': value}
    _defaults = {
        'product_qty_2_buy_sc': 0,
        'seleccionado': False
           }

purchase_requisition_line()












#*********************************************************************************
def mi_log(mensaje):
    Milog = netsvc.Logger()
    Milog.notifyChannel('init', netsvc.LOG_WARNING, '**** Mensaje log MD **** : %s' %( mensaje ,)) 
