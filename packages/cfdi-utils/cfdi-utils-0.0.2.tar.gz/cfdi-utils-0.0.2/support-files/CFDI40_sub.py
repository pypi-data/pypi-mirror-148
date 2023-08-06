#!/usr/bin/env python

#
# Generated Sat Apr 16 23:17:11 2022 by generateDS.py version 2.40.10.
# Python 3.9.7 | packaged by conda-forge | (default, Sep 29 2021, 19:24:02)  [Clang 11.1.0 ]
#
# Command line options:
#   ('-o', 'CFDI40.py')
#   ('-s', 'CFDI40_sub.py')
#
# Command line arguments:
#   cfdv40.xsd.xml
#
# Command line:
#   /opt/homebrew/Caskroom/miniforge/base/bin/generateDS -o "CFDI40.py" -s "CFDI40_sub.py" cfdv40.xsd.xml
#
# Current working directory (os.getcwd()):
#   suppourt-files
#

import os
import sys
from lxml import etree as etree_

import ??? as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True

#
# Data representation classes
#


class ComprobanteSub(supermod.Comprobante):
    def __init__(self, Version='4.0', Serie=None, Folio=None, Fecha=None, Sello=None, FormaPago=None, NoCertificado=None, Certificado=None, CondicionesDePago=None, SubTotal=None, Descuento=None, Moneda=None, TipoCambio=None, Total=None, TipoDeComprobante=None, Exportacion=None, MetodoPago=None, LugarExpedicion=None, Confirmacion=None, InformacionGlobal=None, CfdiRelacionados=None, Emisor=None, Receptor=None, Conceptos=None, Impuestos=None, Complemento=None, Addenda=None, **kwargs_):
        super(ComprobanteSub, self).__init__(Version, Serie, Folio, Fecha, Sello, FormaPago, NoCertificado, Certificado, CondicionesDePago, SubTotal, Descuento, Moneda, TipoCambio, Total, TipoDeComprobante, Exportacion, MetodoPago, LugarExpedicion, Confirmacion, InformacionGlobal, CfdiRelacionados, Emisor, Receptor, Conceptos, Impuestos, Complemento, Addenda,  **kwargs_)
supermod.Comprobante.subclass = ComprobanteSub
# end class ComprobanteSub


class InformacionGlobalTypeSub(supermod.InformacionGlobalType):
    def __init__(self, Periodicidad=None, Meses=None, Año=None, **kwargs_):
        super(InformacionGlobalTypeSub, self).__init__(Periodicidad, Meses, Año,  **kwargs_)
supermod.InformacionGlobalType.subclass = InformacionGlobalTypeSub
# end class InformacionGlobalTypeSub


class CfdiRelacionadosTypeSub(supermod.CfdiRelacionadosType):
    def __init__(self, TipoRelacion=None, CfdiRelacionado=None, **kwargs_):
        super(CfdiRelacionadosTypeSub, self).__init__(TipoRelacion, CfdiRelacionado,  **kwargs_)
supermod.CfdiRelacionadosType.subclass = CfdiRelacionadosTypeSub
# end class CfdiRelacionadosTypeSub


class CfdiRelacionadoTypeSub(supermod.CfdiRelacionadoType):
    def __init__(self, UUID=None, **kwargs_):
        super(CfdiRelacionadoTypeSub, self).__init__(UUID,  **kwargs_)
supermod.CfdiRelacionadoType.subclass = CfdiRelacionadoTypeSub
# end class CfdiRelacionadoTypeSub


class EmisorTypeSub(supermod.EmisorType):
    def __init__(self, Rfc=None, Nombre=None, RegimenFiscal=None, FacAtrAdquirente=None, **kwargs_):
        super(EmisorTypeSub, self).__init__(Rfc, Nombre, RegimenFiscal, FacAtrAdquirente,  **kwargs_)
supermod.EmisorType.subclass = EmisorTypeSub
# end class EmisorTypeSub


class ReceptorTypeSub(supermod.ReceptorType):
    def __init__(self, Rfc=None, Nombre=None, DomicilioFiscalReceptor=None, ResidenciaFiscal=None, NumRegIdTrib=None, RegimenFiscalReceptor=None, UsoCFDI=None, **kwargs_):
        super(ReceptorTypeSub, self).__init__(Rfc, Nombre, DomicilioFiscalReceptor, ResidenciaFiscal, NumRegIdTrib, RegimenFiscalReceptor, UsoCFDI,  **kwargs_)
