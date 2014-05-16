# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
import decimal_precision as dp
import time
import openerp.addons.purchase_requisition


import logging
_logger = logging.getLogger(__name__)

class solicitud_recursos(osv.osv):

    _name= 'solicitud.recursos'
    _inherit = 'solicitud.recursos'


    def action_view_cumplir_stock(self, cr, uid, ids, context=None):
        pass


    def action_view_solicitud_compra(self, cr, uid, ids, context=None):

        solicitud = self.browse(cr, uid, ids)
        sol_id = None
        resultado = {}

        # Mensaje de error cuando se toca el boton "solicitar compra" sin haber cargado productos antes
        #raise osv.except_osv(('Atencion'), ('Debe cargar productos antes de solicitar la compra'))

        # Obtener la compañia a partir del usuario
        partner = self.pool.get('res.partner').browse(cr, uid, ids)[0]
        company = partner.company_id.id

        for record in solicitud:
            # Obtener ID de la solicitud
            sol_id = record.id
            for line in record.srl_ids_solicitado:

                if resultado.has_key(line.product_id):
                    resultado[line.product_id].append(line)
                else:
                    resultado[line.product_id] = [line]


       # Cargar las líneas
        for (key,record) in resultado.iteritems():

            lines = [(0,0,{
                'product_id' : r.product_id.id,
                'product_uom_id' : r.product_uom_id.id,
                'cantidad_solicitada' : r.product_requested_qty,
                'cumplida_con_stock': 0,
                'product_qty' : 0,
                'company_id': company,
                })
                    for r in record]

            # Grabar el pedido de compra
            purchase_requisition_id = self.pool.get('purchase.requisition').create(cr, uid,{
                'line_ids': lines,
                'exclusive': 'multiple',
                'origin' : 'Origen: ' + solicitud[0].name,
            })


        self.write ( cr, uid, ids, { 'state' : 'closed_partial' }, context )


        # Mostrar la pantalla
        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'purchase_requisition', 'view_purchase_requisition_form')
        return {
            'name': 'Solicitud de Compra',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res and res[1] or False],
            'res_id': purchase_requisition_id,
            'res_model': 'purchase.requisition',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }


solicitud_recursos()


class purchase_requisition_line(osv.osv):

    _name = "purchase.requisition.line"
    _inherit ="purchase.requisition.line"

    _columns = {
        'cantidad_solicitada': fields.float('Cantidad solicitada', digits_compute=dp.get_precision('Product Unit of Measure')),
        'cumplida_con_stock': fields.float('Cumplida con stock', digits_compute=dp.get_precision('Product Unit of Measure')),
    }


purchase_requisition_line()

