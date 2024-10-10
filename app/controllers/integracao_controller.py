from flask import Blueprint, jsonify, request
from app.utils.auth_utils import token_required
import requests
from datetime import datetime, timedelta
from app.sap_connection import ConnectionSAPHANA
from app.models.vw_wf_po_unidades import VwWFPOUnidades
import xml.etree.ElementTree as ET
from pyrfc import Connection
from app import db

integracao_blueprint = Blueprint('integracao', __name__)

@integracao_blueprint.route('/bionexo', methods=['POST'])
@token_required
def integracao_bionexo():
    
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    id = request.args.get('id', '')
    materiais = request.get_json()
    
    if not is_number(id):
        return jsonify({"error": "Parâmetro 'id' deve conter apenas números"}), 400  

    if not materiais:
        return jsonify({"error": "Nenhum material foi enviado"}), 400

    try:        
        itens_requisicao = ""
        for material in materiais:
            codigo = material.get('codigo', '')
            descricao = material.get('material', '')
            quantidade = material.get('qtd', '')
            
            item_requisicao = f"""
            <Item_Requisicao>
                <Codigo_Produto>{codigo}</Codigo_Produto>
                <Descricao_Produto><![CDATA[{descricao}]]></Descricao_Produto>
                <Quantidade>{quantidade}</Quantidade>
            </Item_Requisicao>
            """
            itens_requisicao += item_requisicao

        soap_envelope = f"""
        <soapenv:Envelope
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:web="http://webservice.bionexo.com/">
            <soapenv:Header/>
            <soapenv:Body>
                <web:post>
                    <login>ws_palmaswdg</login>
                    <password>Bio@1234</password>
                    <operation>WASE</operation>
                    <parameters>WA</parameters>
                    <xml>
                        <Pedido>
                            <Cabecalho>
                                <Requisicao>{id}</Requisicao>
                                <Titulo_Pdc>Cotação de Compra - {id}</Titulo_Pdc>
                                <Contato></Contato>
                                <Id_Forma_Pagamento>3</Id_Forma_Pagamento>
                                <Data_Vencimento>{(datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')}</Data_Vencimento>
                                <Hora_Vencimento>{datetime.now().strftime('%H:%M')}</Hora_Vencimento>
                                <Moeda>Real</Moeda>
                                <Observacao><![CDATA[Cotação enviada da aplicação 'Requisição de Compra SAP']]></Observacao>
                            </Cabecalho>
                            <Itens_Requisicao>
                                {itens_requisicao}
                            </Itens_Requisicao>
                        </Pedido>
                    </xml>
                </web:post>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        soap_endpoint = "https://ws-bionexo-sandbox.bionexo.com/ws2/BionexoBean"
        headers = {'Content-Type': 'text/xml'}

        response = requests.post(soap_endpoint, data=soap_envelope, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": "Erro na resposta do WS Bionexo"}), 500
        
        response_xml = response.text
        
        root = ET.fromstring(response_xml)
        return_element = root.find('.//return')
        if return_element is not None:
            return_text = return_element.text
            attributes = return_text.split(';')
            response_dict = {
                "code": attributes[0],
                "timestamp": attributes[1],
                "retorno": attributes[2]
            }
            return jsonify(response_dict), 200
        else:
            return jsonify({"error": "Formato de resposta inesperado"}), 500
    except Exception as e:
        print(f"Erro ao executar integracao_bionexo: {e}")
        return jsonify({"error": f"Erro ao executar /integracao_bionexo -> {e}"}), 500

@integracao_blueprint.route('/sap', methods=['POST'])
@token_required
def integracao_sap():
    data = request.get_json()
    unidade = data.get('unidade', '')
    materiais = data.get('materiais', '')

    try:
        unidade_sap = VwWFPOUnidades.query.filter_by(unidade=unidade).first()
        if not unidade_sap:
            return jsonify({"error": f"Código SAP da unidade {unidade} não encontrado"}), 404

        cod_sap = unidade_sap.nu_codigo_sap

        connection = ConnectionSAPHANA()
        if not connection:
            return jsonify({"error": "Não foi possível conectar ao SAP HANA"}), 500

        cursor = connection.cursor()

        query = "SELECT LIFNR FROM SAPHANADB.LFM1 lfb WHERE EKORG = ? LIMIT 1"
        cursor.execute(query, (cod_sap,))
        fornecedor = cursor.fetchone()

        POITEM, POITEMX = [], []

        for idx, material in enumerate(materiais):
            query = "SELECT DISTINCT MWSKZ FROM SAPHANADB.EKPO WHERE MATNR = ? AND MWSKZ IS NOT NULL LIMIT 1"
            cursor.execute(query, (material["codigo"],))
            cod_imposto = cursor.fetchone()
            
            quantidade_decimal = float(material["qtd"])

            POITEM_data = {
                'PO_ITEM': f'{(idx + 1) * 10:05d}',
                'MATERIAL': material["codigo"],
                'PLANT': str(cod_sap),
                'QUANTITY': quantidade_decimal,
                'NET_PRICE': material["preco"]
            }

            POITEMX_data = {
                'PO_ITEM': f'{(idx + 1) * 10:05d}',
                'MATERIAL': 'X',
                'PLANT': 'X',
                'QUANTITY': 'X',
                'NET_PRICE': 'X'
            }

            if cod_imposto:
                POITEM_data['TAX_CODE'] = cod_imposto[0]
                POITEMX_data['TAX_CODE'] = 'X'

            POITEM.append(POITEM_data)
            POITEMX.append(POITEMX_data)

        cursor.close()
        connection.close()

        if fornecedor:
            connection = Connection(
                ashost="10.254.250.39",
                sysnr="00",
                client="400",
                user="48749121847",
                passwd="Sap@1234"
            )

            po_data = {
                'POHEADER': {
                    'COMP_CODE': str(cod_sap),
                    'DOC_TYPE': 'NB',
                    'VENDOR': str(fornecedor[0]),
                    'PURCH_ORG': str(cod_sap),
                    'PUR_GROUP': 'C01',
                    'PMNTTRMS': 'Z001',
                    'CURRENCY': 'BRL'
                },
                'POHEADERX': {
                    'COMP_CODE': 'X',
                    'DOC_TYPE': 'X',
                    'VENDOR': 'X',
                    'PURCH_ORG': 'X',
                    'PUR_GROUP': 'X',
                    'PMNTTRMS': 'X',
                    'CURRENCY': 'X'
                },
                'POITEM': POITEM,
                'POITEMX': POITEMX
            }

            result = connection.call('BAPI_PO_CREATE1', **po_data)

            retorno = []
            errors = [error for error in result.get('RETURN', []) if error.get('TYPE') == 'E']

            if errors:
                retorno = [f"{error['TYPE']} - {error['MESSAGE']}" for error in errors]
                return jsonify({"error": retorno})
            else:
                retorno = [f"{line['TYPE']} - {line['MESSAGE']}" for line in result.get('RETURN', [])]
                connection.call('BAPI_TRANSACTION_COMMIT', WAIT='X')
                return jsonify({"id": result['RETURN'][0]["MESSAGE_V2"], "retorno": retorno})

        else:
            return jsonify({"error": f"Fornecedor da organização {cod_sap} não encontrado"})

    except Exception as e:
        print(f"Erro ao gerar requisição de compra SAP: {e}")
        return jsonify({"error": f"Erro ao gerar requisição de compra SAP: {e}"}), 500