supermod.ReceptorType.subclass = ReceptorTypeSub
# end class ReceptorTypeSub


class ConceptosTypeSub(supermod.ConceptosType):
    def __init__(self, Concepto=None, **kwargs_):
        super(ConceptosTypeSub, self).__init__(Concepto,  **kwargs_)
supermod.ConceptosType.subclass = ConceptosTypeSub
# end class ConceptosTypeSub


class ConceptoTypeSub(supermod.ConceptoType):
    def __init__(self, ClaveProdServ=None, NoIdentificacion=None, Cantidad=None, ClaveUnidad=None, Unidad=None, Descripcion=None, ValorUnitario=None, Importe=None, Descuento=None, ObjetoImp=None, Impuestos=None, ACuentaTerceros=None, InformacionAduanera=None, CuentaPredial=None, ComplementoConcepto=None, Parte=None, **kwargs_):
        super(ConceptoTypeSub, self).__init__(ClaveProdServ, NoIdentificacion, Cantidad, ClaveUnidad, Unidad, Descripcion, ValorUnitario, Importe, Descuento, ObjetoImp, Impuestos, ACuentaTerceros, InformacionAduanera, CuentaPredial, ComplementoConcepto, Parte,  **kwargs_)
supermod.ConceptoType.subclass = ConceptoTypeSub
# end class ConceptoTypeSub


class ImpuestosTypeSub(supermod.ImpuestosType):
    def __init__(self, Traslados=None, Retenciones=None, **kwargs_):
        super(ImpuestosTypeSub, self).__init__(Traslados, Retenciones,  **kwargs_)
supermod.ImpuestosType.subclass = ImpuestosTypeSub
# end class ImpuestosTypeSub


class TrasladosTypeSub(supermod.TrasladosType):
    def __init__(self, Traslado=None, **kwargs_):
        super(TrasladosTypeSub, self).__init__(Traslado,  **kwargs_)
supermod.TrasladosType.subclass = TrasladosTypeSub
# end class TrasladosTypeSub


class TrasladoTypeSub(supermod.TrasladoType):
    def __init__(self, Base=None, Impuesto=None, TipoFactor=None, TasaOCuota=None, Importe=None, **kwargs_):
        super(TrasladoTypeSub, self).__init__(Base, Impuesto, TipoFactor, TasaOCuota, Importe,  **kwargs_)
supermod.TrasladoType.subclass = TrasladoTypeSub
# end class TrasladoTypeSub


class RetencionesTypeSub(supermod.RetencionesType):
    def __init__(self, Retencion=None, **kwargs_):
        super(RetencionesTypeSub, self).__init__(Retencion,  **kwargs_)
supermod.RetencionesType.subclass = RetencionesTypeSub
# end class RetencionesTypeSub


class RetencionTypeSub(supermod.RetencionType):
    def __init__(self, Base=None, Impuesto=None, TipoFactor=None, TasaOCuota=None, Importe=None, **kwargs_):
        super(RetencionTypeSub, self).__init__(Base, Impuesto, TipoFactor, TasaOCuota, Importe,  **kwargs_)
supermod.RetencionType.subclass = RetencionTypeSub
# end class RetencionTypeSub


class ACuentaTercerosTypeSub(supermod.ACuentaTercerosType):
    def __init__(self, RfcACuentaTerceros=None, NombreACuentaTerceros=None, RegimenFiscalACuentaTerceros=None, DomicilioFiscalACuentaTerceros=None, **kwargs_):
        super(ACuentaTercerosTypeSub, self).__init__(RfcACuentaTerceros, NombreACuentaTerceros, RegimenFiscalACuentaTerceros, DomicilioFiscalACuentaTerceros,  **kwargs_)
supermod.ACuentaTercerosType.subclass = ACuentaTercerosTypeSub
# end class ACuentaTercerosTypeSub


class InformacionAduaneraTypeSub(supermod.InformacionAduaneraType):
    def __init__(self, NumeroPedimento=None, **kwargs_):
        super(InformacionAduaneraTypeSub, self).__init__(NumeroPedimento,  **kwargs_)
supermod.InformacionAduaneraType.subclass = InformacionAduaneraTypeSub
# end class InformacionAduaneraTypeSub


