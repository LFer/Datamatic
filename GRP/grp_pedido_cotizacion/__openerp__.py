{
    "name" : "GRP - Pedido de cotizaciones",
    "version" : "1.0",
    "author" : "Datamatic",
    "website" : "www.datamatic.com.uy",
    "category" : "",
    "description": "",
    "depends" : ["account", "stock","product", "grp_solicitud_de_recursos"],
    "init_xml" : [],
    "demo_xml" : [],
    'data': [
		'security/grp_pedido_cotizacion_security.xml',
		'security/ir.model.access.csv',
			],
    "update_xml" : [
        				'pedido_cotizacion_workflow.xml',
        				'pedido_cotizacion_view.xml',
						'pedido_cotizacion_secuencia.xml',
        				],
    "installable": True,
    "active": False,
}
