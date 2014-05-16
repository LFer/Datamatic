{
    "name" : "GRP - Pedidos de compras",
    "version" : "1.0",
    "author" : "Datamatic",
    "website" : "www.datamatic.com.uy",
    "category" : "GRP",
    "description": "GRP",
	'depends' : ["account", "stock", "purchase_requisition", "grp_solicitud_de_recursos"],
    # Tiene que depender de Solicitud de recursos - por menu principal
    "init_xml" : [],
    "demo_xml" : [],
    'data': [
        'security/grp_pedido_compra_security.xml',
        'security/ir.model.access.csv',
                    ],
    "update_xml" : [
        				'pedido_compra_view.xml',
        				'pedido_compra_workflow.xml',
        				'pedido_compra_secuencia.xml',
        			],
    "installable": True,
    "active": False,
}
