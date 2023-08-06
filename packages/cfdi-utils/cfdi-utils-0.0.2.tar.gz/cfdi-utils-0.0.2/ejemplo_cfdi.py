from cfdi_utils import CFDI40
from cfdi_utils.SelloDigital import SelloDigital

from io import StringIO
from datetime import datetime
from pathlib import Path
import lxml.etree as ET

PATH_CER = Path('suppourt-files/FIEL_JES900109Q90_20190614162033/CSD_JES900109Q90_20190617134429/30001000000400002436.cer')
PATH_KEY = Path('suppourt-files/FIEL_JES900109Q90_20190614162033/CSD_JES900109Q90_20190617134429/CSD_Jimenez_Estrada_Salas_1_JES900109Q90_20190617_134353.key')
CONTRASEÑA = '12345678a'

# Crear un objeto SelloDigital
sello = SelloDigital(PATH_CER, PATH_KEY, CONTRASEÑA)
comprobante_dict = {}

CFDI_COMPROBANTE = {
    'Version': '4.0',
    'FormaPago': '01',
    'NoCertificado': sello.numero_cer,
    # 'Certificado': "",
    'SubTotal': 100.00,
    'Total': 100.00,
    'Moneda': 'MXN',
    'TipoDeComprobante': 'I',
    'MetodoPago': 'PUE',
    'LugarExpedicion': '45079',
    # 'Sello': 'faltante',
    'Fecha': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    'Exportacion': '01',
    'Descuento': 1.00,
}

CFDI_EMISOR = {
    'Rfc': 'AAA010101AAA',
    'Nombre': 'EMPRESA DEMO',
    'RegimenFiscal': '601',
}

CFDI_RECEPTOR = {
    'Rfc': 'XAXX010101000',
    'Nombre': 'Publico en General',
    'UsoCFDI': 'G01',
    'DomicilioFiscalReceptor' : '78090',
    'RegimenFiscalReceptor': '601',
}

CFDI_CONCEPTOS = [{
    'ClaveProdServ': '10101502',
    'NoIdentificacion': '1',
    'Cantidad': 1.000000,
    'ClaveUnidad': 'B17',
    'Unidad': 'Actividad',
    'Descripcion': 'Pago',
    'ValorUnitario': 100.00,
    'Importe': 100.00,
    'ObjetoImp': '02',
    'Impuestos': {
        'Traslados': [{
            'Base': '100.00',
            'Impuesto': '002',
            'TipoFactor': 'Tasa',
            'TasaOCuota': '0.160000',
            'Importe': '16.00',
    }]},
}]

comprobante_dict['Emisor'] = CFDI40.EmisorType(**CFDI_EMISOR)
comprobante_dict['Receptor'] = CFDI40.ReceptorType(**CFDI_RECEPTOR)

conceptos_obj = CFDI40.ConceptosType()

# Agregar conceptos al comprobante con impuestos
for concepto in CFDI_CONCEPTOS:
    
    concepto_impuesto = concepto.pop('Impuestos') if 'Impuestos' in concepto else None

    if concepto_impuesto:
        traslados = concepto_impuesto.pop('Traslados')
        traslado_obj = CFDI40.TrasladosType()

        for traslado in traslados:
            traslado_obj.Traslado.append(CFDI40.TrasladoType(**traslado))

        concepto['Impuestos'] = CFDI40.ImpuestosType(Traslados=traslado_obj)
    
    conceptos_obj.add_Concepto(CFDI40.ConceptoType(**concepto))

comprobante_dict['Conceptos'] = conceptos_obj

#Creamos el objeto comprobante
cfdi_obj = CFDI40.Comprobante(**comprobante_dict, **CFDI_COMPROBANTE)

#Exportamos el comprobante sin sellar a XML
output = StringIO()
cfdi_obj.export(output, 0)

#Sellamos el comprobante
signed_xml = sello.sellar_xml(output.getvalue())

#Exportamos el XML
with open('cfdi_sellado.xml', 'wb') as f:
    f.write(signed_xml)