class CuentaPredialTypeSub(supermod.CuentaPredialType):
    def __init__(self, Numero=None, **kwargs_):
        super(CuentaPredialTypeSub, self).__init__(Numero,  **kwargs_)
supermod.CuentaPredialType.subclass = CuentaPredialTypeSub
# end class CuentaPredialTypeSub


class ComplementoConceptoTypeSub(supermod.ComplementoConceptoType):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(ComplementoConceptoTypeSub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.ComplementoConceptoType.subclass = ComplementoConceptoTypeSub
# end class ComplementoConceptoTypeSub


class ParteTypeSub(supermod.ParteType):
    def __init__(self, ClaveProdServ=None, NoIdentificacion=None, Cantidad=None, Unidad=None, Descripcion=None, ValorUnitario=None, Importe=None, InformacionAduanera=None, **kwargs_):
        super(ParteTypeSub, self).__init__(ClaveProdServ, NoIdentificacion, Cantidad, Unidad, Descripcion, ValorUnitario, Importe, InformacionAduanera,  **kwargs_)
supermod.ParteType.subclass = ParteTypeSub
# end class ParteTypeSub


class InformacionAduaneraType4Sub(supermod.InformacionAduaneraType4):
    def __init__(self, NumeroPedimento=None, **kwargs_):
        super(InformacionAduaneraType4Sub, self).__init__(NumeroPedimento,  **kwargs_)
supermod.InformacionAduaneraType4.subclass = InformacionAduaneraType4Sub
# end class InformacionAduaneraType4Sub


class ImpuestosType10Sub(supermod.ImpuestosType10):
    def __init__(self, TotalImpuestosRetenidos=None, TotalImpuestosTrasladados=None, Retenciones=None, Traslados=None, **kwargs_):
        super(ImpuestosType10Sub, self).__init__(TotalImpuestosRetenidos, TotalImpuestosTrasladados, Retenciones, Traslados,  **kwargs_)
supermod.ImpuestosType10.subclass = ImpuestosType10Sub
# end class ImpuestosType10Sub


class RetencionesType11Sub(supermod.RetencionesType11):
    def __init__(self, Retencion=None, **kwargs_):
        super(RetencionesType11Sub, self).__init__(Retencion,  **kwargs_)
supermod.RetencionesType11.subclass = RetencionesType11Sub
# end class RetencionesType11Sub


class RetencionType12Sub(supermod.RetencionType12):
    def __init__(self, Impuesto=None, Importe=None, **kwargs_):
        super(RetencionType12Sub, self).__init__(Impuesto, Importe,  **kwargs_)
supermod.RetencionType12.subclass = RetencionType12Sub
# end class RetencionType12Sub


class TrasladosType13Sub(supermod.TrasladosType13):
    def __init__(self, Traslado=None, **kwargs_):
        super(TrasladosType13Sub, self).__init__(Traslado,  **kwargs_)
supermod.TrasladosType13.subclass = TrasladosType13Sub
# end class TrasladosType13Sub


class TrasladoType14Sub(supermod.TrasladoType14):
    def __init__(self, Base=None, Impuesto=None, TipoFactor=None, TasaOCuota=None, Importe=None, **kwargs_):
        super(TrasladoType14Sub, self).__init__(Base, Impuesto, TipoFactor, TasaOCuota, Importe,  **kwargs_)
supermod.TrasladoType14.subclass = TrasladoType14Sub
# end class TrasladoType14Sub


class ComplementoTypeSub(supermod.ComplementoType):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(ComplementoTypeSub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.ComplementoType.subclass = ComplementoTypeSub
# end class ComplementoTypeSub


class AddendaTypeSub(supermod.AddendaType):
    def __init__(self, anytypeobjs_=None, **kwargs_):
        super(AddendaTypeSub, self).__init__(anytypeobjs_,  **kwargs_)
supermod.AddendaType.subclass = AddendaTypeSub
# end class AddendaTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Comprobante'
        rootClass = supermod.Comprobante
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:cfdi="http://www.sat.gob.mx/cfd/4"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Comprobante'
        rootClass = supermod.Comprobante
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Comprobante'
        rootClass = supermod.Comprobante
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:cfdi="http://www.sat.gob.mx/cfd/4"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Comprobante'
        rootClass = supermod.Comprobante
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
